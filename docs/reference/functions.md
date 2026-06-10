# Functions 参考

## 声明与调用

```stonescript
func Print(message)
  >@message@

Print(Hello World!)
```

声明时不执行；调用时执行函数体。

## 返回值

```stonescript
func NonBossDuration()
  return totalTime - time

var duration = NonBossDuration()
```

## 参数

```stonescript
func RandomRange(min, max)
  ?min >= max
    return min
  return min + rng % (max - min + 1)
```

## this 前缀

函数参数与脚本级变量同名时用 `this.`：

```stonescript
var a = 1
func TestScope(a)
  >Script=@this.a@, func=@a@
```

## 栈限制

调用栈上限 **215**，超限抛错。避免无限递归。

## 外部脚本函数

import 的脚本可导出函数供主脚本调用：

```stonescript
var print = import PrintUtil
print.LowerLeft(0, -1, #ffffff, "Health: " + hp)
```

可实现 `ToString()` 供 `@obj@` 打印。
