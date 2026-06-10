# 基础语法

## 控制流符号

| 符号 | 含义 | 示例 |
|------|------|------|
| `?` | if：条件为真时执行缩进子行 | `?hp < 7`<br>`  activate potion` |
| `:` | else：与上方 `?` 同级缩进，条件为假时执行 | `?loc = caves`<br>`  loadout 1`<br>`: loadout 2` |
| `:?` | else-if | `?loc = caves`<br>`  loadout 1`<br>`:?loc = deadwood`<br>`  loadout 2`<br>`: loadout 3` |
| `^` | 续行（合并到上一行） | `?loc=caves \|`<br>`^loc = mine equip repeating` |
| `//` | 行注释 | `?loc = caves loadout 1 // Caves` |
| `/* */` | 块注释 | `/* 整段忽略 */` |

## 缩进与作用域

**行首空格决定归属。** 子指令必须比父级 `?` 多缩进（通常 2 个空格）。

```stonescript
?loc = deadwood
  ?hp < 7
    activate potion
  equipL sword
```

- `activate potion` 仅在 deadwood 且 hp<7 时执行
- `equipL sword` 在 deadwood 时总是尝试执行

`: ` 与 `:?` 的缩进层级与对应的 `?` **相同**，不是子行。

## 执行顺序

脚本**从上到下**每帧执行。靠后的 `equip` 会覆盖靠前的装备结果。

## 变量插值

在 `>` 打印或 equip 字符串变量时用 `@变量名@`：

```stonescript
var weaponName = "poison sword *10"
equipL @weaponName@
>HP = @hp@
```

## 字符串

字符串变量可用引号，支持特殊符号与尾部空格：

```stonescript
var msg = a + " x " + b
```

## 函数

```stonescript
func Greet(name)
  >Hello @name@

Greet(World)
```

- 函数声明时不立即执行
- 可用 `return` 返回值
- 可用 `this.` 区分脚本级变量与参数同名的情况
- 调用栈上限 215，超限报错

## 循环

```stonescript
for i = 1..5
  >i = @i@
```

详见 [reference/loops-arrays.md](reference/loops-arrays.md)。

## 相关

- 比较运算符：[comparisons.md](comparisons.md)
- 覆盖问题：[patterns/overwriting.md](patterns/overwriting.md)
