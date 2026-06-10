# Search Filters（搜索过滤器）

用于 `?foe`、`?loc`、`equip` 等处的匹配条件。

## 元素 / 种族

`poison`, `vigor`, `aether`, `fire`, `air`, `ice`, `arachnid`, `serpent`, `insect`, `machine`, `humanoid`, `elemental`

## 敌人特性

`boss`, `phase1`, `phase2`, `phase3`, `spawner`, `flying`, `slow`, `ranged`, `explode`, `swarm`, `unpushable`, `undamageable`, `magic_resist`, `magic_vulnerability`, `immune_to_stun`, `immune_to_ranged`, `immune_to_debuff_damage`, `immune_to_physical`

## 数值修饰

| 符号 | 含义 | 适用范围 |
|------|------|----------|
| `*N` | N 星 | 地点或物品 |
| `+N` | +N 附魔 | 仅物品 |

## 示例

```stonescript
?foe = insect | foe = poison
  loadout 3

equip hammer *7 D
equip vigor staff +13
```

## 减法条件

equip 字符串支持 `-criteria` 排除：

```stonescript
var weaponName = "poison sword *10 -big"
equipR @weaponName@
```

JSON 索引：[db/search-filters.json](../../db/search-filters.json)。
