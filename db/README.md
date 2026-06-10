# db/ — 机器可读索引

供 agent 用 `grep` 或 JSON 解析快速定位 API。

| 文件 | 内容 |
|------|------|
| `index.json` | 关键词 → 条目（入口） |
| `game-state.json` | `?loc`, `foe`, `item` 等 |
| `commands.json` | `equip`, `activate`, `>` 等 |
| `search-filters.json` | 装备/敌人筛选词 |
| `native-functions.json` | 原生函数摘要 |
| `imports.json` | 内置 import 路径 |
| `appendix-index.json` | 冷却 ID、附录索引 |

查询：读 `index.json` 匹配 `topics` → 打开 `file` 指向的 JSON → 需要全文时读条目的 `doc` 字段。

版本：`manual-4.27.1`（2026/01/15）
