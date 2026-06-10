# 装备覆盖（Overwriting）

## 问题

脚本每帧从上到下执行。若先 `equip crossbow`，再在 BOSS 条件下 `equip bardiche`，下一帧又会先执行 `equip crossbow`，**覆盖** Bardiche，导致施法被打断。

## 症状

- Bardiche / 其他有施法时间的武器能力无法完成
- 武器「闪一下」就换回默认装备

## 解法：else 分支 `: ` 与 else-if `:?`

把互斥的 equip 放进同一棵 `?` 树，用 `:` / `:?` 保证每帧只走一条分支。

### 错误示例

```stonescript
equip heavy crossbow
?foe = boss
  equipL sword
  equipR hammer
?foe.distance <= 10 & item.GetCooldown("bardiche") <= 0
  equip bardiche
  activate R
```

### 正确示例

```stonescript
?foe = boss
  ?foe.distance <= 10 & ^item.GetCooldown("bardiche") <= 0 & ^item.CanActivate()
    | ^item.right = bardiche & ^item.right.state = 2
    equip bardiche
    activate R
  :
    equipL sword
    equipR hammer
: equip heavy crossbow
```

## else-if 链（拾取优先）

```stonescript
?pickup.distance < 10
  equipL star
:?foe.distance > 10
  equipR shield
  equipL triskelion
:?foe = boss
  equip ice crossbow
: equipR shield
  equipL ice wand
```

靠前的条件满足时，**跳过后续**所有 `:?` 与 `:`。

## 何时故意覆盖

攻击动画取消（AAC）**故意**用垃圾装备覆盖 state=3 的武器以跳过动画。见 [aac.md](aac.md)。

## 相关

- [abilities.md](abilities.md) — 施法状态保持
- [syntax.md](../syntax.md) — `: / :?` 缩进规则
