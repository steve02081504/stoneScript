# 比较与逻辑运算符

用于 `?` 条件表达式中。

| 运算符 | 含义 | 示例 |
|--------|------|------|
| `=` | 相等；字符串表示包含 | `?hp = maxhp` |
| `!` | 不等；字符串表示不包含 | `?foe ! boss` |
| `&` | 逻辑与（AND） | `?loc=caves & foe=boss` |
| `\|` | 逻辑或（OR） | `?foe=slow \| foe.count>3` |
| `>` | 大于 | `?foe.distance > 8` |
| `<` | 小于 | `?hp < 7` |
| `>=` | 大于等于 | `?loc.stars >= 6` |
| `<=` | 小于等于 | `?hp <= 6` |

## 混合 `&` 与 `|`

在同一表达式中，**所有 `&` 先于 `|` 求值**。

```stonescript
?foe = boss & foe.distance <= 10 | item.right.state = 2
```

等价于 `(foe=boss AND distance<=10) OR (item.right.state=2)`。

## 续行 `^`

长条件用 `^` 拆行：

```stonescript
?foe = boss & ^foe.distance <= 10 & ^item.GetCooldown("bardiche") <= 0
  equip bardiche
  activate R
```

## 否定 `!`（布尔）

在布尔表达式前加 `!` 取反：

```stonescript
? !ai.enabled
  >AI is off
```

## 相关

- Game state 字段：[reference/game-state.md](reference/game-state.md)
- 搜索过滤器：[reference/search-filters.md](reference/search-filters.md)
