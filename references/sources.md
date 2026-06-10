# Stonescript 参考资料

本仓库知识库基于以下来源整理。在线版本为权威原文；本地快照供离线查阅。

## 官方资源

| 资源 | URL | 用途 | 本地镜像 |
|------|-----|------|----------|
| Introduction（心智石入门教程） | https://stonestoryrpg.com/stonescript/ | 零基础入门、Deadwood 自动化示例 | — |
| Manual（完整参考手册） | https://stonestoryrpg.com/stonescript/manual.html | 全部语法、game state、命令、原生函数、附录 | [manual-v4.27.1.html](snapshots/manual-v4.27.1.html) |
| Beta / Release notes / FAQ | https://stonestoryrpg.com/stonescript/ | 版本变更、测试功能 | — |

**Manual 版本**：v4.27.1（2026/01/15）

## Wiki（社区文档）

| 资源 | URL | 用途 |
|------|-----|------|
| Stonescript 概述 | https://stonestoryrpg.miraheze.org/wiki/Stonescript | 用途说明、官方示例脚本 |
| Guide:Stonescript | https://stonestoryrpg.miraheze.org/wiki/Guide:Stonescript | 分主题进阶指南索引 |
| Community Scripts | https://stonestoryrpg.miraheze.org/wiki/Community_Scripts | 内置 `import` 脚本分类列表 |

### Wiki 子指南（Guide 索引）

- [Basics](https://stonestoryrpg.miraheze.org/wiki/Guide:Stonescript/Basics)
- [Variables](https://stonestoryrpg.miraheze.org/wiki/Guide:Stonescript/Variables)
- [Game State](https://stonestoryrpg.miraheze.org/wiki/Guide:Stonescript/Game_State)
- [Commands](https://stonestoryrpg.miraheze.org/wiki/Guide:Stonescript/Commands)
- [Abilities](https://stonestoryrpg.miraheze.org/wiki/Guide:Stonescript/Abilities)
- [Player Actions](https://stonestoryrpg.miraheze.org/wiki/Guide:Stonescript/Player_Actions)
- [Functions](https://stonestoryrpg.miraheze.org/wiki/Guide:Stonescript/Functions)
- [Prints](https://stonestoryrpg.miraheze.org/wiki/Guide:Stonescript/Prints)

## 社区

- [Stone Story RPG Discord](https://discord.gg/stonestory) — 脚本协作与求助（官方教程推荐）

## 本仓库映射

| 需求 | 先查本仓库 | 不足时查 |
|------|-----------|----------|
| 快速查 API | `db/index.json` → 对应 JSON | Manual 快照 |
| 理解模式/踩坑 | `docs/patterns/` | Introduction |
| 完整 UI/附录 | `db/appendix-index.json` | Manual 在线/快照 |
| 社区 import | `db/imports.json` | Community Scripts Wiki |
