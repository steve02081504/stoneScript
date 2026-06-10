# Variables 参考

## 声明

```stonescript
var myVar = 10
myVar = myVar + 5
```

`var` **仅在首次执行时初始化**。之后每帧可赋值但不会重新 var 初始化。

## 生命周期

| 事件 | 变量是否重置 |
|------|-------------|
| 离开地点，手动新 run | 是 |
| Ouroboros 循环 | **否** |
| 打开/关闭心智石 | **否** |

重置模式：

```stonescript
var i
?loc.begin
  i = 0

var loopCount = 0
?loc.loop
  loopCount++
```

## 字符串

可用引号，支持特殊符号与尾部空格：

```stonescript
var msg = a + " x " + b + " = " + (a * b)
```

## import 隔离

各 `import` / `new` 脚本内变量**独立**，不会与其他脚本冲突。

## 数组

数组是特殊变量类型，见 [loops-arrays.md](loops-arrays.md)。
