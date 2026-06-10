# 入门：心智石与 Stonescript

## 模块化源码 → 单文件部署

| 路径 | 用途 |
|------|------|
| [`scripts/user/src/`](../scripts/user/src/) | 模块化源码 |
| [`scripts/user/build.py`](../scripts/user/build.py) | 拼接 + 压缩 → `main.txt` |
| [`scripts/user/main.txt`](../scripts/user/main.txt) | 构建产物（粘贴到心智石） |

工作流：

1. 编辑 `src/` 下模块（开关写在 [`toggles.txt`](../scripts/user/src/toggles.txt)）
2. `python scripts/user/build.py`
3. 全选复制 `main.txt` → 心智石粘贴 → 保存重载

模块边界与 Facade API 见 [patterns/modules.md](patterns/modules.md)；组织原则见 [patterns/universal-script.md](patterns/universal-script.md)。

构建选项：

```bash
python scripts/user/build.py          # 默认：压缩后写入 main.txt
python scripts/user/build.py --dev    # 不压缩，便于 diff
python scripts/user/build.py --lint   # 检查 import/export 边界
python scripts/user/build.py --check  # 校验 main.txt 是否与源码一致
```

## 什么是 Stonescript

Stone Story RPG 心智石脚本语言，**每帧执行一次**（30 fps）。地点中按 **M** 打开心智石修改，关闭后重载；Power 按钮开关执行。

## 变量生命周期

- `var` 只在首次执行时初始化
- 离开地点手动重新开始会重置
- **Ouroboros 循环**与开关心智石**不重置**变量
- 每轮重置：`?loc.begin` 或 `?loc.loop`

## 装备覆盖

同一帧多个 `equip`，**最后一条生效**。用 `:` / `:?` 组织分支，见 [patterns/overwriting.md](patterns/overwriting.md)。

## PC 扩展（可选）

PC 版可将外部脚本放在存档 `Stonescript/*.txt`，用 `import Script` / `new Script` 引用；导入脚本变量与主脚本隔离。手机版不依赖此机制。

## 下一步

- [syntax.md](syntax.md) — 控制流与缩进
- [patterns/modules.md](patterns/modules.md) — 模块 Facade 与 loop 编排
- [debugging.md](debugging.md) — 排错
