#!/usr/bin/env python3
"""Build scripts/user/main.txt from src/ modules via import graph."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from itertools import product
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
ENTRY = SRC / "index.txt"
OUTPUT = ROOT / "main.txt"
MAP_JSON = ROOT / "minify-map.json"
MAP_MD = ROOT / "minify-map.md"

IMPORT_RE = re.compile(r"^import\s+(\S+)\s*$")
FUNC_RE = re.compile(
    r"^(?:export\s+)?(?:inline\s+)?func\s+(\w+)\s*\(([^)]*)\)", re.MULTILINE
)
FUNC_LINE_RE = re.compile(
    r"^(?:export\s+)?(?:inline\s+)?func\s+(\w+)\s*\(([^)]*)\)\s*$"
)
INLINE_FUNC_RE = re.compile(r"^(?:export\s+)?inline\s+func\s+(\w+)\s*\(([^)]*)\)")
VAR_RE = re.compile(r"^(?:export\s+)?var\s+(\w+)\s*(?:=|$)", re.MULTILINE)
VAR_INDENT_RE = re.compile(r"^\s+var\s+(\w+)\s*(?:=|$)", re.MULTILINE)
CONST_DECL_RE = re.compile(r"^(?:export\s+)?const\s+(\w+)\s*=\s*(.+)$")
AT_REF_RE = re.compile(r"@(\w+)@")
BRIDGE_RE = re.compile(r"^#\s*bridge\s+(.+)$")
ROLE_RE = re.compile(r"^#\s*role\s+(\w+)\s*$")
CONSUMER_RE = re.compile(r"^#\s*consumer\s+(.+)$")
LAYER_RE = re.compile(r"^#\s*layer\s+(\w+)\s*$")
GATE_RE = re.compile(r"^#\s*gate(?:\s+(\w+))?\s*$")
HEADER_BODY_RE = re.compile(r"^(?:export\s+)?(?:func|var|const)\s")
_BUILD_ANNOTATION_PATTERNS = (BRIDGE_RE, ROLE_RE, CONSUMER_RE, LAYER_RE, GATE_RE)

PARAM_SHORT = list("abcdefghijklmnopqrstuvwxyz")
LF_ERROR = "must use LF (\\n) line endings; found carriage return (\\r)"


@dataclass(frozen=True)
class LayerPolicy:
    cross_domain_free: bool = False
    orchestrator_import: bool = False
    blocks_cross_import: bool = False


LAYER_POLICIES: dict[str, LayerPolicy] = {
    "L0": LayerPolicy(cross_domain_free=True, orchestrator_import=True),
    "util": LayerPolicy(cross_domain_free=True, orchestrator_import=False),
    "orchestration": LayerPolicy(blocks_cross_import=True),
}

# Game-state / 语言根名 — 不参与 minify 短名分配（脚本里未必声明，运行时仍占用）
STONESCRIPT_RESERVED: frozenset[str] = frozenset(
    {
        "ai",
        "armor",
        "bighead",
        "buffs",
        "debuffs",
        "empty",
        "encounter",
        "face",
        "foe",
        "harvest",
        "hp",
        "input",
        "item",
        "key",
        "loc",
        "maxhp",
        "pickup",
        "player",
        "pos",
        "res",
        "rng",
        "rngf",
        "screen",
        "summon",
        "this",
        "time",
        "totalgp",
        "totaltime",
        "utc",
    }
)

@dataclass
class FunctionBlock:
    start: int
    end: int
    name: str
    params: list[str]
    forced_inline: bool = False


@dataclass
class ParsedFunction:
    name: str
    params: list[str]
    body: str
    start: int
    end: int
    forced_inline: bool


@dataclass
class ModuleSymbols:
    exported: set[str] = field(default_factory=set)
    private: set[str] = field(default_factory=set)
    consts: set[str] = field(default_factory=set)
    funcs: set[str] = field(default_factory=set)
    vars: set[str] = field(default_factory=set)


@dataclass(frozen=True)
class ModuleAnnotations:
    bridges: frozenset[str]
    role: str | None
    consumers: frozenset[str]
    layer: str | None
    gate: str | None


@dataclass
class ModuleRecord:
    path: str
    raw_text: str
    preserve_row: bool
    row_prologue: str
    imports: list[str]
    symbols: ModuleSymbols
    annotations: ModuleAnnotations


def strip_trailing_comment(line: str) -> str:
    """Remove trailing // comment outside double-quoted strings."""
    in_string = False
    i = 0
    while i < len(line):
        ch = line[i]
        if ch == '"':
            in_string = not in_string
            i += 1
            continue
        if not in_string and ch == "/" and i + 1 < len(line) and line[i + 1] == "/":
            return line[:i].rstrip()
        i += 1
    return line.rstrip()


def top_level_decl_stripped(line: str) -> str:
    stripped = strip_trailing_comment(line).strip()
    if stripped.startswith("export "):
        stripped = stripped[len("export ") :].strip()
    return stripped


def is_build_annotation_line(stripped: str) -> bool:
    return stripped == "#row" or any(
        pattern.match(stripped) for pattern in _BUILD_ANNOTATION_PATTERNS
    )


def is_module_body_start(stripped: str) -> bool:
    return bool(HEADER_BODY_RE.match(stripped))


def module_header_lines(text: str) -> list[str]:
    """Lines before imports / body: stops at indentation or top-level decl."""
    lines: list[str] = []
    for line in text.splitlines():
        if line[:1].isspace():
            break
        stripped = strip_trailing_comment(line).strip()
        if stripped and is_module_body_start(stripped):
            break
        lines.append(line)
    return lines


def is_header_skippable_line(stripped: str) -> bool:
    """Blank, // comment, or build annotations before imports / module body."""
    return not stripped or stripped.startswith("//") or is_build_annotation_line(stripped)


def extract_row_prologue(text: str) -> str:
    """#row 之后、import 或正文之前的序言（注释与空行，原样保留）。"""
    lines = text.splitlines()
    if not lines or strip_trailing_comment(lines[0]).strip() != "#row":
        return ""
    prologue: list[str] = []
    for idx in range(1, len(lines)):
        line = lines[idx]
        if line[:1].isspace():
            break
        stripped = strip_trailing_comment(line).strip()
        if stripped and is_build_annotation_line(stripped):
            continue
        if stripped and IMPORT_RE.match(stripped):
            break
        prologue.append(line)
    if not prologue:
        return ""
    body = "\n".join(prologue)
    # "\n".join 会吞掉末尾空行元素，序言若止于空行需补回
    if not prologue[-1]:
        body += "\n"
    elif not body.endswith("\n"):
        body += "\n"
    return body


def parse_module_header(text: str) -> tuple[bool, list[str]]:
    preserve_row = False
    imports: list[str] = []
    lines = text.splitlines()
    idx = 0
    if lines and strip_trailing_comment(lines[0]).strip() == "#row":
        preserve_row = True
        idx = 1
    while idx < len(lines):
        line = lines[idx]
        if line[:1].isspace():
            break
        stripped = strip_trailing_comment(line).strip()
        if is_header_skippable_line(stripped):
            idx += 1
            continue
        match = IMPORT_RE.match(stripped)
        if not match:
            break
        imports.append(match.group(1))
        idx += 1
    return preserve_row, imports


def import_path_candidates(spec: str, *, importer: str) -> list[str]:
    """Resolve order: sibling → ancestor dirs → src-root absolute."""
    spec = spec.replace("\\", "/").strip()
    candidates: list[str] = []
    dir_path = PurePosixPath(importer).parent
    while True:
        dir_str = dir_path.as_posix()
        if dir_str and dir_str != ".":
            candidates.append(f"{dir_str}/{spec}.txt")
            candidates.append(f"{dir_str}/{spec}/index.txt")
        parent = dir_path.parent
        if parent == dir_path:
            break
        dir_path = parent
    candidates.append(f"{spec}.txt")
    candidates.append(f"{spec}/index.txt")
    return candidates


def resolve_import(spec: str, *, importer: str) -> str:
    spec = spec.replace("\\", "/").strip()
    if not spec:
        raise SystemExit(f"{importer}: empty import path")

    for rel in import_path_candidates(spec, importer=importer):
        if (SRC / rel).is_file():
            return rel
    raise SystemExit(f"{importer}: unresolved import `{spec}`")


def read_src_text(path: str) -> str:
    """Read src/*.txt as UTF-8; reject CR (LF-only line endings)."""
    raw = (SRC / path).read_bytes()
    if b"\r" in raw:
        raise SystemExit(f"{path}: {LF_ERROR}")
    return raw.decode("utf-8")


def find_line_ending_violations() -> list[str]:
    return [
        f"{path}: {LF_ERROR}"
        for path in sorted(list_all_src_modules())
        if b"\r" in (SRC / path).read_bytes()
    ]


def load_module(path: str) -> ModuleRecord:
    text = read_src_text(path)
    preserve_row, raw_imports = parse_module_header(text)
    imports = [resolve_import(spec, importer=path) for spec in raw_imports]
    return ModuleRecord(
        path=path,
        raw_text=text,
        preserve_row=preserve_row,
        row_prologue=extract_row_prologue(text) if preserve_row else "",
        imports=imports,
        symbols=parse_module_symbols(text),
        annotations=parse_module_annotations(text),
    )


def is_index_module(path: str) -> bool:
    return path == "index.txt" or path.endswith("/index.txt")


def list_all_src_modules() -> set[str]:
    return {
        path.relative_to(SRC).as_posix()
        for path in SRC.rglob("*.txt")
        if path.is_file()
    }


def collect_module_order(entry: str) -> tuple[list[str], list[str]]:
    order: list[str] = []
    visited: set[str] = set()
    visiting: set[str] = set()
    stack: list[str] = []
    cycle_errors: list[str] = []

    def visit(path: str) -> None:
        if path in visited:
            return
        if path in visiting:
            start = stack.index(path)
            cycle = stack[start:] + [path]
            cycle_errors.append(f"circular import: {' -> '.join(cycle)}")
            return
        visiting.add(path)
        stack.append(path)
        module = load_module(path)
        for imp in module.imports:
            visit(imp)
        stack.pop()
        visiting.remove(path)
        visited.add(path)
        order.append(path)

    visit(entry)
    return order, cycle_errors


def parse_module_symbols(text: str) -> ModuleSymbols:
    exported: set[str] = set()
    private: set[str] = set()
    consts: set[str] = set()
    funcs: set[str] = set()
    vars_: set[str] = set()
    for line in text.splitlines():
        if line[:1].isspace():
            continue
        raw = strip_trailing_comment(line).strip()
        if not raw or raw == "#row":
            continue
        if IMPORT_RE.match(raw):
            continue
        is_exported = raw.startswith("export ")
        stripped = top_level_decl_stripped(line)
        if stripped.startswith("const "):
            match = re.match(r"const\s+(\w+)", stripped)
            if match:
                consts.add(match.group(1))
                if is_exported:
                    exported.add(match.group(1))
                else:
                    private.add(match.group(1))
            continue
        target = exported if is_exported else private
        if stripped.startswith("var "):
            match = re.match(r"var\s+(\w+)", stripped)
            if match:
                name = match.group(1)
                target.add(name)
                vars_.add(name)
        elif stripped.startswith("func ") or stripped.startswith("inline func "):
            match = re.match(r"(?:inline\s+)?func\s+(\w+)", stripped)
            if match:
                name = match.group(1)
                target.add(name)
                funcs.add(name)
    return ModuleSymbols(
        exported=exported,
        private=private,
        consts=consts,
        funcs=funcs,
        vars=vars_,
    )


def symbol_kind(
    name: str,
    module: ModuleRecord,
    *,
    is_const: bool,
) -> str:
    if is_const:
        return "const"
    if name in module.symbols.funcs:
        return "func"
    if name in module.symbols.vars:
        return "var"
    return "symbol"


def is_symbol_definition_line(line: str, name: str, *, kind: str) -> bool:
    if kind == "var-local":
        return bool(re.match(rf"^\s+var\s+{re.escape(name)}\s*(?:=|$)", line))
    if line[:1].isspace():
        return False
    stripped = top_level_decl_stripped(line)
    if kind == "const":
        return bool(re.match(rf"^const\s+{re.escape(name)}\s*=", stripped))
    if kind == "func":
        return bool(re.match(rf"^(?:inline\s+)?func\s+{re.escape(name)}\s*\(", stripped))
    if kind == "var":
        return bool(re.match(rf"^var\s+{re.escape(name)}\s*(?:=|$)", stripped))
    return False


def collect_symbol_usages(
    text: str,
    symbols: set[str],
    *,
    module_path: str | None = None,
    def_module: str | None = None,
    symbol_kinds: dict[str, str] | None = None,
    exclude_definitions: bool = False,
) -> set[str]:
    if not symbols:
        return set()
    used: set[str] = set()
    for line in text.splitlines():
        stripped = strip_trailing_comment(line).strip()
        if stripped == "#row" or IMPORT_RE.match(stripped):
            continue
        code = strip_trailing_comment(line)
        for name in symbols:
            if (
                exclude_definitions
                and module_path == def_module
                and symbol_kinds
                and is_symbol_definition_line(line, name, kind=symbol_kinds[name])
            ):
                continue
            if re.search(rf"\b{re.escape(name)}\b", code):
                used.add(name)
        for match in AT_REF_RE.finditer(code):
            ref = match.group(1)
            if ref in symbols:
                used.add(ref)
    return used


def build_symbol_registry(
    modules: dict[str, ModuleRecord],
) -> tuple[dict[str, tuple[str, bool, bool, str]], list[str]]:
    """Map symbol -> (module, exported, is_const, kind)."""
    registry: dict[str, tuple[str, bool, bool, str]] = {}
    errors: list[str] = []

    def register(
        name: str,
        path: str,
        *,
        exported: bool,
        is_const: bool,
        kind: str,
    ) -> None:
        if name in registry:
            prev, _, _, _ = registry[name]
            errors.append(f"duplicate symbol `{name}` in `{path}` and `{prev}`")
            return
        registry[name] = (path, exported, is_const, kind)

    for path, module in sorted(modules.items()):
        for name in sorted(module.symbols.consts):
            register(
                name,
                path,
                exported=name in module.symbols.exported,
                is_const=True,
                kind="const",
            )
        for name in sorted(module.symbols.exported | module.symbols.private):
            if name in module.symbols.consts:
                continue
            register(
                name,
                path,
                exported=name in module.symbols.exported,
                is_const=False,
                kind=symbol_kind(name, module, is_const=False),
            )
    return registry, errors


def package_prefix(path: str) -> str | None:
    if "/" in path:
        return path.rsplit("/", 1)[0] + "/"
    return None


def is_subpackage_of(child_pkg: str, parent_pkg: str) -> bool:
    """True when child_pkg is a strict descendant of parent_pkg (e.g. combat/bosses/ under combat/)."""
    return child_pkg.startswith(parent_pkg) and child_pkg != parent_pkg


def can_access_private_symbols(importer_pkg: str | None, imported_pkg: str | None) -> bool:
    """Same package, or importer lives in a sub-package of the imported module."""
    if not importer_pkg or not imported_pkg:
        return False
    if importer_pkg == imported_pkg:
        return True
    return is_subpackage_of(importer_pkg, imported_pkg)


def available_symbols(
    module: ModuleRecord,
    *,
    modules: dict[str, ModuleRecord],
) -> set[str]:
    names = set(module.symbols.exported) | set(module.symbols.private)
    module_pkg = package_prefix(module.path)
    for imp in module.imports:
        imported_mod = modules[imp]
        imported = imported_mod.symbols
        if is_infra_module(imported_mod):
            names |= imported.consts
        else:
            names |= imported.consts & imported.exported
        names |= imported.exported
        imported_pkg = package_prefix(imp)
        if can_access_private_symbols(module_pkg, imported_pkg):
            priv = imported.private
            if not is_infra_module(imported_mod):
                priv -= imported.consts - imported.exported
            names |= priv
    return names


def module_can_reference_symbol(
    importer: str,
    owner: str,
    *,
    modules: dict[str, ModuleRecord],
    exported: bool,
    is_const: bool,
) -> bool:
    if importer == owner:
        return True
    if exported:
        return True
    if is_const:
        owner_mod = modules.get(owner)
        return owner_mod is not None and is_infra_module(owner_mod)
    owner_pkg = package_prefix(owner)
    importer_pkg = package_prefix(importer)
    return can_access_private_symbols(importer_pkg, owner_pkg)


def find_orphan_modules(reachable: set[str]) -> list[str]:
    orphans = sorted(list_all_src_modules() - reachable)
    return [f"unreferenced module `{path}` (not reachable from entry)" for path in orphans]


def find_unused_top_level_symbols(
    modules: dict[str, ModuleRecord],
    registry: dict[str, tuple[str, bool, bool, str]],
) -> list[str]:
    warnings: list[str] = []
    for name, (def_module, exported, is_const, kind) in sorted(registry.items()):
        if kind not in {"func", "var", "const"}:
            continue
        symbol_kinds = {name: kind}
        used = False
        for path in modules:
            if not module_can_reference_symbol(
                path,
                def_module,
                modules=modules,
                exported=exported,
                is_const=is_const,
            ):
                continue
            hits = collect_symbol_usages(
                modules[path].raw_text,
                {name},
                module_path=path,
                def_module=def_module,
                symbol_kinds=symbol_kinds,
                exclude_definitions=True,
            )
            if hits:
                used = True
                break
        if not used:
            vis = "export" if exported else "private"
            warnings.append(f"{def_module}: unused {kind} `{name}` ({vis})")
    return warnings


def find_unused_local_vars(modules: dict[str, ModuleRecord]) -> list[str]:
    warnings: list[str] = []
    local_var_re = re.compile(r"^\s+var\s+(\w+)\s*(?:=|$)")
    for path, module in sorted(modules.items()):
        lines = module.raw_text.splitlines()
        for block in parse_function_blocks(lines):
            declared: dict[str, int] = {}
            for idx in range(block.start + 1, block.end):
                match = local_var_re.match(lines[idx])
                if match:
                    declared[match.group(1)] = idx
            for name, decl_idx in sorted(declared.items()):
                used = False
                for idx in range(block.start + 1, block.end):
                    if idx == decl_idx:
                        continue
                    if re.search(
                        rf"\b{re.escape(name)}\b",
                        strip_trailing_comment(lines[idx]),
                    ):
                        used = True
                        break
                if not used:
                    line_no = decl_idx + 1
                    warnings.append(
                        f"{path}:{line_no}: unused local var `{name}` in func `{block.name}`"
                    )
    return warnings


def find_duplicate_imports(modules: dict[str, ModuleRecord]) -> list[str]:
    warnings: list[str] = []
    for path, module in sorted(modules.items()):
        seen: set[str] = set()
        for imp in module.imports:
            if imp in seen:
                warnings.append(f"{path}: duplicate import `{imp}`")
            seen.add(imp)
    return warnings


def module_domain(path: str) -> str:
    if "/" in path:
        return path.split("/", 1)[0]
    return path.removesuffix(".txt")


def layer_policy(layer: str | None) -> LayerPolicy | None:
    if layer is None:
        return None
    return LAYER_POLICIES.get(layer)


def is_cross_domain_free(*, layer: str | None) -> bool:
    policy = layer_policy(layer)
    return policy is not None and policy.cross_domain_free


def is_barrel_module(path: str, module: ModuleRecord | None = None) -> bool:
    if module is not None and module_role(module) == "barrel":
        return True
    return path.endswith("/index.txt")


def is_entry_module(path: str, module: ModuleRecord) -> bool:
    return module_role(module) == "entry"


def is_infra_module(module: ModuleRecord) -> bool:
    return is_cross_domain_free(layer=module_layer(module))


def is_infra_import(imp: str, modules: dict[str, ModuleRecord]) -> bool:
    imported = modules.get(imp)
    return imported is not None and is_infra_module(imported)


def is_aggregate_import(path: str, modules: dict[str, ModuleRecord]) -> bool:
    """Infra barrel entrypoints — leaf importers must use concrete submodules."""
    imported = modules.get(path)
    if imported is None:
        return False
    return is_barrel_module(path, imported) and is_infra_module(imported)


def gate_consumer_name(path: str, gate: str | None) -> str | None:
    """Return consumer name only when module header declares `#gate`."""
    if gate is None:
        return None
    if gate:
        return gate
    if "/" not in path:
        return path.removesuffix(".txt")
    return PurePosixPath(path).stem


def _annotation_tokens(raw: str) -> set[str]:
    return {part for part in raw.split() if part}


def parse_module_annotations(text: str) -> ModuleAnnotations:
    """Parse build annotations from module header."""
    bridges: set[str] = set()
    role: str | None = None
    consumers: set[str] = set()
    layer: str | None = None
    gate: str | None = None
    for line in module_header_lines(text):
        stripped = strip_trailing_comment(line).strip()
        if not stripped or stripped.startswith("//"):
            continue
        if match := BRIDGE_RE.match(stripped):
            bridges |= _annotation_tokens(match.group(1))
        elif match := ROLE_RE.match(stripped):
            role = match.group(1)
        elif match := CONSUMER_RE.match(stripped):
            consumers |= _annotation_tokens(match.group(1))
        elif match := LAYER_RE.match(stripped):
            layer = match.group(1)
        elif match := GATE_RE.match(stripped):
            gate = match.group(1) or ""
    return ModuleAnnotations(
        bridges=frozenset(bridges),
        role=role,
        consumers=frozenset(consumers),
        layer=layer,
        gate=gate,
    )


def module_role(module: ModuleRecord) -> str | None:
    return module.annotations.role


def module_consumers(module: ModuleRecord) -> frozenset[str]:
    return module.annotations.consumers


def module_bridges(module: ModuleRecord) -> frozenset[str]:
    return module.annotations.bridges


def module_layer(module: ModuleRecord) -> str | None:
    return module.annotations.layer


def is_orchestrator_module(path: str, module: ModuleRecord) -> bool:
    return module_role(module) == "orchestrator"


def is_wiring_module(path: str, module: ModuleRecord) -> bool:
    return module_role(module) == "wiring"


def is_facade_module(module: ModuleRecord) -> bool:
    return module_role(module) == "facade"


def is_orchestrator_allowed_import(
    imp: str,
    modules: dict[str, ModuleRecord],
) -> bool:
    """Orchestrator: root L1, #role facade, or #layer L0 (not util/barrel/entry)."""
    imported = modules.get(imp)
    if imported is None:
        return False
    ann = imported.annotations
    if (
        is_barrel_module(imp, imported)
        or module_role(imported) == "entry"
        or module_role(imported) == "orchestrator"
    ):
        return False
    if is_facade_module(imported):
        return True
    policy = layer_policy(ann.layer)
    if policy is not None:
        if policy.orchestrator_import:
            return True
        if policy.cross_domain_free:
            return False
    if "/" not in imp:
        return True
    return False


def is_orchestration_module(path: str, modules: dict[str, ModuleRecord]) -> bool:
    module = modules.get(path)
    if module is None:
        return False
    policy = layer_policy(module_layer(module))
    return policy is not None and policy.blocks_cross_import


def module_is_cross_import_foundation(
    path: str,
    modules: dict[str, ModuleRecord],
    *,
    visiting: set[str] | None = None,
    safe_cache: dict[str, bool] | None = None,
) -> bool:
    """True when module has no #layer orchestration in its import subgraph."""
    if safe_cache is None:
        safe_cache = {}
    if path in safe_cache:
        return safe_cache[path]
    if visiting is None:
        visiting = set()
    if path in visiting:
        safe_cache[path] = False
        return False
    visiting.add(path)
    if is_orchestration_module(path, modules):
        visiting.remove(path)
        safe_cache[path] = False
        return False
    for imp in modules[path].imports:
        if not module_is_cross_import_foundation(
            imp, modules, visiting=visiting, safe_cache=safe_cache
        ):
            visiting.remove(path)
            safe_cache[path] = False
            return False
    visiting.remove(path)
    safe_cache[path] = True
    return True


def is_direct_orchestrator_import(
    path: str,
    modules: dict[str, ModuleRecord],
) -> bool:
    for orch_path, orch in modules.items():
        if is_orchestrator_module(orch_path, orch) and path in orch.imports:
            return True
    return False


def requires_infra_import_usage_check(
    path: str,
    module: ModuleRecord,
    *,
    modules: dict[str, ModuleRecord],
) -> bool:
    """Root facades and orchestrator deps must use imported #layer L0/util symbols."""
    if (
        is_entry_module(path, module)
        or is_orchestrator_module(path, module)
        or is_wiring_module(path, module)
    ):
        return False
    if is_infra_module(module) or is_barrel_module(path, module):
        return False
    if module_layer(module) == "orchestration":
        return False
    if "/" not in path:
        return True
    return is_direct_orchestrator_import(path, modules)


def symbols_defined_in(
    path: str,
    registry: dict[str, tuple[str, bool, bool, str]],
) -> set[str]:
    return {
        name
        for name, (mod, _, _, kind) in registry.items()
        if mod == path and kind in {"const", "func", "var"}
    }


def find_cross_import_violations(modules: dict[str, ModuleRecord]) -> list[str]:
    errors: list[str] = []
    for path, module in sorted(modules.items()):
        if is_entry_module(path, module) or is_wiring_module(path, module):
            continue

        domain = module_domain(path)
        consumers = module_consumers(module)

        if is_orchestrator_module(path, module):
            for imp in module.imports:
                if not is_orchestrator_allowed_import(imp, modules):
                    errors.append(
                        f"{path}: orchestrator may not import `{imp}` "
                        "(need root L1, #role facade, or #layer L0; "
                        "no util/barrel/entry/orchestrator)"
                    )
            continue

        for imp in module.imports:
            imp_domain = module_domain(imp)
            if domain == imp_domain:
                continue

            imported = modules[imp]
            imported_ann = imported.annotations
            gate_name = gate_consumer_name(imp, imported_ann.gate)
            if gate_name and gate_name not in consumers:
                errors.append(
                    f"{path}: `{imp}` requires `#consumer {gate_name}` on importer"
                )
                continue

            if is_cross_domain_free(layer=imported_ann.layer):
                continue

            target_bridges = module_bridges(imported)
            if domain not in target_bridges:
                errors.append(
                    f"{path}: `{imp}` missing `#bridge {domain}` for cross-domain import"
                )
                continue

            if not module_is_cross_import_foundation(imp, modules):
                errors.append(
                    f"{path}: cross-domain import `{imp}` "
                    "reaches #layer orchestration (transitive)"
                )
    return errors


def find_constants_utils_import_violations(
    modules: dict[str, ModuleRecord],
    registry: dict[str, tuple[str, bool, bool, str]],
) -> list[str]:
    errors: list[str] = []
    for path, module in sorted(modules.items()):
        if is_barrel_module(path, module):
            continue
        for imp in module.imports:
            if is_aggregate_import(imp, modules):
                errors.append(
                    f"{path}: use concrete submodules, not barrel `{imp}`"
                )
        if is_infra_module(module) or not requires_infra_import_usage_check(
            path, module, modules=modules
        ):
            continue
        body = module.raw_text
        for imp in module.imports:
            if not is_infra_import(imp, modules):
                continue
            defined = symbols_defined_in(imp, registry)
            if not defined:
                continue
            used = collect_symbol_usages(body, defined)
            if not used:
                errors.append(
                    f"{path}: unused `{imp}` import (no symbols referenced)"
                )
    return errors


def lint_modules(entry: str) -> list[str]:
    errors = find_line_ending_violations()
    if errors:
        return errors
    order, cycle_errors = collect_module_order(entry)
    reachable = set(order)
    modules = {path: load_module(path) for path in order}
    registry, registry_errors = build_symbol_registry(modules)
    errors.extend(cycle_errors)
    errors.extend(find_orphan_modules(reachable))
    errors.extend(find_duplicate_imports(modules))
    errors.extend(find_cross_import_violations(modules))
    errors.extend(find_constants_utils_import_violations(modules, registry))
    errors.extend(registry_errors)

    all_names = set(registry)
    for path, module in sorted(modules.items()):
        allowed = available_symbols(module, modules=modules)
        used = collect_symbol_usages(module.raw_text, all_names)
        for name in sorted(used):
            if name not in registry:
                continue
            defining_module, exported, is_const, _ = registry[name]
            if defining_module == path:
                continue
            if name in allowed:
                continue
            owner_mod = modules[defining_module]
            infra_const = is_const and is_infra_module(owner_mod)
            if not exported and not infra_const:
                errors.append(
                    f"{path}: uses non-exported `{name}` from `{defining_module}`"
                )
            else:
                errors.append(
                    f"{path}: uses `{name}` from `{defining_module}` without import"
                )

    errors.extend(find_unused_top_level_symbols(modules, registry))
    errors.extend(find_unused_local_vars(modules))
    return errors


def strip_inline_keyword(line: str) -> str:
    stripped = line.lstrip()
    if "inline func" not in stripped:
        return line
    indent = line[: len(line) - len(stripped)]
    stripped = re.sub(r"^(?:export\s+)?inline\s+func\b", "func", stripped)
    return indent + stripped


def strip_build_annotations(text: str) -> str:
    out: list[str] = []
    for line in text.splitlines():
        code = strip_trailing_comment(line).strip()
        if is_build_annotation_line(code):
            continue
        if not line[:1].isspace():
            if IMPORT_RE.match(code):
                continue
            if code.startswith("export "):
                indent = line[: len(line) - len(line.lstrip())]
                line = indent + line.lstrip()[len("export ") :]
            line = strip_inline_keyword(line)
        out.append(line)
    return "\n".join(out)


def compress_text(text: str) -> str:
    out: list[str] = []
    for raw in text.splitlines():
        line = raw.rstrip()
        stripped = line.lstrip()
        if not stripped:
            continue
        if stripped.startswith("//"):
            continue
        out.append(strip_trailing_comment(line))
    return "\n".join(out)


def split_params(params: str) -> list[str]:
    return [part.strip() for part in params.split(",") if part.strip()]


def parse_function_blocks(lines: list[str]) -> list[FunctionBlock]:
    blocks: list[FunctionBlock] = []
    i = 0
    while i < len(lines):
        match = FUNC_LINE_RE.match(lines[i])
        if not match:
            i += 1
            continue
        name = match.group(1)
        params = split_params(match.group(2))
        j = i + 1
        while j < len(lines) and (lines[j].startswith(" ") or lines[j].startswith("\t")):
            j += 1
        blocks.append(FunctionBlock(i, j, name, params))
        i = j
    return blocks


def collect_global_identifiers(text: str) -> set[str]:
    names: set[str] = set()
    for match in FUNC_RE.finditer(text):
        names.add(match.group(1))
    names.update(VAR_RE.findall(text))
    names.update(VAR_INDENT_RE.findall(text))
    return names


def resolve_const_value(value: str, const_map: dict[str, str]) -> str:
    resolved = value
    for name in sorted(const_map, key=len, reverse=True):
        resolved = re.sub(rf"\b{re.escape(name)}\b", const_map[name], resolved)
    return resolved


def extract_const_declarations(
    text: str,
    const_map: dict[str, str],
    *,
    decl_order: list[str] | None = None,
) -> dict[str, str]:
    merged = dict(const_map)
    for line in text.splitlines():
        stripped = top_level_decl_stripped(line)
        if not stripped.startswith("const "):
            continue
        match = CONST_DECL_RE.match(stripped)
        if not match:
            raise SystemExit(f"invalid const declaration: {line!r}")
        if line[:1].isspace():
            raise SystemExit(f"const must be top-level: {line!r}")
        name, value = match.group(1), match.group(2).strip()
        if decl_order is not None and name not in merged:
            decl_order.append(name)
        merged[name] = resolve_const_value(value, merged)
    return merged


def strip_const_declarations(text: str) -> str:
    out_lines: list[str] = []
    for line in text.splitlines():
        stripped = top_level_decl_stripped(line)
        if stripped == "#row":
            continue
        if not line[:1].isspace() and IMPORT_RE.match(strip_trailing_comment(line).strip()):
            continue
        if stripped.startswith("const "):
            match = CONST_DECL_RE.match(stripped)
            if not match:
                raise SystemExit(f"invalid const declaration: {line!r}")
            if line[:1].isspace():
                raise SystemExit(f"const must be top-level: {line!r}")
            continue
        out_lines.append(line)
    return "\n".join(out_lines)


def apply_renames(text: str, mapping: dict[str, str]) -> str:
    if not mapping:
        return text
    for old in sorted(mapping, key=len, reverse=True):
        new = mapping[old]
        text = text.replace(f"@{old}@", f"@{new}@")
        text = re.sub(rf"\b{re.escape(old)}\b", new, text)
    return text


def count_identifier_usages(text: str, name: str) -> int:
    return len(re.findall(rf"\b{re.escape(name)}\b", text))


def choose_const_strategies(
    *,
    const_map: dict[str, str],
    decl_order: list[str],
    merged_stripped: str,
    name_lengths: dict[str, str],
) -> dict[str, str]:
    """Return per-const strategy: ``inline`` or ``var`` (hoisted runtime var)."""
    strategies: dict[str, str] = {}
    for name in decl_order:
        value = const_map[name]
        usages = count_identifier_usages(merged_stripped, name)
        if usages <= 0:
            strategies[name] = "inline"
            continue
        short = name_lengths.get(name, name)
        inline_cost = usages * len(value)
        var_cost = len(f"var {short} = {value}\n") + usages * len(short)
        strategies[name] = "inline" if inline_cost <= var_cost else "var"
    return strategies


def apply_const_substitutions(
    text: str,
    const_map: dict[str, str],
    strategies: dict[str, str],
) -> str:
    text = strip_build_annotations(strip_const_declarations(text))
    inline_map = {
        name: value
        for name, value in const_map.items()
        if strategies.get(name, "inline") == "inline"
    }
    return apply_renames(text, inline_map)


def build_hoisted_const_vars(
    *,
    const_map: dict[str, str],
    strategies: dict[str, str],
    decl_order: list[str],
) -> str:
    lines: list[str] = []
    for name in decl_order:
        if strategies.get(name) != "var":
            continue
        lines.append(f"var {name} = {const_map[name]}")
    if not lines:
        return ""
    return "\n".join(lines) + "\n"


def apply_const_pipeline(
    text: str,
    const_map: dict[str, str],
    strategies: dict[str, str] | None = None,
) -> str:
    if strategies is None:
        strategies = {name: "inline" for name in const_map}
    return apply_const_substitutions(text, const_map, strategies)


def split_top_level_binary(text: str, op: str) -> list[str] | None:
    parts: list[str] = []
    depth = 0
    in_string = False
    start = 0
    i = 0
    while i < len(text):
        ch = text[i]
        if ch == '"':
            in_string = not in_string
            i += 1
            continue
        if in_string:
            i += 1
            continue
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        elif depth == 0 and text[i : i + len(op)] == op:
            parts.append(text[start:i].strip())
            i += len(op)
            start = i
            continue
        i += 1
    parts.append(text[start:].strip())
    if len(parts) <= 1:
        return None
    return parts


def split_call_args(args_str: str) -> list[str]:
    args_str = args_str.strip()
    if not args_str:
        return []
    args: list[str] = []
    depth = 0
    in_string = False
    start = 0
    for i, ch in enumerate(args_str):
        if ch == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        elif ch == "," and depth == 0:
            args.append(args_str[start:i].strip())
            start = i + 1
    args.append(args_str[start:].strip())
    return args


def _literal_truth(expr: str) -> int | None:
    expr = expr.strip()
    if not expr:
        return None
    if re.fullmatch(r"-?\d+(?:\.\d+)?", expr):
        return 1 if float(expr) != 0.0 else 0
    if expr in ("0", "0.0"):
        return 0
    if expr == "1":
        return 1
    match = re.fullmatch(
        r"(-?\d+(?:\.\d+)?)\s*(=|!=|>|<|>=|<=)\s*(-?\d+(?:\.\d+)?)", expr
    )
    if not match:
        return None
    left = float(match.group(1))
    op = match.group(2)
    right = float(match.group(3))
    if op == "=":
        ok = left == right
    elif op == "!=":
        ok = left != right
    elif op == ">":
        ok = left > right
    elif op == "<":
        ok = left < right
    elif op == ">=":
        ok = left >= right
    else:
        ok = left <= right
    return 1 if ok else 0


def fold_arithmetic_factors(expr: str) -> str:
    expr = re.sub(r"1\.0\s*\*\s*", "", expr)
    expr = re.sub(r"\s*\*\s*1\.0\b", "", expr)
    expr = re.sub(r"\(\s*1\.0\s*\*\s*([^)]+)\)", r"(\1)", expr)
    expr = re.sub(r"\(\s*([^)]+)\s*\*\s*1\.0\s*\)", r"(\1)", expr)
    return expr


def fold_logical_chain(expr: str, op: str) -> str:
    parts = split_top_level_binary(expr, op)
    if not parts:
        return fold_arithmetic_factors(expr)
    folded = [fold_expression(part) for part in parts]
    if op == "&":
        for part in folded:
            truth = _literal_truth(part)
            if truth == 0:
                return "0"
        folded = [part for part in folded if _literal_truth(part) != 1]
        if not folded:
            return "1"
        if len(folded) == 1:
            return folded[0]
        return " & ".join(folded)
    for part in folded:
        truth = _literal_truth(part)
        if truth == 1:
            return "1"
    folded = [part for part in folded if _literal_truth(part) != 0]
    if not folded:
        return "0"
    if len(folded) == 1:
        return folded[0]
    return " | ".join(folded)


def fold_expression(expr: str) -> str:
    expr = expr.strip()
    if not expr:
        return expr
    truth = _literal_truth(expr)
    if truth is not None and re.fullmatch(
        r"-?\d+(?:\.\d+)?\s*(=|!=|>|<|>=|<=)\s*-?\d+(?:\.\d+)?", expr
    ):
        return str(truth)
    expr = fold_arithmetic_factors(expr)
    if "&" in expr:
        expr = fold_logical_chain(expr, "&")
    if "|" in expr:
        expr = fold_logical_chain(expr, "|")
    return expr


def fold_line_expressions(line: str) -> str:
    code = strip_trailing_comment(line)
    stripped = code.lstrip()
    if not stripped:
        return line
    indent = code[: len(code) - len(stripped)]
    if stripped.startswith("return "):
        expr = stripped[len("return ") :]
        folded = fold_expression(expr)
        if folded != expr:
            return indent + "return " + folded
    assign = re.match(r"^([\w.]+\s*=\s*)(.+)$", stripped)
    if assign:
        folded = fold_expression(assign.group(2))
        if folded != assign.group(2):
            return indent + assign.group(1) + folded
    if stripped.startswith("?"):
        cond = stripped[1:].strip()
        folded = fold_expression(cond)
        if folded != cond:
            return indent + "?" + folded
    return line


def fold_constants(text: str) -> str:
    return "\n".join(fold_line_expressions(line) for line in text.splitlines())


def parse_functions_detailed(lines: list[str]) -> list[ParsedFunction]:
    functions: list[ParsedFunction] = []
    i = 0
    while i < len(lines):
        match = FUNC_LINE_RE.match(lines[i])
        if not match:
            i += 1
            continue
        name = match.group(1)
        params = split_params(match.group(2))
        forced = bool(INLINE_FUNC_RE.match(lines[i].lstrip()))
        j = i + 1
        body_lines: list[str] = []
        while j < len(lines) and (lines[j].startswith(" ") or lines[j].startswith("\t")):
            body_lines.append(lines[j])
            j += 1
        body = "\n".join(body_lines).rstrip("\n")
        functions.append(
            ParsedFunction(
                name=name,
                params=params,
                body=body,
                start=i,
                end=j,
                forced_inline=forced,
            )
        )
        i = j
    return functions


def normalize_function_body(body: str, params: list[str]) -> str:
    normalized = "\n".join(line.rstrip() for line in body.splitlines()).strip()
    return normalized + "\0" + ",".join(params)


def is_standalone_call_line(line: str, func_name: str) -> bool:
    stripped = strip_trailing_comment(line).strip()
    return bool(re.fullmatch(rf"{re.escape(func_name)}\s*\([^)]*\)", stripped))


def can_inline_function(func: ParsedFunction, *, calls: int) -> bool:
    if func.forced_inline:
        return True
    if calls != 1:
        return False
    return "\n" not in func.body.strip()


def count_function_calls(text: str, name: str, *, definition_line: int | None) -> int:
    count = 0
    lines = text.splitlines()
    for idx, line in enumerate(lines):
        if definition_line is not None and idx == definition_line:
            continue
        count += len(re.findall(rf"\b{re.escape(name)}\s*\(", line))
    return count


def substitute_call_params(body: str, params: list[str], args: list[str]) -> str:
    if len(params) != len(args):
        raise ValueError(f"param/arg mismatch: {params!r} vs {args!r}")
    result = body
    for param, arg in zip(params, args):
        result = result.replace(f"@{param}@", f"@{arg}@")
        result = re.sub(rf"\b{re.escape(param)}\b", arg, result)
    return result


def inline_body_at_indent(body: str, indent: str) -> str:
    lines = body.splitlines()
    if not lines:
        return ""
    out: list[str] = []
    body_indent = lines[0][: len(lines[0]) - len(lines[0].lstrip())] if lines else ""
    for line in lines:
        if line.strip():
            if body_indent and line.startswith(body_indent):
                content = line[len(body_indent) :]
            else:
                content = line.lstrip()
            out.append(indent + content)
        else:
            out.append("")
    return "\n".join(out)


def replace_function_calls_v2(
    text: str,
    func: ParsedFunction,
) -> tuple[str, int]:
    lines = text.splitlines()
    call_re = re.compile(rf"\b{re.escape(func.name)}\s*\(([^)]*)\)")
    replaced = 0
    rebuilt: list[str] = []
    allow_multiline = func.forced_inline
    for idx, line in enumerate(lines):
        if func.start <= idx < func.end:
            continue
        if not call_re.search(line):
            rebuilt.append(line)
            continue
        if "\n" in func.body and not (
            allow_multiline or is_standalone_call_line(line, func.name)
        ):
            rebuilt.append(line)
            continue
        line_indent = line[: len(line) - len(line.lstrip())]
        parts: list[str] = []
        pos = 0
        for match in call_re.finditer(line):
            parts.append(line[pos : match.start()])
            args = split_call_args(match.group(1))
            body = substitute_call_params(func.body, func.params, args)
            body_line = body.strip()
            if body_line.startswith("return "):
                body_line = body_line[len("return ") :]
            if "\n" in body:
                parts.append(inline_body_at_indent(body, line_indent))
            else:
                parts.append(body_line)
            replaced += 1
            pos = match.end()
        parts.append(line[pos:])
        merged = "".join(parts)
        if "\n" in merged and allow_multiline:
            rebuilt.extend(merged.splitlines())
        else:
            rebuilt.append(merged.rstrip())
    if replaced == 0:
        return text, 0
    return "\n".join(rebuilt), replaced


def remove_function_definition(text: str, func: ParsedFunction) -> str:
    lines = text.splitlines()
    return "\n".join(
        line for idx, line in enumerate(lines) if not (func.start <= idx < func.end)
    )


def remap_function_calls(text: str, old_name: str, new_name: str) -> str:
    if old_name == new_name:
        return text
    return re.sub(rf"\b{re.escape(old_name)}\s*\(", f"{new_name}(", text)


def merge_identical_functions(text: str) -> tuple[str, int]:
    merged = 0
    while True:
        lines = text.splitlines()
        functions = parse_functions_detailed(lines)
        body_groups: dict[str, list[ParsedFunction]] = {}
        for func in functions:
            key = normalize_function_body(func.body, func.params)
            body_groups.setdefault(key, []).append(func)
        changed = False
        for group in body_groups.values():
            if len(group) < 2:
                continue
            keeper = min(group, key=lambda f: (len(f.name), f.name))
            for func in group:
                if func.name == keeper.name:
                    continue
                before = text
                text = remap_function_calls(text, func.name, keeper.name)
                if text != before:
                    merged += 1
                    changed = True
                functions = parse_functions_detailed(text.splitlines())
                victim = next((f for f in functions if f.name == func.name), None)
                if victim is not None:
                    remaining = count_function_calls(
                        text, func.name, definition_line=victim.start
                    )
                    if remaining == 0:
                        text = remove_function_definition(text, victim)
        if not changed:
            break
    return text, merged


def find_function_by_name(text: str, name: str) -> ParsedFunction | None:
    for func in parse_functions_detailed(text.splitlines()):
        if func.name == name:
            return func
    return None


def optimize_functions(text: str) -> tuple[str, int]:
    inlined = 0
    for _ in range(64):
        changed = False
        text, merged = merge_identical_functions(text)
        if merged:
            changed = True
        functions = parse_functions_detailed(text.splitlines())
        for func in sorted(functions, key=lambda f: (len(f.body), f.name)):
            calls = count_function_calls(text, func.name, definition_line=func.start)
            if calls == 0:
                text = remove_function_definition(text, func)
                changed = True
                continue
            if not can_inline_function(func, calls=calls):
                continue
            new_text, count = replace_function_calls_v2(text, func)
            if count == 0:
                continue
            victim = find_function_by_name(new_text, func.name)
            if victim is not None:
                new_text = remove_function_definition(new_text, victim)
            text = new_text
            inlined += count
            changed = True
            break
        if not changed:
            break
    return text, inlined


def optimize_release_text(text: str) -> tuple[str, dict[str, int]]:
    before_fold = len(text)
    text = fold_constants(text)
    folded_chars = max(0, before_fold - len(text))
    before_inline = len(text)
    text, inlined_funcs = optimize_functions(text)
    inlined_chars = max(0, before_inline - len(text))
    return text, {
        "folded_chars": folded_chars,
        "inlined_funcs": inlined_funcs,
        "inlined_chars": inlined_chars,
    }


def generate_short_names(count: int, reserved: set[str]) -> list[str]:
    pool: list[str] = []
    letters = "abcdefghijklmnopqrstuvwxyz"
    for length in range(1, 4):
        for combo in product(letters, repeat=length):
            name = "".join(combo)
            if name not in reserved:
                pool.append(name)
            if len(pool) >= count:
                return pool
    raise SystemExit("not enough short identifier names for minification")


def build_global_minify_map(identifiers: set[str], frozen: set[str]) -> dict[str, str]:
    to_rename = sorted(
        (name for name in identifiers if name not in frozen and len(name) > 1),
        key=lambda name: (-len(name), name),
    )
    reserved = set(frozen) | set(identifiers) | STONESCRIPT_RESERVED
    short_names = generate_short_names(len(to_rename), reserved)
    return dict(zip(to_rename, short_names))


def build_param_minify_map(params: list[str]) -> dict[str, str]:
    mapping: dict[str, str] = {}
    slot = 0
    for param in params:
        if len(param) <= 1:
            continue
        while slot < len(PARAM_SHORT) and PARAM_SHORT[slot] == param:
            slot += 1
        if slot >= len(PARAM_SHORT):
            raise SystemExit(f"too many parameters to minify in one function: {params}")
        mapping[param] = PARAM_SHORT[slot]
        slot += 1
    return mapping


def minify_chunk(text: str, global_map: dict[str, str]) -> tuple[str, list[tuple[str, dict[str, str]]]]:
    lines = text.splitlines()
    blocks = parse_function_blocks(lines)

    param_entries: list[tuple[str, dict[str, str]]] = []
    for block in blocks:
        local_map = build_param_minify_map(block.params)
        if not local_map:
            continue
        param_entries.append((block.name, local_map))
        for idx in range(block.start, block.end):
            lines[idx] = apply_renames(lines[idx], local_map)

    result = "\n".join(lines)
    result = apply_renames(result, global_map)
    return result, param_entries


def write_minify_map(
    *,
    global_map: dict[str, str],
    param_entries: list[tuple[str, dict[str, str]]],
    func_name_map: dict[str, str],
    frozen: set[str],
    inlined_consts: dict[str, str],
    var_consts: dict[str, str],
    const_strategies: dict[str, str],
) -> None:
    payload = {
        "frozen": sorted(frozen),
        "consts": {name: value for name, value in sorted(inlined_consts.items())},
        "var_consts": {name: value for name, value in sorted(var_consts.items())},
        "const_strategies": {
            name: const_strategies[name] for name in sorted(const_strategies)
        },
        "globals": {old: global_map[old] for old in sorted(global_map)},
        "params": [
            {
                "function": name,
                "minified": func_name_map.get(name, name),
                "params": {old: new for old, new in sorted(local.items())},
            }
            for name, local in param_entries
            if local
        ],
    }
    MAP_JSON.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    md: list[str] = [
        "# Minify 对照表",
        "",
        "由 `python scripts/user/build.py` 自动生成。",
        "",
        "## #row（不压缩）",
        "",
        "| 原名 | 压缩名 |",
        "|------|--------|",
    ]
    for name in sorted(frozen):
        md.append(f"| `{name}` | `{name}` |")

    if const_strategies:
        md += [
            "",
            "## const 策略",
            "",
            "| 名称 | 策略 | 值 |",
            "|------|------|-----|",
        ]
        for name in sorted(const_strategies):
            strategy = const_strategies[name]
            value = inlined_consts.get(name) or var_consts.get(name, "")
            md.append(f"| `{name}` | `{strategy}` | `{value}` |")

    if inlined_consts:
        md += [
            "",
            "## const（内联，无声明）",
            "",
            "| 名称 | 内联值 |",
            "|------|--------|",
        ]
        for name, value in sorted(inlined_consts.items()):
            md.append(f"| `{name}` | `{value}` |")

    if var_consts:
        md += [
            "",
            "## const（提升为 var）",
            "",
            "| 名称 | 初值 |",
            "|------|------|",
        ]
        for name, value in sorted(var_consts.items()):
            md.append(f"| `{name}` | `{value}` |")

    md += [
        "",
        "## 全局函数 / 变量",
        "",
        "| 原名 | 压缩名 |",
        "|------|--------|",
    ]
    for old, new in sorted(global_map.items(), key=lambda item: item[0].lower()):
        md.append(f"| `{old}` | `{new}` |")

    md += [
        "",
        "## 函数参数（各函数体内独立，短名可复用）",
        "",
        "| 函数 | 压缩后函数名 | 参数原名 | 参数压缩名 |",
        "|------|--------------|----------|------------|",
    ]
    for name, local in param_entries:
        if not local:
            continue
        minified_func = func_name_map.get(name, name)
        for idx, (old, new) in enumerate(sorted(local.items())):
            func_col = f"`{name}`" if idx == 0 else ""
            minified_col = f"`{minified_func}`" if idx == 0 else ""
            md.append(f"| {func_col} | {minified_col} | `{old}` | `{new}` |")

    MAP_MD.write_text("\n".join(md) + "\n", encoding="utf-8", newline="\n")


def build(*, entry: str, dev: bool = False, minify: bool = True) -> tuple[str, dict]:
    order, _ = collect_module_order(entry)
    release = not dev
    do_minify = release and minify

    raw_chars = 0
    frozen: set[str] = set()
    all_texts: dict[str, str] = {}
    const_map: dict[str, str] = {}
    const_decl_order: list[str] = []
    raw_sources: dict[str, str] = {}
    preserve_row: dict[str, bool] = {}

    for path in order:
        module = load_module(path)
        text = module.raw_text
        raw_chars += len(text)
        raw_sources[path] = text
        preserve_row[path] = module.preserve_row
        const_map = extract_const_declarations(
            text, const_map, decl_order=const_decl_order
        )

    analysis_parts: list[str] = []
    for path in order:
        if is_index_module(path):
            continue
        analysis_parts.append(
            strip_build_annotations(strip_const_declarations(raw_sources[path]))
        )
    merged_for_analysis = "\n".join(analysis_parts)

    for path in order:
        if preserve_row[path]:
            frozen |= collect_global_identifiers(
                strip_build_annotations(strip_const_declarations(raw_sources[path]))
            )

    prelim_globals = collect_global_identifiers(merged_for_analysis)
    prelim_map = (
        build_global_minify_map(prelim_globals, frozen) if do_minify else {}
    )
    name_lengths = {name: prelim_map.get(name, name) for name in const_map}
    const_strategies = choose_const_strategies(
        const_map=const_map,
        decl_order=const_decl_order,
        merged_stripped=merged_for_analysis,
        name_lengths=name_lengths,
    )
    inlined_consts = {
        name: value
        for name, value in const_map.items()
        if const_strategies.get(name, "inline") == "inline"
    }
    var_consts = {
        name: const_map[name]
        for name in const_decl_order
        if const_strategies.get(name) == "var"
    }
    hoisted_vars = (
        build_hoisted_const_vars(
            const_map=const_map,
            strategies=const_strategies,
            decl_order=const_decl_order,
        )
        if release
        else ""
    )

    compressed_chunks: dict[str, str] = {}
    for path in order:
        text = apply_const_pipeline(
            raw_sources[path], const_map, const_strategies
        )
        all_texts[path] = text
        if release and not preserve_row[path]:
            compressed_chunks[path] = compress_text(text)

    global_map: dict[str, str] = {}
    all_param_entries: list[tuple[str, dict[str, str]]] = []
    optimize_stats = {"folded_chars": 0, "inlined_funcs": 0, "inlined_chars": 0}

    entry_prologue = (
        extract_row_prologue(raw_sources[entry]) if preserve_row.get(entry) else ""
    )

    if dev:
        parts: list[str] = []
        for path in order:
            if is_index_module(path):
                continue
            parts.append(all_texts[path])
        if entry_prologue:
            if parts:
                parts[0] = entry_prologue + parts[0]
            else:
                parts.append(entry_prologue)
        result = "".join(parts)
    else:
        fixed_parts: list[str] = []
        optimizable_parts: list[str] = []
        for path in order:
            if is_index_module(path):
                continue
            if preserve_row[path]:
                fixed_parts.append(all_texts[path].removesuffix("\n"))
            else:
                optimizable_parts.append(compressed_chunks[path])

        merged_opt = "\n".join(part for part in optimizable_parts if part)
        if hoisted_vars:
            merged_opt = hoisted_vars.removesuffix("\n") + "\n" + merged_opt
        merged_opt, optimize_stats = optimize_release_text(merged_opt)

        if do_minify:
            global_map = build_global_minify_map(
                collect_global_identifiers(merged_opt), frozen
            )
            merged_opt, all_param_entries = minify_chunk(merged_opt, global_map)
        elif release:
            global_map = {}

        body_segments = [*fixed_parts, merged_opt]
        merged = "\n".join(part for part in body_segments if part)
        if entry_prologue:
            merged = entry_prologue + merged
        result = merged
        if result and not result.endswith("\n"):
            result += "\n"

    func_name_map = {
        block.name: global_map.get(block.name, block.name)
        for block in parse_function_blocks(result.splitlines())
    }

    if do_minify:
        write_minify_map(
            global_map=global_map,
            param_entries=all_param_entries,
            func_name_map=func_name_map,
            frozen=frozen,
            inlined_consts=inlined_consts,
            var_consts=var_consts,
            const_strategies=const_strategies,
        )

    return result, {
        "modules": sum(1 for path in order if not is_index_module(path)),
        "raw_chars": raw_chars,
        "out_chars": len(result),
        "saved": raw_chars - len(result),
        "minified_globals": len(global_map),
        "minified_param_slots": sum(len(local) for _, local in all_param_entries),
        "inlined_consts": len(inlined_consts),
        "var_consts": len(var_consts),
        "folded_chars": optimize_stats["folded_chars"],
        "inlined_funcs": optimize_stats["inlined_funcs"],
        "inlined_chars": optimize_stats["inlined_chars"],
    }


def copy_to_clipboard(text: str) -> bool:
    """Copy text to the system clipboard. Returns True on success."""
    try:
        if sys.platform == "win32":
            return _copy_clipboard_win32(text)
        if sys.platform == "darwin":
            proc = subprocess.run(
                ["pbcopy"],
                input=text,
                text=True,
                encoding="utf-8",
                check=False,
            )
            return proc.returncode == 0
        for cmd in (
            ["wl-copy"],
            ["xclip", "-selection", "clipboard"],
            ["xsel", "--clipboard", "--input"],
        ):
            try:
                proc = subprocess.run(
                    cmd,
                    input=text,
                    text=True,
                    encoding="utf-8",
                    capture_output=True,
                    check=False,
                )
            except FileNotFoundError:
                continue
            if proc.returncode == 0:
                return True
        return False
    except OSError:
        return False


def _copy_clipboard_win32(text: str) -> bool:
    import ctypes

    CF_UNICODETEXT = 13
    GMEM_MOVEABLE = 0x0002

    user32 = ctypes.windll.user32
    kernel32 = ctypes.windll.kernel32

    kernel32.GlobalAlloc.argtypes = [ctypes.c_uint, ctypes.c_size_t]
    kernel32.GlobalAlloc.restype = ctypes.c_void_p
    kernel32.GlobalLock.argtypes = [ctypes.c_void_p]
    kernel32.GlobalLock.restype = ctypes.c_void_p
    kernel32.GlobalUnlock.argtypes = [ctypes.c_void_p]
    user32.SetClipboardData.argtypes = [ctypes.c_uint, ctypes.c_void_p]
    user32.SetClipboardData.restype = ctypes.c_void_p

    if not user32.OpenClipboard(None):
        return False
    try:
        if not user32.EmptyClipboard():
            return False
        payload = text.encode("utf-16-le") + b"\x00\x00"
        h_mem = kernel32.GlobalAlloc(GMEM_MOVEABLE, len(payload))
        if not h_mem:
            return False
        locked = kernel32.GlobalLock(h_mem)
        if not locked:
            kernel32.GlobalFree(h_mem)
            return False
        ctypes.memmove(locked, payload, len(payload))
        kernel32.GlobalUnlock(h_mem)
        if not user32.SetClipboardData(CF_UNICODETEXT, h_mem):
            kernel32.GlobalFree(h_mem)
            return False
        return True
    finally:
        user32.CloseClipboard()


def main() -> int:
    parser = argparse.ArgumentParser(description="Build main.txt from src/ modules")
    parser.add_argument(
        "--entry",
        default="index.txt",
        help="entry module under src/ (default: index.txt)",
    )
    parser.add_argument(
        "--dev",
        action="store_true",
        help="concatenate without compression (for diff/debug)",
    )
    parser.add_argument(
        "--no-minify",
        action="store_true",
        help="compress comments but keep original identifier names",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="compare output with existing main.txt; exit 1 on mismatch",
    )
    parser.add_argument(
        "--lint",
        action="store_true",
        help="run full module analysis only; exit 1 on any violation",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=OUTPUT,
        help=f"output file (default: {OUTPUT.name})",
    )
    args = parser.parse_args()

    entry = args.entry.replace("\\", "/")
    if not (SRC / entry).is_file():
        print(f"entry not found: {SRC / entry}", file=sys.stderr)
        return 1

    lint_errors = lint_modules(entry)
    if lint_errors:
        print("module lint failed:", file=sys.stderr)
        for err in lint_errors:
            print(f"  {err}", file=sys.stderr)
        return 1

    if args.lint:
        print("module lint ok")
        return 0

    result, stats = build(entry=entry, dev=args.dev, minify=not args.no_minify)

    if args.check:
        if not args.output.is_file():
            print(f"check failed: {args.output} does not exist", file=sys.stderr)
            return 1
        expected = args.output.read_text(encoding="utf-8")
        if result != expected:
            print("check failed: built output differs from main.txt", file=sys.stderr)
            return 1
        print("check ok")
        return 0

    args.output.write_text(result, encoding="utf-8", newline="\n")
    if copy_to_clipboard(result):
        print("  copied to clipboard")
    else:
        print("  clipboard copy failed", file=sys.stderr)

    release = not args.dev
    do_minify = release and not args.no_minify
    saved = stats["saved"]
    pct = (100.0 * saved / stats["raw_chars"]) if stats["raw_chars"] else 0.0
    mode = "dev" if args.dev else "release"
    print(f"built {args.output.name} ({mode})")
    print(f"  entry: {entry}")
    print(f"  modules: {stats['modules']}")
    print(f"  source chars: {stats['raw_chars']}")
    print(f"  output chars: {stats['out_chars']}")
    if release:
        print(f"  inlined consts: {stats['inlined_consts']}")
        print(f"  hoisted const vars: {stats['var_consts']}")
        print(f"  folded chars: {stats['folded_chars']}")
        print(f"  inlined funcs: {stats['inlined_funcs']}")
        print(f"  inlined chars: {stats['inlined_chars']}")
        if do_minify:
            print(f"  minified globals: {stats['minified_globals']}")
            print(f"  minified param slots: {stats['minified_param_slots']}")
            print(f"  map: {MAP_MD.name}, {MAP_JSON.name}")
        print(f"  saved: {saved} ({pct:.1f}%)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
