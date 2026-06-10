# User Interface 概要

Stonescript 提供 Panel / Text / Button / Anim / Canvas 树形 UI。默认存在不可见 `ui.rootPanel`。

完整 API 见 Manual 第 16 节与快照 [references/snapshots/manual-v4.27.1.html](../../references/snapshots/manual-v4.27.1.html)。

## 基本流程

```stonescript
disable hud
ui.root.visible = true

?loc.begin
  var button = ui.AddButton()
  button.y = 1
  button.text = Press me
  button.SetPressed(OnPressed)

func OnPressed()
  >Hello World!
```

## ui 命名空间

| 函数 | 返回 | 说明 |
|------|------|------|
| `ui.AddPanel()` | Panel | 容器 |
| `ui.AddText()` / `ui.AddText(str)` | Text | 文本 |
| `ui.AddButton()` | Button | 按钮 |
| `ui.AddAnim(str)` | Anim | ASCII 动画 |
| `ui.AddCanvas()` | Canvas | 自由绘制 |
| `ui.AddStyle()` | int | 自定义样式 ID |
| `ui.Clear()` | — | 清空 root 子元素 |

## Component 通用属性

`x`, `y`, `w`, `h`, `anchor`, `dock`, `visible`, `parent`, `absoluteX/Y`, `Recycle()`

anchor/dock 值：`top_left`, `center_center`, `bottom_right` 等。

## 社区 UI import

常用：`import UI/MindstoneButton`, `UI/BossBar`, `UI/FoeStateTracker` 等。见 [db/imports.json](../../db/imports.json) category=UI。

## 性能提示

- 大段 ASCII 用 `ascii/asciiend` 块，避免 `\n` 换行符（昂贵）
- `panel.clip = true` 可裁剪子元素
