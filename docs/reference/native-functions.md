# Native Functions 摘要

按主题分组。完整签名见 Manual 与 [db/native-functions.json](../../db/native-functions.json)。

## item.*

| 函数 | 返回 | 说明 |
|------|------|------|
| `item.CanActivate()` | bool | 全局可否激活能力 |
| `item.CanActivate(str)` | bool | 特定武器可否激活（须已装备） |
| `item.GetCooldown(str)` | int | 剩余冷却帧；无效 ID 返回 -1 |

## string.*

| 函数 | 说明 |
|------|------|
| `string.Size(str)` | 字符串长度 |
| `string.Contains(a, b)` | 是否包含 |
| `string.Replace(s, old, new)` | 替换 |
| `string.Split(s, sep)` | 分割为数组 |
| `string.ToLower` / `ToUpper` | 大小写 |

## math.*

| 函数 | 说明 |
|------|------|
| `math.BigNumber(n)` | 大数对象 |
| `math.Min` / `math.Max` | 最值 |
| `math.Abs` | 绝对值 |
| `math.Floor` / `math.Ceil` | 取整 |

BigNumber 方法：`Add`, `Sub`, `Mul`, `Div`, `Eq`, `Compare` 等。

## music.*

| 函数 | 说明 |
|------|------|
| `music.Play(track)` | 播放音乐 |
| `music.Stop()` | 停止 |

曲目列表见 [db/appendix-index.json](../../db/appendix-index.json) `music`。

## ambient.*

| 函数 | 说明 |
|------|------|
| `ambient` | 当前环境层 ID 列表（逗号分隔） |
| `ambient.Add(id)` | 添加环境层（最多 4 层） |
| `ambient.Stop()` | 清除所有层 |

环境 ID 见 appendix `ambient`。

## color.*

| 函数 | 说明 |
|------|------|
| `color.Random()` | 随机颜色 |
| `color.Lerp(a, b, t)` | 插值 |

## file.*

| 函数 | 说明 |
|------|------|
| `file.Exists(path)` | 文件是否存在 |
| `file.Read(path)` | 读取文本 |
| `file.Write(path, content)` | 写入 |

路径相对于存档 `Stonescript/`。

## sys.*

| 函数 | 说明 |
|------|------|
| `sys.SetFileUrl(url)` | 更改 import 源（仅心智石）；`local`/`remote`/URL |

## 其他常用

- `screen.w` / `screen.h` — 屏幕 ASCII 网格尺寸
- `summon.GetId()` 等 — 见 [game-state.md](game-state.md)
- `player.name` — 玩家名

## 附录索引

音效、音乐、环境、冷却 ID 等长尾列表不全文复制，查：

- [db/appendix-index.json](../../db/appendix-index.json)
- [references/snapshots/manual-v4.27.1.html](../../references/snapshots/manual-v4.27.1.html)
