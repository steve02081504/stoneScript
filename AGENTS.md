# AGENTS.md — Stonescript 知识库入口

本仓库 = **Stonescript 知识库** + **万能脚本版本库**。不是 Stone Story RPG 游戏源码。

## 接到任务时

**无需请示**，按类型执行：

| 任务 | 先读 | 再查 | 改哪里 |
|------|------|------|--------|
| 改脚本（默认） | [docs/patterns/modules.md](docs/patterns/modules.md)、[docs/patterns/universal-script.md](docs/patterns/universal-script.md) | — | [scripts/user/src/](scripts/user/src/) 对应模块 |
| 查 API | [db/index.json](db/index.json) | 对应 JSON 或 `docs/reference/` | — |
| 排错 | [docs/debugging.md](docs/debugging.md) | `foe.state` / `foe.time` | `scripts/user/src/` 模块 |
| 新地点 / 采集 | [docs/patterns/universal-script.md](docs/patterns/universal-script.md) | `db/game-state.json` | `harvest.txt`、`mobility.txt` 等 |
| 战斗路由 | [docs/patterns/modules.md](docs/patterns/modules.md) § combat | `combat/data` 遭遇标签 | `combat/routing.txt`（`RunCombatFrame` 流水线） |
| 定制遭遇 / BOSS | [docs/patterns/abilities.md](docs/patterns/abilities.md) | `db/native-functions.json` | `combat/dedicated.txt` 分发 + `combat/encounters/*`；新 Boss 须在 `dedicated` 注册 |
| 泛用战斗 / 换装 | [docs/patterns/overwriting.md](docs/patterns/overwriting.md) | `constants/combat` | `combat/generic.txt`、`combat/equip.txt` |
| 能力激活 | [docs/patterns/abilities.md](docs/patterns/abilities.md) | `db/appendix-index.json` | `combat/abilities/`（`index` / `smite` / `finisher`） |
| Boss debuff 轮换 | [docs/patterns/modules.md](docs/patterns/modules.md) § combat | `combat/data` 查表 | `combat/debuff.txt` |
| 加 UI | [docs/reference/ui.md](docs/reference/ui.md) | `db/imports.json` | `src/index.txt` 序言（`#row` 与 `import` 之间） |
| 移速 / 拾取 | [docs/patterns/mobility.md](docs/patterns/mobility.md) | `pickup.distance` | `mobility.txt`、`combat/travel.txt` |
| 攻速 AAC | [docs/patterns/aac.md](docs/patterns/aac.md) | `item.*.state` | `aac.txt` |
| 开关 / 竞速 | — | — | `toggles.txt`（`speedRun`、`useAutoPotion`、`finisher*`、`bestiary*`）、`constants/speedrun.txt` |
| 主循环编排 | [docs/patterns/modules.md](docs/patterns/modules.md) | — | `loop.txt`（唯一 orchestrator） |

文档总目录：[docs/README.md](docs/README.md)。官方外链：[references/sources.md](references/sources.md)。

## 硬性约定

- **只改** [`scripts/user/src/`](scripts/user/src/) 模块；[`scripts/examples/`](scripts/examples/) 只读
- **不要手改** [`scripts/user/main.txt`](scripts/user/main.txt)（构建产物）；改完后运行 `python scripts/user/build.py`
- 新模块通过 **`import` 链** 接入（入口 [`index.txt`](scripts/user/src/index.txt) → `loop.txt` 等）；开关变量写在 [`toggles.txt`](scripts/user/src/toggles.txt)
- 允许 [`index.txt`](scripts/user/src/index.txt) 序言一行**内置** import（如 `import UI/MindstoneButton`）；**禁止**用户自建 import
- 部署：构建 → 全选复制 `main.txt` → 心智石粘贴 → 保存重载
- 缩进决定 `?` 子作用域；多 `equip` 后者覆盖 — 用 `:` / `:?` 避免打断施法
- `var` 在 Ouroboros 循环间不重置；需重置用 `?loc.begin` / `?loc.loop`
- 改完可跑 `python scripts/user/build.py --lint` 检查模块边界
