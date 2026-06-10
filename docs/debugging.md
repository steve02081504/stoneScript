# 调试 Stonescript

## 游戏内工具

| 操作 | 作用 |
|------|------|
| **Tab**（按住） | 显示 game state 信息与最近 Stonescript **错误列表** |
| **M** | 地点中打开心智石，修改后关闭即重载脚本 |
| Power 按钮 | 开关心智石脚本执行 |

排错时优先看 Tab 下的错误信息。

## 打印调试

### 屏幕左上角

```stonescript
>Hello World!
>HP = @hp@, foe = @foe.name@
```

### 固定坐标（屏幕左上角为原点）

```stonescript
>`0,1,Foe state: @foe.state@, time: @foe.time@
```

### 相对玩家

```stonescript
>o-6,3,#red,Let's go!
```

### 相对敌人头部（闪避调试）

```stonescript
>Foe state: @foe.state@, foe time: @foe.time@
```

观察 BOSS 攻击动画的 `foe.state` 与 `foe.time`，在精确帧装备心智石闪避：

```stonescript
?foe = boss
  ?foe.state = 32 & foe.time = 40
    equipL mind
```

## 常见异常原因

### 能力被打断

同一帧内后面的 `equip` 覆盖了正在施法的武器。用 `:` / `:?` 分支，或在施法中检查 `item.right.state = 2`。见 [patterns/overwriting.md](patterns/overwriting.md)、[patterns/abilities.md](patterns/abilities.md)。

### 变量「不归零」

变量在 Ouroboros 循环间保持。计数器异常时检查是否应在 `?loc.begin` 或 `?loc.loop` 重置。

### import 报错

- 仅使用**内置**社区 import（如 `import UI/MindstoneButton`），写在 [`index.txt`](../scripts/user/src/index.txt) 序言（`import toggles` 之前）
- **不要**写用户自建 import（`import shared/...`）——手机版无法加载外部文件
- PC 外部文件 import 见 [getting-started.md](getting-started.md) PC 扩展节

### 冷却 ID 错误

`item.GetCooldown("xxx")` 无效 ID 返回 **-1**。查 [db/appendix-index.json](../db/appendix-index.json) 的 `cooldownIds`。

## 工作流

编辑 `scripts/user/src/` → `python scripts/user/build.py` → 复制 `main.txt` 到心智石 → Tab 看错误 → 用 `>` 验证条件。部署步骤见 [getting-started.md](getting-started.md)。
