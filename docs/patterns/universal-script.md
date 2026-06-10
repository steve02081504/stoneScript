# 万能脚本组织规范

手机版只有一个心智石输入栏。本仓库在开发时拆分为 [`scripts/user/src/`](../../scripts/user/src/) 多模块，构建后得到 [`main.txt`](../../scripts/user/main.txt) 作为**唯一**部署文件。

## 工作流

1. 编辑 [`src/`](../../scripts/user/src/) 下对应模块（模块边界见 [modules.md](modules.md)）
2. `python scripts/user/build.py`
3. 全选复制 `main.txt` → 心智石粘贴 → 保存重载

## 入口结构

[`index.txt`](../../scripts/user/src/index.txt) 为构建入口（`#row` 不压缩）：

```stonescript
#row
// 贤者序言（可选注释）
// import UI/MindstoneButton   ← 内置 import 写在此，import toggles 之前

import toggles
import loop
```

[`toggles.txt`](../../scripts/user/src/toggles.txt) 集中放开关（`speedRun`、`useAutoPotion`、终结技配置等）。

[`loop.txt`](../../scripts/user/src/loop.txt) 为每帧主循环，按 [modules.md](modules.md) 中的顺序调度各 Facade。

## 逻辑分层（概念）

| 段落 | 对应模块 | 说明 |
|------|----------|------|
| 内置 import | `index.txt` 序言 | 最多一行，如 `import UI/MindstoneButton` |
| 开关 | `toggles.txt` | `speedRun`、`useAutoPotion`、终结技、图鉴等 |
| 全局 AAC | `aac.txt` | 每帧最先执行 |
| 主循环 | `loop.txt` | 薄编排，调用各 Facade |
| 战斗路由 | `combat/routing` → `dedicated` / `generic` / `abilities` | 定制遭遇优先，否则泛用链 |
| 具名 Boss | `combat/encounters/*` | 由 `dedicated.txt` 按 foe/loc 分发 |
| 移速 / 采集 | `mobility.txt`、`harvest.txt` | 经 `combat/travel`、`combat/equip` 桥接 |
| 药水 | `potion/*` | loc.begin 炼药 + loop 末尾自动用药 |

战斗子包细节见 [modules.md](modules.md) § combat。

## 新地点 / 采集

地点相关 equip 与距离判断分散在 `harvest.txt`、`mobility.txt`、`combat/data`（地点默认元素）、`combat/encounters/*` 等模块。新 Boss 除 `encounters/<名>.txt` 外须在 `combat/dedicated.txt` 注册匹配与 `Fight*` 调用。地点 id 与游戏内一致（如 `deadwood`, `caves`, `rocky`）。参考 [`scripts/examples/`](../../scripts/examples/) 复制官方片段。

## 用 func 减少重复

模块内用 `func` 复用；跨模块通过 **export func** 暴露 Facade（见 [modules.md](modules.md)）。

## 避免 overwriting

模块内部的 equip 仍会每帧从上到下执行。BOSS 能力等须用 `: / :?`，见 [overwriting.md](overwriting.md)。

## 内置 import 规则

| 允许 | 禁止 |
|------|------|
| `import UI/MindstoneButton` | `import shared/potion` |
| `import UI/BossBar` 等游戏内置路径 | `import by-location/deadwood` |
| 查 [db/imports.json](../../db/imports.json) | 用户存档 `Stonescript/` 下的文件 |

## 性能提示

- 大段 ASCII 打印用 `ascii/asciiend`，避免 `\n` 换行
- 避免每帧重建大数组；用 `?loc.begin` 时 `Clear()` 而非 `= []`
- 嵌套 `for` 不宜过深
