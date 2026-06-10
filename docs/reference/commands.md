# Commands 参考

告诉游戏执行动作的指令。JSON 索引：[db/commands.json](../../db/commands.json)。

## 装备与 loadout

| 命令 | 说明 |
|------|------|
| `equip (str)` | 装备（双手武器必须用此形式）；最多 7 个筛选条件 |
| `equipL (str)` | 左手 |
| `equipR (str)` | 右手 |
| `equip @var@` | 用字符串变量作筛选（支持减法条件如 `-big`） |
| `loadout (n)` | 装备预设 loadout 编号 |

示例：

```stonescript
equip vigor crossbow *8 +5
equipL poison d_sword
equipR vigor shield
var w = "poison sword *10 -big"
equipR @w@
```

## 能力

| 命令 | 说明 |
|------|------|
| `activate (ability)` | `potion`, `P`, `left`, `L`, `right`, `R`，或能力 ID |
| `brew (ingredients)` | 仅在 `time=0` 调配药水，如 `brew bronze + tar` |

## 打印

| 命令 | 说明 |
|------|------|
| `> (str)` | 屏幕顶部打印 |
| `> @var@` | 插值变量 |
| `>(expr` | 大头表情（需 Big Head） |
| `>oX,Y,[#color,](str)` | 相对玩家 |
| `>hX,Y,[#color,](str)` | 大头层（帽子等） |
| `>\`X,Y,[#color,](str)` | 相对屏幕左上角 |
| `>cX,Y,[#color,](str)` | 相对屏幕中心 |
| `>fX,Y,[#color,](str)` | 相对敌人头部 |

颜色：`#rrggbb` 或 `#white`, `#cyan`, `#yellow`, `#green`, `#blue`, `#red`, `#rainFF`。

ASCII 块：`ascii ... asciiend`；`#` 为透明。

## 变量与函数

| 命令 | 说明 |
|------|------|
| `var name = value` | 声明变量（仅首次初始化） |
| `func Name(args)` | 声明函数 |
| `for v = a..b` | 循环 |

## 外部脚本

| 命令 | 说明 |
|------|------|
| `import (script)` | 加载单例外部脚本 |
| `new (script)` | 创建独立副本 |

## HUD / 界面开关

| 命令 | 说明 |
|------|------|
| `disable abilities` / `enable abilities` | 能力按钮 |
| `disable hud (opts)` / `enable hud (opts)` | `p`玩家 `f`敌人 `a`能力 `r`资源 `b`横幅 `u`工具带 |
| `disable banner` / `enable banner` | 地点横幅 |
| `disable loadout input/print` | loadout 快捷键/提示 |
| `disable npcDialog` / `enable npcDialog` | NPC 对话 |
| `disable pause` / `enable pause` | 暂停按钮 |
| `disable player` / `enable player` | 隐藏玩家（纯装饰） |

## 音频

| 命令 | 说明 |
|------|------|
| `play (sound) (pitch)` | 播放音效；pitch 默认 100 |

音效列表见 [db/appendix-index.json](../../db/appendix-index.json) `sounds`。

## 相关

- 原生函数 `music.*`, `ambient.*`：[native-functions.md](native-functions.md)
