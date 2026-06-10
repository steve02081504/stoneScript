# Loops 与 Arrays

## for 循环

```stonescript
for i = 1..5
  >`0,@i@,i = @i@
```

- 迭代变量 `v` 勿提前 `var` 声明
- 支持反向：`for k = 5..-2`
- 提前退出：将迭代变量设为范围外，或用 `break` / `continue`
- 遍历数组：`for value : a`

## 数组操作

| 操作 | 说明 |
|------|------|
| `a = []` | 新建空数组 |
| `a[i]` | 读/写元素（0-based） |
| `a.Add(v)` | 末尾添加 |
| `a.Clear()` | 清空（比每帧 `= []` 更高效） |
| `a.Contains(v)` | 是否包含 |
| `a.Count()` | 元素数 |
| `a.Emplace(i, v)` | 替换位置 i |
| `a.IndexOf(v)` | 首次出现索引，无则 -1 |
| `a.Insert(i, v)` | 插入 |
| `a.RemoveAt(i)` | 移除并返回 |
| `a.Sort()` | 升序排序 |

## 初始化示例

```stonescript
var magicNumbers = [10, 3, 0, 15, -7]
var someStrings = ["apple", "banana", "cherry"]
var multiDimensional = [[], [], []]
var objectCollection = [new Components/Vector, new Components/Vector]
```

## 循环重置建议

```stonescript
var clearedEachLoop = []
?loc.begin | loc.loop
  clearedEachLoop.Clear()
```

## import 机制补充

外部脚本放在 `(存档)/Stonescript/*.txt`：

- `import Rocky` — 单例，变量隔离
- `new Components/Vector` — 独立副本，体只执行一次
- 子文件夹：`import Games/Blackjack`

详见 [getting-started.md](../getting-started.md)。
