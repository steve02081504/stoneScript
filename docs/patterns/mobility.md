# 移速与拾取优化

## 星石（拾取）

```stonescript
?pickup.distance < 10
  equipL star
```

`pickup.distance` 为到当前目标拾取物的距离。星石吸拾取并大幅加速移动。

## 衔尾蛇（远程回血）

```stonescript
?foe ! boss & foe.distance > 8
  equipL ouroboros
```

- 距离 **8**：衔尾蛇会参与战斗（近战时仍用剑）
- 距离 **17**：完全排除战斗（衔尾蛇攻击范围 17），循环更快

## 冲刺盾

```stonescript
?foe.distance >= 11 & foe.distance <= 16
  equipR dashing
```

在特定距离装备触发冲刺。

## 三叉戟

```stonescript
?foe.distance > 10
  equipR shield
  equipL triskelion
```

常与星石、else-if 链组合，见 [overwriting.md](overwriting.md)。

## 伐木

```stonescript
?harvest.distance < 10
  equip hatchet
```

## Deadwood 完整组合

见 [scripts/examples/deadwood.txt](../../scripts/examples/deadwood.txt)。

## 相关

- `pickup.distance`、`harvest.distance`：[reference/game-state.md](../reference/game-state.md)
