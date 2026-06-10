# Math Operations

| 运算符 | 含义 |
|--------|------|
| `+` | 加（数字或字符串拼接） |
| `-` | 减 |
| `*` | 乘 |
| `/` | 除（整数向下取整） |
| `++` / `--` | 自增/自减 |
| `%` | 取模 |
| `( )` | 优先级 |
| `!` | 布尔取反 |

## 示例

```stonescript
?hp < maxhp - 5
  equip vigor sword dL

?time % 300 = 0
  >Every 10 seconds

var n = min + rng % (max - min + 1)
```

可在 `?` 条件与变量赋值中直接使用。
