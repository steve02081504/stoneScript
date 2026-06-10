# 脚本目录

| 路径 | 用途 |
|------|------|
| [`user/src/`](user/src/) | 模块化源码（按功能拆分） |
| [`user/build.py`](user/build.py) | 构建：import 图拼接 + 压缩 → `main.txt` |
| [`user/main.txt`](user/main.txt) | 构建产物（部署用心智石脚本） |
| `examples/` | 官方对照片段，只读勿改 |

## 工作流

1. 编辑 [`user/src/`](user/src/) 下对应模块（开关写在 [`user/src/toggles.txt`](user/src/toggles.txt)）
2. 构建：`python scripts/user/build.py`
3. 部署：全选复制 `main.txt` → 心智石粘贴 → 保存重载

构建选项：

```bash
python scripts/user/build.py          # 默认：压缩后写入 main.txt
python scripts/user/build.py --dev    # 不压缩，便于 diff
python scripts/user/build.py --lint   # 仅检查 import/export 边界
python scripts/user/build.py --check  # 校验 main.txt 是否与源码一致（未构建则失败）
```

压缩规则：除 [`#row`](user/src/index.txt) 模块（[`index.txt`](user/src/index.txt) 序言与 [`toggles.txt`](user/src/toggles.txt) 开关段）外，其余模块去除空行与注释，并将自定义函数名/变量名缩短；函数参数在各函数体内独立映射为 `a`/`b`/…（可复用）。对照表见 [`user/minify-map.md`](user/minify-map.md)（及 `minify-map.json`）。

```bash
python scripts/user/build.py --no-minify  # 仅去注释，不缩短标识符
```

模块依赖由 [`index.txt`](user/src/index.txt) 的 import 链决定（入口 → `loop.txt` → 各 Facade）。战斗子包：`combat/routing` → `dedicated` / `generic` / `abilities` / `encounters/*`。边界规则见 [docs/patterns/modules.md](../docs/patterns/modules.md)。

工作流与 import 规则见 [docs/getting-started.md](../docs/getting-started.md) 与 [docs/patterns/universal-script.md](../docs/patterns/universal-script.md)。
