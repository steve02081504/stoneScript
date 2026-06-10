# Game State 参考

在 `?` 条件中查询游戏状态。完整 JSON 索引：[db/game-state.json](../../db/game-state.json)。

## 地点 loc

| 表达式 | 说明 |
|--------|------|
| `?loc` | 当前地点（如 `caves`, `deadwood`, `rocky`） |
| `loc.id` | 地点唯一 ID |
| `loc.name` | 本地化名称 |
| `loc.stars` | 难度星级 |
| `loc.gp` | 本次 run 已用 gear power |
| `loc.begin` | 地点第一帧（time=0），Ouroboros 循环后不为真 |
| `loc.loop` | Ouroboros 循环后第一帧 |
| `loc.isQuest` | 是否为 Legend/任务特殊地点 |
| `loc.averageTime` | 加权平均通关帧数 |
| `loc.bestTime` | 最佳通关帧数 |

## 敌人 foe

| 表达式 | 说明 |
|--------|------|
| `?foe` | 当前目标敌人类型 |
| `foe.id` / `foe.name` | ID / 本地化名 |
| `foe.distance` | 与玩家距离 |
| `foe.z` | z 坐标 |
| `foe.count` | 46 单位内敌人数 |
| `foe.GetCount(n)` | n 单位内敌人数 |
| `foe.hp` / `foe.maxhp` | 当前/最大生命 |
| `foe.armor` / `foe.maxarmor` | 护甲 |
| `foe.state` | 动画状态编号（闪避调试用） |
| `foe.time` | 当前 state 已过帧数 |
| `foe.level` | 敌人等级 |
| `foe.damage` | 单次攻击伤害 |
| `foe.buffs.*` / `foe.debuffs.*` | count, string, GetCount(str), GetTime(str) |

## 玩家生命与状态

| 表达式 | 说明 |
|--------|------|
| `hp` / `maxhp` | 当前/最大生命 |
| `armor` / `armor.f` | 护甲整数/小数部分 |
| `maxarmor` | 最大护甲 |
| `buffs.*` / `debuffs.*` | 同 foe，作用于玩家 |
| `buffs.oldest` / `debuffs.oldest` | 最旧 buff/debuff ID |

## 装备 item

| 表达式 | 说明 |
|--------|------|
| `item.left` / `item.right` | 左右手装备名 |
| `item.left.id` / `item.right.id` | 装备 ID |
| `item.left.gp` / `item.right.gp` | gear power |
| `item.left.state` / `item.right.state` | 武器状态（2=cast, 3=perf, 4=cd） |
| `item.left.time` / `item.right.time` | 当前 state 帧数 |
| `item.potion` | 当前药水（含 `auto`） |

## 拾取与采集

| 表达式 | 说明 |
|--------|------|
| `pickup` / `pickup.distance` / `pickup.z` | 目标拾取物 |
| `harvest` / `harvest.distance` / `harvest.z` | 可采集物（树、岩石等） |

## AI 与移动

| 表达式 | 说明 |
|--------|------|
| `ai.enabled` / `ai.paused` / `ai.idle` / `ai.walking` | AI 状态 |
| `pos.x` / `pos.y` / `pos.z` | 玩家坐标 |
| `player.direction` | 朝向（1=右, -1=左） |
| `player.framesPerMove` | 移动一步所需帧数 |
| `player.moveX` / `player.moveZ` | 移动速度 |
| `player.moveAddX` / `player.moveAddZ` | 累积移动加成 |
| `player.name` | 玩家名 |

## 资源

`res.stone`, `res.wood`, `res.tar`, `res.ki`, `res.bronze`, `res.crystals`

## 屏幕与时间

| 表达式 | 说明 |
|--------|------|
| `screen.i` / `screen.x` / `screen.w` / `screen.h` | 屏幕索引/位置/宽高 |
| `time` | 当前地点帧号 |
| `totaltime` | 含 BOSS 子区域的累积帧号 |
| `time.year` … `time.second` | 本地系统时间 |
| `utc.*` | UTC 时间 |
| `time.msbn` | Unix 毫秒（BigNumber） |

## 召唤 summon

| 表达式 | 说明 |
|--------|------|
| `summon.count` | 召唤物数量 |
| `summon.GetId(i)` | 召唤物 ID |
| `summon.GetName(i)` | 名称 |
| `summon.GetState(i)` / `summon.GetTime(i)` | 状态/帧数 |
| `summon.GetVar(name, i)` | 自定义变量 |

## 其他

| 表达式 | 说明 |
|--------|------|
| `encounter.isElite` / `encounter.eliteMod` | 精英遭遇 |
| `input.x` / `input.y` | 鼠标/触摸 ASCII 网格坐标 |
| `key` | 自定义输入，见 [custom-input.md](custom-input.md) |
| `rng` / `rngf` | 随机整数 0–9999 / 随机浮点 0–1 |
| `totalgp` | 背包总 gear power |
| `bighead` / `face` | 大头模式 / 表情 |
| `player.GetNextLegendName()` | 下一未完成 Legend |
