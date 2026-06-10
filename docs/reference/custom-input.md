# Custom Input

通过 `?key` 读取玩家输入，可驱动小游戏或 AI 模式切换。

## 示例（移动 @ 符号）

```stonescript
var x = 0
var y = 0
?key = leftBegin
  x--
  ?x < 0
    x = 0
?key = rightBegin
  x++
```

## 按键代码

| 持续按住 | 按下 | 释放 | 默认 PC |
|----------|------|------|---------|
| `left` | `leftBegin` | `leftEnd` | A / ← |
| `right` | `rightBegin` | `rightEnd` | D / → |
| `up` | `upBegin` | `upEnd` | W / ↑ |
| `down` | `downBegin` | `downEnd` | S / ↓ |
| `primary` | `primaryBegin` | `primaryEnd` | LMB / Enter |
| `back` | `backBegin` | `backEnd` | X |
| `ability1` | `ability1Begin` | `ability1End` | Shift |
| `ability2` | `ability2Begin` | `ability2End` | Control |
| `bumpL` | `bumpLBegin` | `bumpLEnd` | Z |
| `bumpR` | `bumpRBegin` | `bumpREnd` | C |

调试：`>@key@`
