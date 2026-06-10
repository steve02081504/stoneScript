# 攻击动画取消（AAC）

通过故意**覆盖装备**跳过 state=3（performance）的剩余动画，提高攻速。伤害在 performance 开始时已结算。

## 通用模板（放脚本顶部）

```stonescript
?item.left.state = 3
  equipL stone throwing
  equipL @item.left@
?item.right.state = 3
  equipR shield *0*
  equip @item.right@
```

说明：

1. 检测左手/右手是否在 state=3
2. 用垃圾装备（stone throwing、0 星 shield）覆盖
3. 立即换回 `@item.left@` / `@item.right@`（覆盖前的武器）

AAC 与正常战斗 equip **共存**——战斗逻辑无需为 AAC 单独改武器名。

## 武器状态

| state | 含义 |
|-------|------|
| 3 | performance（已造成伤害，动画可跳过） |
| 4 | cooldown |

## 注意

- 这是**有意**使用 overwriting；与 [overwriting.md](overwriting.md) 中要避免的覆盖不同
- 垃圾装备勿用实战武器，避免误装备

## 相关

- Game state `item.left.state`：[reference/game-state.md](../reference/game-state.md)
