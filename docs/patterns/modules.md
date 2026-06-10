# 模块边界与 Facade API

手机版 Stonescript 无法用户 `import`，[`scripts/user/src/`](../../scripts/user/src/) 通过 [`index.txt`](../../scripts/user/src/index.txt) 的 import 图拼接为单一 `main.txt`。模块化靠 **分层 + 命名 Facade + 薄编排 loop**。

## 分层

| 层 | 路径 | 职责 |
|----|------|------|
| 入口 | `index.txt`（`#role entry`，`#row`） | 心智石序言 + `import toggles` / `loop` |
| L0 配置 | `toggles.txt`（`#role wiring`）、`constants/*` | 开关与分域常量 |
| L0 工具 | `utils/*`（`#layer util`） | 距离 / hp / 物品 / buff |
| L1 业务 | `bestiary`、`harvest`、`mobility`、`potion/*`、`combat/*` | 各域逻辑 |
| L1 配线 | `aac.txt`（`#role wiring`） | 全局 AAC，loop 每帧最先调用 |
| L2 编排 | `loop.txt`（`#role orchestrator`） | **唯一**阶段调度者 |

`combat/equip.txt` 为战斗装备原语（`#bridge mobility`）；`combat/travel.txt` 为 dash / 换装原语。帧状态（`dedicatedCombatActive`、`combatMobilityEnabled`、`dashFreezeUntil` 等）在 `combat/state.txt`；冻结查询用 `utils/item` 的 `IsFrozen()`。

### combat 子包（`#layer orchestration` 内部）

| 模块 | 职责 |
|------|------|
| `combat/data` | 遭遇标签（`Combat_Is*`）、地点元素、debuff 查表 |
| `combat/state` | 地点/帧状态 var；`Combat_ResetLocState()` |
| `combat/routing` | `RunCombatFrame()`：定制 → smite 收刀 → 泛用链 |
| `combat/dedicated` | `TryDedicatedEncounter()`：炸弹车 / Acronian / Boss 分发与默认收尾 |
| `combat/generic` | 泛用怪换装与 `IsThinShellFoe()` |
| `combat/equip` | 装备原语（`EqMelee`、`EquipBashLeftHammer` 等） |
| `combat/travel` | dash / 旅行换装（`Travel_*`） |
| `combat/debuff` | debuff 剑轮换（`BossDebuffRotate` 等） |
| `combat/abilities/` | `GenericAbilities` / `BossAbilities` / smite / finisher |
| `combat/encounters/` | 具名 Boss 脚本；`common.txt` 提供 `Encounter_*` 片段 |

新具名 Boss：`encounters/<名>.txt` 导出 `Fight*()` → 在 `dedicated.txt` 的 `TryNamedBoss*` 中 import 并注册匹配条件。简单远距 Boss 可复用 `encounters/common.txt` 的 `Encounter_EquipDefaultRanged()`。

当前 `encounters/`：`acronian`、`bomb-cart`、`bolesh`、`ceiling`、`dysangelos`、`enoki`、`epic`、`guardian`、`hrimnir`、`morel`、`nagaraja`、`pallas`、`poena`、`puff`、`shroom`、`snail`、`xyloalgia`。

## 规则

1. **跨模块只调 export 符号**（或 L0 常量），禁止读取其它模块内部 private `var`。
2. **`loop.txt` 只 import**：根级 L1、`#role facade`、`#layer L0`（见下表）；不穿透 `encounters/*`、`abilities/*` 等 orchestration 子模块。
3. **常量**写在 `constants/distance|combat|harvest|potion|speedrun`；各 L1 模块 import 最小子集。
4. 新模块加入 import 链（通常由 `loop.txt` 或同包子模块 import）；开关写在 `toggles.txt`。
5. **同包私有可见**：`combat/*` 子模块互 import 时可调用对方 **private** 符号；跨包（如 `mobility` → `combat`）仅允许 **export/const**。
6. **combat 禁止** import `mobility`；mobility 经 `#bridge mobility` 访问 `combat/state`、`combat/travel`、`combat/equip`。**potion/use** 声明 `#bridge combat`，供 `combat/debuff` 等转发药水。
7. **竞速跳过图鉴/采集**由 `loop.txt` 读 `speedRun` 门控；`bestiary` / `harvest` 内部不再查竞速开关。

## 公开 API 一览

### AAC（`aac.txt`）

| 函数 | 说明 |
|------|------|
| `Aac_Run()` | 全局段顶解除 state=3 护甲阻塞（sight 手跳过） |

### 竞速（`toggles.txt` + `constants/speedrun.txt`）

| 符号 | 说明 |
|------|------|
| `speedRun`（toggle） | true = 不采集、不图鉴、超时自动 Leave |
| `useAutoPotion`（toggle） | loop 末尾是否 `RunAuto()` |
| `finisherWeapon` / `finisherCooldown` / `finisherLastHitOnly` | 终结技配置（见 `combat/abilities/finisher`） |
| `bestiaryReset` / `bestiaryDebug` | 图鉴 storage 重置与调试打印 |
| `SpeedRun_ShouldAutoLeave()` | loop 调用：超时自动 `loc.Leave()` |

### Bestiary

| 函数 | 说明 |
|------|------|
| `Bestiary_Init(isLocStart)` | 加载图鉴 storage；`bestiaryReset` 时 loc.begin 清空 |
| `Bestiary_RunPhase()` | 记录 + 扫描 |
| `Bestiary_NeedsChase()` | 是否需要追怪扫图 |
| `Bestiary_IsBlocking()` | 扫图中（阻塞战斗/移速/采集） |

### Harvest

| 函数 | 说明 |
|------|------|
| `Harvest_ShouldRun()` | 本帧是否优先采集 |
| `Harvest_Run()` | 执行采集 equip |

### Mobility

| 函数 | 说明 |
|------|------|
| `Mobility_RunCombatPhase()` | 战斗向移速 |
| `Mobility_RunPickupPhase()` | 拾取 star |
| `Mobility_RunTravelPhase()` | 无怪行走 |

跨域桥接：`combat/travel` 的 `Travel_*`；`combat/state` 的帧 flag；`combat/equip` 的 `EquipSpitDodge()` / `EquipTravelDefault()`。

### Combat（对 loop / mobility 可见的 Facade）

| 模块 | 主要 export |
|------|-------------|
| `combat/data` | `Combat_IsAcronianFight()`、`Combat_IsRockyDysangelosFight()`、`Combat_SkipsBardicheBurst()` 等 |
| `combat/state` | `Combat_ResetLocState()`、帧状态 var（`dedicatedCombatActive` 等） |
| `combat/routing` | `RunCombatFrame()` |
| `combat/dedicated` | `Combat_IsDedicatedEncounter()`、`TryDedicatedEncounter()` |
| `combat/generic` | `IsThinShellFoe()` |
| `combat/travel` | `Travel_RefreshTags()`、`Travel_Try*`、`Travel_SwapToTravelGear()` |
| `combat/equip` | `EquipSpitDodge()`、`EquipTravelDefault()` |

`combat/abilities/index`（包内）：`GenericAbilities()`、`BossAbilities()`、`CinderwispDevour()`。`combat/debuff` 由 `dedicated` 的 `RunBossEncounter` 与 `abilities` 调用，不直接暴露给 loop。

#### `RunCombatFrame` 单帧流水线（`routing.txt`）

1. `TryDedicatedEncounter(element)` — 炸弹车 / Acronian / Boss（含具名 `Fight*` 与默认收尾）
2. `dedicatedCombatActive` 仍为真 → 跳过泛用链
3. smite 收刀 → 旅行装
4. 泛用：`GenericAbilities` → 强制换装检查 → 施法等待 → 无怪旅行装 → `GenericEquip`

### Potion

| 模块 | 函数 | 说明 |
|------|------|------|
| `potion/brew` | `BrewAtLocStart()` | loc.begin 炼药 |
| `potion/use` | `TryCleansingPotion()`、`TryOffensePotion()`、`RunAuto()` | loop 末尾自动用药；combat 经 debuff 等转发 |

## loop 编排顺序

```
loc.begin: Combat_ResetLocState + BrewAtLocStart + Bestiary_Init
loc.loop:  Bestiary_Init(false)

每帧: Aac_Run → Loop_RefreshCombatFlags → Travel_RefreshTags
竞速超时 → loc.Leave()
图鉴(非 speedRun) → [远距] 追怪移速
采集(非 speedRun) → 战斗移速 → RunCombatFrame → 拾取移速 → 旅行移速
末尾: useAutoPotion → RunAuto()
```

`loop.txt` 直接 import：`toggles`、`aac`、`combat/data|state|routing|dedicated|generic|travel`、`potion/brew|use`、`bestiary`、`harvest`、`mobility`、`constants/speedrun`。

## 构建与 lint

```bash
python scripts/user/build.py          # 构建 main.txt
python scripts/user/build.py --lint   # 仅检查 import/export 边界
python scripts/user/build.py --check  # 与已提交 main.txt 比对（行为等价）
python scripts/user/build.py --dev    # 不压缩，便于 diff
```

`build.py --lint` 规则：

- 跨包：必须 import 且只能使用对方的 **export** 或 **const**。
- 同包（如 `combat/foo` import `combat/bar`）：可使用对方 **private** 符号。
- 拒绝未 import 的跨模块符号引用。
- **跨域 import**：`#layer L0` / `#layer util` 基础设施全局可达；其余跨域须在目标模块头声明 `#bridge <源域>`；跨域 import 不得触达 `#layer orchestration` 子图（含传递依赖）。
- **编排模块**（`#role orchestrator`，`loop.txt`）：仅可 import 根级 L1、`#role facade`、或 `#layer L0`；禁 `#layer util`、`#role barrel`、`#role entry`、其它 orchestrator。
- **配线模块**（`#role wiring`）：豁免跨域与 unused infra import 检查。
- **入口**（`#role entry`，`index.txt`）：豁免跨域检查。
- **门控模块**（`#gate <名>`，如 `constants/speedrun`）：仅 `#consumer <名>` 的 importer 可 import。
- orchestrator 与其直接 import 的 facade，其 `#layer L0`/`#layer util` import 须实际引用符号。

`#row` 模块（`index.txt`、`toggles.txt`）构建时不压缩标识符；其余模块见 [`scripts/README.md`](../../scripts/README.md)。
