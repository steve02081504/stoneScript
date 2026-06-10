# Minify 对照表

由 `python scripts/user/build.py` 自动生成。

## #row（不压缩）

| 原名 | 压缩名 |
|------|--------|
| `bestiaryDebug` | `bestiaryDebug` |
| `bestiaryReset` | `bestiaryReset` |
| `finisherCooldown` | `finisherCooldown` |
| `finisherLastHitOnly` | `finisherLastHitOnly` |
| `finisherWeapon` | `finisherWeapon` |
| `speedRun` | `speedRun` |
| `useAutoPotion` | `useAutoPotion` |

## const 策略

| 名称 | 策略 | 值 |
|------|------|-----|
| `avgTimeExitRatio` | `inline` | `1.15` |
| `bardicheMinHpArmorMultiplier` | `inline` | `6` |
| `bombCartMindDist` | `inline` | `7` |
| `bossDebuffAlwaysSkip` | `inline` | `[["chill", "yeti"]]` |
| `bossDebuffFullHpDotFoes` | `inline` | `["bolesh"]` |
| `bossDebuffFullHpFeebleFoes` | `inline` | `["pallas"]` |
| `bossDebuffFullHpFoes` | `inline` | `["poena", "guardian", "nagaraja"]` |
| `bossDebuffFullHpNonDotFeebleFoes` | `inline` | `["bolesh", "pallas"]` |
| `bossDebuffShroomFoes` | `inline` | `["bolesh", "morel", "yeti"]` |
| `bossDebuffThresholds` | `var` | `[["damage","morel",0.25],["damage","yeti",0.15],["damage","rocky",0],["chill","morel",0.1],["chill","rocky",0.1],["dot","morel",0.1],["dot","yeti",0.15],["dot","pallas",0.05],["dot","rocky",0.05],["feeble","shroom",0.15],["feeble","rocky",0.15]]` |
| `bossVampiricEquipDist` | `inline` | `8` |
| `brewResSurplusMin` | `inline` | `1500` |
| `cinderwispMinBestTimeSecs` | `inline` | `90` |
| `closeRangeMax` | `inline` | `10` |
| `counterCounters` | `inline` | `["poison", "vigor", "aether", "fire", "ice"]` |
| `counterElements` | `inline` | `["vigor", "aether", "fire", "ice", "poison"]` |
| `dashFreezeFrames` | `inline` | `60` |
| `dashRangeMax` | `inline` | `16` |
| `dashRangeMin` | `inline` | `11` |
| `debuffSwordRows` | `inline` | `[["damage","dP","damage"],["dot","dF","dot"],["chill","dI",""]]` |
| `defensiveHpMin` | `inline` | `5` |
| `devourBossCount` | `inline` | `10` |
| `devourFoeCount` | `inline` | `3` |
| `dysangelosBuffTable` | `var` | `[["aether","vigor"],["fire","aether"],["vigor","poison"],["poison","ice"],["ice","fire"]]` |
| `elementRingSize` | `inline` | `5` |
| `fastArmorShieldMax` | `inline` | `14` |
| `finisherLastHitHpSum` | `inline` | `10` |
| `finisherRangeMax` | `inline` | `7` |
| `fireTalismanMinDist` | `inline` | `16` |
| `foeArmorThreshold` | `inline` | `50` |
| `harvestFoeMinDist` | `inline` | `18` |
| `harvestSwingDist` | `inline` | `7` |
| `healPotionHpThreshold` | `inline` | `7` |
| `hpBerserkRatio` | `inline` | `0.6` |
| `hpBossEquipLowRatio` | `inline` | `0.8` |
| `hpCleansingRatio` | `inline` | `0.5` |
| `hpDefensiveRatio` | `inline` | `0.7` |
| `hpExperienceRatio` | `inline` | `0.8` |
| `hpInvisibilityRatio` | `inline` | `0.3` |
| `hpLuckyRatio` | `inline` | `0.5` |
| `hpRetreatRatio` | `inline` | `0.75` |
| `hpVampiricRatio` | `inline` | `0.85` |
| `hpWandSwitchRatio` | `inline` | `0.7` |
| `hrimnirShovelMaxDist` | `inline` | `7` |
| `hrimnirShovelMinDist` | `inline` | `2` |
| `midRangeMax` | `inline` | `17` |
| `midRangeMin` | `inline` | `11` |
| `mindTimeEq` | `inline` | `1` |
| `mindTimeGt` | `inline` | `2` |
| `mindTimeGte` | `inline` | `0` |
| `nagarajaSpitDodgeMinFrames` | `inline` | `6` |
| `nagarajaSpitLeadFrames` | `inline` | `25` |
| `ouroborosHpRatio` | `inline` | `0.6` |
| `pickPocketThreshold` | `inline` | `3` |
| `pickupMobilityMaxDist` | `inline` | `10` |
| `selfDamageMax` | `inline` | `7` |
| `sightScanDist` | `inline` | `22` |
| `smiteMinFoes` | `inline` | `6` |
| `smiteNormalMaxDist` | `inline` | `25` |
| `smiteTimeGateMax` | `inline` | `120` |
| `smiteTimeGateMin` | `inline` | `90` |
| `splashMinFoes` | `inline` | `3` |
| `strengthPotionArmorDist` | `inline` | `15` |
| `thinShellArmorMin` | `inline` | `100` |
| `vampiricHpMin` | `inline` | `5` |

## const（内联，无声明）

| 名称 | 内联值 |
|------|--------|
| `avgTimeExitRatio` | `1.15` |
| `bardicheMinHpArmorMultiplier` | `6` |
| `bombCartMindDist` | `7` |
| `bossDebuffAlwaysSkip` | `[["chill", "yeti"]]` |
| `bossDebuffFullHpDotFoes` | `["bolesh"]` |
| `bossDebuffFullHpFeebleFoes` | `["pallas"]` |
| `bossDebuffFullHpFoes` | `["poena", "guardian", "nagaraja"]` |
| `bossDebuffFullHpNonDotFeebleFoes` | `["bolesh", "pallas"]` |
| `bossDebuffShroomFoes` | `["bolesh", "morel", "yeti"]` |
| `bossVampiricEquipDist` | `8` |
| `brewResSurplusMin` | `1500` |
| `cinderwispMinBestTimeSecs` | `90` |
| `closeRangeMax` | `10` |
| `counterCounters` | `["poison", "vigor", "aether", "fire", "ice"]` |
| `counterElements` | `["vigor", "aether", "fire", "ice", "poison"]` |
| `dashFreezeFrames` | `60` |
| `dashRangeMax` | `16` |
| `dashRangeMin` | `11` |
| `debuffSwordRows` | `[["damage","dP","damage"],["dot","dF","dot"],["chill","dI",""]]` |
| `defensiveHpMin` | `5` |
| `devourBossCount` | `10` |
| `devourFoeCount` | `3` |
| `elementRingSize` | `5` |
| `fastArmorShieldMax` | `14` |
| `finisherLastHitHpSum` | `10` |
| `finisherRangeMax` | `7` |
| `fireTalismanMinDist` | `16` |
| `foeArmorThreshold` | `50` |
| `harvestFoeMinDist` | `18` |
| `harvestSwingDist` | `7` |
| `healPotionHpThreshold` | `7` |
| `hpBerserkRatio` | `0.6` |
| `hpBossEquipLowRatio` | `0.8` |
| `hpCleansingRatio` | `0.5` |
| `hpDefensiveRatio` | `0.7` |
| `hpExperienceRatio` | `0.8` |
| `hpInvisibilityRatio` | `0.3` |
| `hpLuckyRatio` | `0.5` |
| `hpRetreatRatio` | `0.75` |
| `hpVampiricRatio` | `0.85` |
| `hpWandSwitchRatio` | `0.7` |
| `hrimnirShovelMaxDist` | `7` |
| `hrimnirShovelMinDist` | `2` |
| `midRangeMax` | `17` |
| `midRangeMin` | `11` |
| `mindTimeEq` | `1` |
| `mindTimeGt` | `2` |
| `mindTimeGte` | `0` |
| `nagarajaSpitDodgeMinFrames` | `6` |
| `nagarajaSpitLeadFrames` | `25` |
| `ouroborosHpRatio` | `0.6` |
| `pickPocketThreshold` | `3` |
| `pickupMobilityMaxDist` | `10` |
| `selfDamageMax` | `7` |
| `sightScanDist` | `22` |
| `smiteMinFoes` | `6` |
| `smiteNormalMaxDist` | `25` |
| `smiteTimeGateMax` | `120` |
| `smiteTimeGateMin` | `90` |
| `splashMinFoes` | `3` |
| `strengthPotionArmorDist` | `15` |
| `thinShellArmorMin` | `100` |
| `vampiricHpMin` | `5` |

## const（提升为 var）

| 名称 | 初值 |
|------|------|
| `bossDebuffThresholds` | `[["damage","morel",0.25],["damage","yeti",0.15],["damage","rocky",0],["chill","morel",0.1],["chill","rocky",0.1],["dot","morel",0.1],["dot","yeti",0.15],["dot","pallas",0.05],["dot","rocky",0.05],["feeble","shroom",0.15],["feeble","rocky",0.15]]` |
| `dysangelosBuffTable` | `[["aether","vigor"],["fire","aether"],["vigor","poison"],["poison","ice"],["ice","fire"]]` |

## 全局函数 / 变量

| 原名 | 压缩名 |
|------|--------|
| `Aac_Run` | `fe` |
| `ActivateFeebleMask` | `br` |
| `ActivateSightHand` | `ca` |
| `bestiary` | `fb` |
| `Bestiary_Init` | `dr` |
| `Bestiary_RunPhase` | `cb` |
| `BestiaryContains` | `cm` |
| `BestiaryFoeKey` | `df` |
| `bestiaryKey` | `ej` |
| `BladeSmite` | `em` |
| `BossDebuffAlwaysSkip` | `au` |
| `BossDebuffRotate` | `cn` |
| `BossDebuffTagMatches` | `av` |
| `BossDebuffThreshold` | `be` |
| `bossDebuffThresholds` | `bd` |
| `BossSkipsDebuffAtFullHp` | `r` |
| `BrewAtLocStart` | `dg` |
| `BrewPotionType` | `dh` |
| `bronzeRes` | `ew` |
| `BuffCount` | `es` |
| `buffParts` | `ex` |
| `buffStrings` | `ek` |
| `CanBladeSmite` | `ds` |
| `CanEngage` | `et` |
| `CastR` | `fx` |
| `CdReady` | `ff` |
| `Combat_IsAcronianFight` | `ab` |
| `Combat_IsDedicatedEncounter` | `f` |
| `Combat_ResetLocState` | `aw` |
| `combatMobilityEnabled` | `ar` |
| `counter` | `fn` |
| `CounterElement` | `di` |
| `dashFreezeUntil` | `dd` |
| `DebuffBlockedByFoeState` | `s` |
| `DebuffSword` | `ec` |
| `DebugBestiary` | `dt` |
| `dedicatedCombatActive` | `as` |
| `diSword` | `fo` |
| `dpSword` | `fp` |
| `dysangelosBuffTable` | `bq` |
| `el` | `fz` |
| `element` | `fq` |
| `Encounter_EquipDefaultRanged` | `d` |
| `Encounter_TryCleansingIfDamagedAndLowHp` | `a` |
| `Encounter_TryCleansingIfHeavy` | `c` |
| `Encounter_TryStrengthIfReady` | `e` |
| `EqDI` | `fy` |
| `EqDpDi` | `fs` |
| `EqDual` | `ft` |
| `EqDualSh` | `ez` |
| `EqMelee` | `fg` |
| `EqMind` | `fu` |
| `EqStaff` | `fh` |
| `EquipBashLeftHammer` | `bf` |
| `EquipBashShield` | `cw` |
| `EquipBossFallback` | `cc` |
| `EquipBossFallbackWeapons` | `l` |
| `EquipCounterWandShield` | `ac` |
| `EquipForMagicResistFoe` | `ad` |
| `EquipForMagicVulnFoe` | `ax` |
| `EquipForPhysicalImmuneFoe` | `i` |
| `EquipForRangedImmuneFoe` | `t` |
| `EquipForThinShellFoe` | `ay` |
| `EquipHammerShield` | `cd` |
| `EquipHeavyHammer` | `co` |
| `EquipMagicVulnBonus` | `bg` |
| `EquipMindFreeze` | `cx` |
| `EquipSightHand` | `dj` |
| `EquipSpitDodge` | `dk` |
| `EquipVigorMeleeOrCrossbow` | `j` |
| `EquipWithDashFreeze` | `bh` |
| `EqXbow` | `fv` |
| `FastArmorShield` | `cy` |
| `FightAcronian` | `du` |
| `FightBolesh` | `ed` |
| `FightBombCart` | `dv` |
| `FightCeiling` | `dz` |
| `FightDysangelos` | `cz` |
| `FightDysangelosPhase1` | `ag` |
| `FightDysangelosPhase2` | `ah` |
| `FightDysangelosPhase3` | `aj` |
| `FightEpic` | `eu` |
| `FightGuardian` | `dw` |
| `FightHrimnir` | `ea` |
| `FightMorel` | `en` |
| `FightNagaraja` | `dx` |
| `FightPallas` | `ee` |
| `FightPoena` | `eo` |
| `FightShroom` | `ef` |
| `FightXyloalgia` | `dl` |
| `FoeBeyondCloseRange` | `bi` |
| `FoeBeyondMidRange` | `ce` |
| `FoeGone` | `fi` |
| `FoeHpArmorRatio` | `da` |
| `FoeInactive` | `eg` |
| `FoeInMeleeApproachRange` | `u` |
| `FoeIsOneOf` | `ep` |
| `foeKey` | `fw` |
| `FoeTimeMatches` | `dm` |
| `FoeWithinCloseRange` | `bj` |
| `GenericEquip` | `eb` |
| `GetHealingPotionByRes` | `ak` |
| `Harvest_Run` | `eh` |
| `Harvest_ShouldRun` | `cf` |
| `HpAbove` | `fj` |
| `HpBelow` | `fk` |
| `HpRatio` | `fl` |
| `IsBombCartEncounter` | `bk` |
| `IsFlyingFoe` | `ei` |
| `IsFrozen` | `fa` |
| `IsHandSightCasting` | `bs` |
| `IsHoldingTravelSwapWeapon` | `k` |
| `IsInSmiteTimeGateWindow` | `v` |
| `IsSightOnHand` | `dy` |
| `IsThinShellFoe` | `dn` |
| `IsWeaponCasting` | `db` |
| `LocElement` | `eq` |
| `Loop_InitOnLocBegin` | `bl` |
| `Loop_RefreshCombatFlags` | `w` |
| `mindFreezeUntil` | `de` |
| `Mobility_RunCombatPhase` | `x` |
| `Mobility_RunPickupPhase` | `y` |
| `Nagaraja_OnSpitWindup` | `al` |
| `Nagaraja_SyncQueuedSpitLand` | `g` |
| `Nagaraja_TrySpitDodge` | `am` |
| `nagarajaQueuedSpitLandAt` | `q` |
| `nagarajaSpitLandAt` | `bz` |
| `NeedsBestiaryScan` | `cg` |
| `OuroborosEquipOk` | `cp` |
| `Potion_HasOffenseOn` | `bm` |
| `RunAuto` | `fm` |
| `RunBossEncounter` | `cq` |
| `RunCombatFrame` | `do` |
| `RunCombatMobility` | `ch` |
| `RunGenericCombatPath` | `az` |
| `RunTravelIfSmiteSheathed` | `m` |
| `RunTravelMobility` | `ci` |
| `secsLeft` | `fc` |
| `sh` | `ga` |
| `ShouldAttemptCombatMobility` | `h` |
| `ShouldBladeSmite` | `cr` |
| `ShouldForceReequip` | `bt` |
| `ShouldSkipRanged` | `cs` |
| `SightHandJustScanned` | `ba` |
| `SkipBossDebuff` | `dp` |
| `SkipDebuff` | `er` |
| `stoneRes` | `fd` |
| `threshold` | `ey` |
| `Travel_RefreshTags` | `bu` |
| `Travel_SwapToTravelGear` | `z` |
| `Travel_TryDashToFoe` | `bn` |
| `Travel_TryForwardDash` | `an` |
| `Travel_TryStarMobility` | `ae` |
| `Travel_TryTravelMobility` | `n` |
| `travelNeedsWeaponSwap` | `at` |
| `travelSmiteSheath` | `cl` |
| `TryBestiaryScan` | `dc` |
| `TryBossBashOrDebuffSword` | `o` |
| `TryBossEngagePotions` | `bb` |
| `TryBossTraitEquip` | `cj` |
| `TryCleansingPotion` | `bv` |
| `TryDedicatedEncounter` | `ao` |
| `TryDefensivePotion` | `bw` |
| `TryEarlyCombatTravelSwap` | `p` |
| `TryEquipForFoeTraits` | `bc` |
| `TryExperiencePotion` | `bo` |
| `TryHarvestTool` | `dq` |
| `TryHealingPotion` | `ct` |
| `TryHeavyHammerActivate` | `af` |
| `TryInvisibilityPotion` | `ap` |
| `TryLogFoe` | `ev` |
| `TryLowHpMindRetreat` | `bp` |
| `TryNamedBossEncounter` | `aq` |
| `TryNamedBossFungus` | `bx` |
| `TryNamedBossMisc` | `cu` |
| `TryNamedBossSerpentAndGuardian` | `b` |
| `TryOffensePotion` | `cv` |
| `TryQuarterstaffActivate` | `aa` |
| `TrySightScanOnHand` | `by` |
| `TryVampiricPotion` | `ck` |
| `woodRes` | `fr` |

## 函数参数（各函数体内独立，短名可复用）

| 函数 | 压缩后函数名 | 参数原名 | 参数压缩名 |
|------|--------------|----------|------------|
| `CdReady` | `CdReady` | `cdKey` | `a` |
| `CastR` | `CastR` | `itemName` | `a` |
| `IsFrozen` | `IsFrozen` | `until` | `a` |
| `CanBladeSmite` | `CanBladeSmite` | `allowBoss` | `c` |
|  |  | `maxDist` | `b` |
|  |  | `minFoes` | `a` |
| `ShouldBladeSmite` | `ShouldBladeSmite` | `allowBoss` | `c` |
|  |  | `maxDist` | `b` |
|  |  | `minFoes` | `a` |
|  |  | `skipTimeGate` | `d` |
| `BladeSmite` | `BladeSmite` | `allowBoss` | `c` |
|  |  | `maxDist` | `b` |
|  |  | `minFoes` | `a` |
|  |  | `skipTimeGate` | `d` |
| `BuffCount` | `BuffCount` | `kind` | `a` |
|  |  | `src` | `b` |
| `HpBelow` | `HpBelow` | `ratio` | `a` |
| `HpAbove` | `HpAbove` | `ratio` | `a` |
| `EquipWithDashFreeze` | `EquipWithDashFreeze` | `itemName` | `a` |
| `EquipMindFreeze` | `EquipMindFreeze` | `setMindFreezeToo` | `a` |
| `EquipBashLeftHammer` | `EquipBashLeftHammer` | `element` | `a` |
| `EqMelee` | `EqMelee` | `element` | `a` |
| `EqXbow` | `EqXbow` | `element` | `a` |
| `EqStaff` | `EqStaff` | `element` | `a` |
| `EquipCounterWandShield` | `EquipCounterWandShield` | `element` | `a` |
| `EqDpDi` | `EqDpDi` | `element` | `a` |
| `EqDI` | `EqDI` | `element` | `a` |
| `EqDual` | `EqDual` | `element` | `a` |
| `EqDualSh` | `EqDualSh` | `element` | `a` |
| `FoeTimeMatches` | `FoeTimeMatches` | `minTime` | `a` |
|  |  | `timeMode` | `b` |
| `EqMind` | `EqMind` | `minTime` | `b` |
|  |  | `requireMindReady` | `d` |
|  |  | `setMindFreezeToo` | `e` |
|  |  | `state` | `a` |
|  |  | `timeMode` | `c` |
| `EquipHeavyHammer` | `EquipHeavyHammer` | `tryActivate` | `a` |
| `EquipMagicVulnBonus` | `EquipMagicVulnBonus` | `element` | `a` |
| `TryOffensePotion` | `TryOffensePotion` | `condition` | `b` |
|  |  | `potId` | `a` |
| `FoeIsOneOf` | `FoeIsOneOf` | `names` | `a` |
| `BossDebuffTagMatches` | `BossDebuffTagMatches` | `tag` | `a` |
| `BossDebuffThreshold` | `BossDebuffThreshold` | `kind` | `a` |
| `BossSkipsDebuffAtFullHp` | `BossSkipsDebuffAtFullHp` | `kind` | `a` |
| `SkipDebuff` | `SkipDebuff` | `kind` | `a` |
| `BossDebuffAlwaysSkip` | `BossDebuffAlwaysSkip` | `kind` | `a` |
| `SkipBossDebuff` | `SkipBossDebuff` | `kind` | `a` |
| `DebuffSword` | `DebuffSword` | `element` | `a` |
|  |  | `kind` | `b` |
|  |  | `skipIfFoeHasDebuff` | `d` |
|  |  | `swordPrefix` | `c` |
| `ActivateFeebleMask` | `ActivateFeebleMask` | `bossOnly` | `a` |
|  |  | `returnOnSuccess` | `b` |
| `BossDebuffRotate` | `BossDebuffRotate` | `element` | `a` |
| `EquipForMagicResistFoe` | `EquipForMagicResistFoe` | `element` | `a` |
| `EquipForPhysicalImmuneFoe` | `EquipForPhysicalImmuneFoe` | `element` | `a` |
| `EquipForMagicVulnFoe` | `EquipForMagicVulnFoe` | `element` | `a` |
| `EquipForRangedImmuneFoe` | `EquipForRangedImmuneFoe` | `allowOuroboros` | `b` |
|  |  | `element` | `a` |
| `TryEquipForFoeTraits` | `TryEquipForFoeTraits` | `allowOuroboros` | `b` |
|  |  | `element` | `a` |
| `EquipForThinShellFoe` | `EquipForThinShellFoe` | `element` | `a` |
| `GenericEquip` | `GenericEquip` | `element` | `a` |
| `FightAcronian` | `FightAcronian` | `element` | `a` |
| `Encounter_TryCleansingIfHeavy` | `Encounter_TryCleansingIfHeavy` | `threshold` | `a` |
| `Encounter_EquipDefaultRanged` | `Encounter_EquipDefaultRanged` | `element` | `a` |
| `FightBolesh` | `FightBolesh` | `element` | `a` |
| `FightCeiling` | `FightCeiling` | `element` | `a` |
| `FightEpic` | `FightEpic` | `element` | `a` |
| `FightEpic` | `FightEpic` | `element` | `a` |
| `FightHrimnir` | `FightHrimnir` | `element` | `a` |
| `FightMorel` | `FightMorel` | `element` | `a` |
| `FightNagaraja` | `FightNagaraja` | `element` | `a` |
| `FightPallas` | `FightPallas` | `element` | `a` |
| `FightPoena` | `FightPoena` | `element` | `a` |
| `FightEpic` | `FightEpic` | `element` | `a` |
| `FightShroom` | `FightShroom` | `element` | `a` |
| `FightEpic` | `FightEpic` | `element` | `a` |
| `FightXyloalgia` | `FightXyloalgia` | `element` | `a` |
| `TryDedicatedEncounter` | `TryDedicatedEncounter` | `element` | `a` |
| `TryBossTraitEquip` | `TryBossTraitEquip` | `element` | `a` |
| `TryBossBashOrDebuffSword` | `TryBossBashOrDebuffSword` | `element` | `a` |
| `EquipBossFallbackWeapons` | `EquipBossFallbackWeapons` | `element` | `a` |
| `EquipBossFallback` | `EquipBossFallback` | `element` | `a` |
| `TryNamedBossSerpentAndGuardian` | `TryNamedBossSerpentAndGuardian` | `element` | `a` |
| `TryNamedBossFungus` | `TryNamedBossFungus` | `element` | `a` |
| `TryNamedBossMisc` | `TryNamedBossMisc` | `element` | `a` |
| `TryNamedBossEncounter` | `TryNamedBossEncounter` | `element` | `a` |
| `RunBossEncounter` | `RunBossEncounter` | `element` | `a` |
| `RunGenericCombatPath` | `RunGenericCombatPath` | `element` | `a` |
| `BrewPotionType` | `BrewPotionType` | `potion` | `a` |
| `Bestiary_Init` | `Bestiary_Init` | `isLocStart` | `a` |
| `BestiaryContains` | `BestiaryContains` | `id` | `a` |
| `IsSightOnHand` | `IsSightOnHand` | `useRightHand` | `a` |
| `IsHandSightCasting` | `IsHandSightCasting` | `useRightHand` | `a` |
| `SightHandJustScanned` | `SightHandJustScanned` | `useRightHand` | `a` |
| `EquipSightHand` | `EquipSightHand` | `useRightHand` | `a` |
| `ActivateSightHand` | `ActivateSightHand` | `useRightHand` | `a` |
| `TrySightScanOnHand` | `TrySightScanOnHand` | `useRightHand` | `a` |
| `TryHarvestTool` | `TryHarvestTool` | `cdKey` | `b` |
|  |  | `useHatchet` | `a` |
