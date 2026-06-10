# 能力激活模式

本仓库实现位于 `combat/abilities/`：`index.txt`（`GenericAbilities` / `BossAbilities`）、`smite.txt`、`finisher.txt`。泛用链由 `combat/routing` 调用；Boss 链由 `combat/dedicated` 的 `RunBossEncounter` 调用。模块边界见 [modules.md](modules.md)。

## 基本结构

```stonescript
?条件
  equip 武器名
  activate R    // 或 L / P / potion
```

`activate` 参数：`potion`, `P`, `left`, `L`, `right`, `R`，或能力 ID。

## 冷却与可激活检查

```stonescript
?item.GetCooldown("quarterstaff") <= 0 & ^item.CanActivate()
  equip quarterstaff
  activate R
```

- `item.GetCooldown(str)` — 剩余冷却帧数；无效 ID 返回 -1
- `item.CanActivate()` — 全局是否允许激活
- `item.CanActivate(str)` — 特定武器是否可激活（须已装备）

冷却 ID 见 [db/appendix-index.json](../../db/appendix-index.json)。

## Quarterstaff 冲刺（简单瞬时能力）

```stonescript
?foe.distance > 17 & ^item.GetCooldown("quarterstaff") <= 0 & ^item.CanActivate()
  equip quarterstaff
  activate R
```

## Bardiche（有施法时间）

施法期间换装备会取消能力并进入冷却。须保持装备并在施法中继续 `activate R`：

```stonescript
?foe = boss & ^foe.distance <= 10 & ^item.GetCooldown("bardiche") <= 0 & ^item.CanActivate()
  | ^item.right = bardiche & ^item.right.state = 2
  equip bardiche
  activate R
```

- `item.right.state = 2` 表示 cast（施法）状态
- `\|` 表示：可激活 **或** 已在施法中

配合 [overwriting.md](overwriting.md) 的 `: / :?` 避免被其他 equip 打断。

## 毒剑 BOSS 减伤

```stonescript
?foe = boss & foe.debuffs.count = 0
  equipR sword dP
```

检查 debuff 数量避免重复上毒。

## 武器状态

| state | 含义 |
|-------|------|
| 2 | cast（施法） |
| 3 | performance（攻击判定） |
| 4 | cooldown |

## 相关

- `item.*` 原生函数：[reference/native-functions.md](../reference/native-functions.md)
- 调试 foe 动画：[debugging.md](../debugging.md)
