# ProtoHub-mada 产品团队操作指南

> 版本：v3.1（2026-07-08）| 原型方案重构：从独立 HTML 改为前端代码修改+预览；补充 PRD 方案确认后置入口
>
> Changelog：
> - v3.1（2026-07-08）：结合产品需求流程，明确原型设计在需求大纲确认、产品方案/流程图制定、研发版 PRD 确认之后启动；补充 Web 使用 Element UI、小程序使用 Vant 的组件库要求
> - v3.0（2026-06-24）：原型方案重构——不再生成独立演示 HTML，改为拉取生产前端代码 → 修改/编写 Vue 代码 → 构建预览；新增 Step 1 克隆前端仓库；gitnexus-hub 更新为正式环境 + multica skill 封装
> - v2.0（2026-06-22）：分层架构重构（L0/L1/L2）+ 业务术语映射表 + 10步线性工作流 + GATE/CHECKPOINT + 目录结构对齐 prd-writer 规范
> - v1.0（2026-06-04）：初始版本，平铺式结构

面向产品团队全员。无论使用什么智能体，读完这篇就能上手。

---

## 目录

- [L0. 核心原则](#l0-核心原则)
- [L1. 工作流（10步线性）](#l1-工作流10步线性)
- [L2. 规范层](#l2-规范层)
  - [§1 目录结构](#1-目录结构)
  - [§2 业务术语-仓库/页面映射表](#2-业务术语-仓库页面映射表)
  - [§3 新成员环境准备](#3-新成员环境准备每人一次)
  - [§4 不同工具操作对照](#4-不同工具操作对照)
  - [§5 提示词模板库](#5-提示词模板库)
  - [§6 设计规范](#6-设计规范)
  - [§7 常见问题](#7-常见问题)
  - [§8 分支管理与版本追踪](#8-分支管理与版本追踪)
  - [§9 代码定位指南](#9-代码定位指南)

---

## L0. 核心原则

> 无论哪个步骤，遇到疑惑时回来看这 10 条。

1. **前端代码驱动**：不再生成独立演示 HTML。通过拉取生产环境前端代码，直接修改或编写新的 Vue 代码，再用修改后的代码构建预览页面。原型即真实前端代码的修改版本。
2. **两阶段分离**：本地修改（拉取→扫描→改→预览）和确认推送（说"可以推了"才推）严格分离，不混在一起。改到满意再推，不怕反复改。
3. **拉取优先**：每次开始工作前必须先说「拉最新代码」，不拉不改，避免覆盖同事的改动。
4. **关联检查必须执行**：推送前必须查 `docs/data-flow-map.md` 确认改动影响，不可跳过。
5. **Commit 规范**：格式 `type(scope): 说明`，说明用中文 20 字以内，AI 自动生成，你确认即可。
6. **前端代码为准**：样式以生产环境前端 Vue 源码为准，不自行定义设计体系。现有页面匹配现有前端样式，新页面匹配同类型前端页面样式。
7. **先读后改**：AI 修改前端代码前必须先读目标文件，不凭空写，未变更区域保持原样。
8. **一次一模块**：一次会话只改一个页面/模块，改完立即推，不积压。
9. **数据流向映射同步**：新增或删除模块/页面后，必须同步更新 `docs/data-flow-map.md`。
10. **分支管理**：原型修改在 ProtoHub-mada 的功能分支上进行，不直接推 dev。功能分支只推到 ProtoHub-mada，不同步到前端开发仓库。
11. **PRD 确认后再做原型**：原型流程是产品需求流程的后置步骤。必须先完成需求大纲确认、产品方案与流程图制定、研发版 PRD 确认；仍在讨论方案或 PRD 时，不进入 Vue/HTML 原型修改。
12. **组件库对齐**：Web 管理后台使用 Element UI 组件形态，小程序使用 Vant 组件形态；若目标源码依赖或业务封装不同，以目标源码为准，但不得跨端套用组件形态。

---

## L1. 工作流（12步线性）

共 12 步，三个阶段：准备（0-1）→ 修改（2-4）→ 推送（5-10）。

> **v3.0 核心变化**：不再生成独立演示 HTML。改为拉取生产前端代码 → 修改 Vue 代码 → 构建预览 → 同步到 ProtoHub。

每步有 **GATE**（前置条件，不满足不能开始）和 **CHECKPOINT**（产出验证）。

| 步骤 | 做什么 | 产出 | GATE | CHECKPOINT |
|------|--------|------|------|------------|
| -1 | 原型设计前置确认 | `tmp/prototype_entry_check.md` | 需求大纲、产品方案、PRD 已确认 | 可进入原型设计 |
| 0 | 拉最新代码 + 创建功能分支 | `tmp/pull_status.md` | Step -1 完成；仓库已克隆、Token 有效 | pull 成功，功能分支已创建 |
| 0.5 | 遍历前端代码变更 | `tmp/code_changes.md` | Step 0 完成 | 变更摘要已写入，结构调整已识别 |
| 1 | 变更类型评估 | `tmp/change_plan.md` | Step 0.5 完成 | 类型已确定、影响范围已列 |
| 2 | 读取目标 Vue 文件 | — | Step 1 完成 | 文件内容已在上下文 |
| 3 | 修改/编写前端代码（Vue） | 修改后的 `.vue` 文件 | Step 2 完成 | 文件已写入磁盘 |
| 4 | 构建预览（npm run dev） | `tmp/preview_result.md` | Step 3 完成 | 用户确认满意 |
| 5 | 关联影响检查 | `tmp/impact_check.md` | Step 4 完成 | 关联页面已列举、用户已确认 |
| 6 | 推送前自审（6组） | `tmp/self_audit.md` | Step 5 完成 | 所有检查项通过 |
| 7 | 同步到 ProtoHub + diff + commit 预览 | `tmp/commit_preview.md` | Step 6 完成 | 快照已同步（含版本标记），用户确认 commit message |
| 8 | 推送功能分支 ⛔ | — | **Step 7 用户确认** | push 功能分支到 ProtoHub-mada 成功 |
| 9 | 评审通过后合并 dev + 更新映射表 | `docs/data-flow-map.md` | Step 8 完成、评审通过 | 合并到 dev，新文件/模块已补录 |
| 10 | 知识回流 | `docs/change-log.md` 追加 | Step 9 完成 | 变更记录已写入 |

> **⛔ Step 8 是唯一需要用户明确说「可以推了」才执行的步骤。** 推送的是功能分支（如 `protohub/order-refund`），不是直接推 dev。评审通过后才合并到 dev（Step 9）。

### Step -1 详解：原型设计前置确认

> **触发时机**：每次开始修改原型前，先执行；这一步属于产品需求流程与 ProtoHub 原型流程之间的交接。
>
> **目标**：确认当前不是在讨论大纲或方案，而是已经进入“把已确认方案可视化”的阶段。

**执行内容**：

1. 检查需求大纲是否已确认。
2. 检查产品方案、流程图/建模决策是否已确认；简单需求应确认已生成简化流程图。
3. 检查研发版 PRD 是否已按 6 个模块生成并确认。
4. 判断目标端：Web 管理后台、小程序，或多端。
5. 明确组件库：Web 使用 Element UI，小程序使用 Vant；若源码依赖不同，以源码为准。
6. 写入 `tmp/prototype_entry_check.md`。

```markdown
## 原型设计前置确认
- 需求大纲：已确认 / 未确认
- 产品方案与流程图：已确认 / 未确认 / 简化流程图
- 研发版 PRD：已确认 / 未确认
- 端类型：Web / 小程序 / 多端
- 组件库：Element UI / Vant / 以源码为准
- 结论：可进入原型设计 / 返回 PRD 流程
```

任一关键项未确认时，先返回产品需求流程补齐，不进入 Vue/HTML 原型修改。

### Step 0.5 详解：遍历前端代码变更

> **触发时机**：每次开始修改原型前，必须先执行。
>
> **目标**：把线上前端系统的真实改动同步到原型，防止原型和实际系统越走越远。

**执行内容**：

1. 通过 gitnexus-hub（multica skill 封装，约束了 MCP 调用层级）查询目标模块的最新代码变更（新增字段/枚举变更/页面结构调整）
2. 比对原型现有展示和线上代码，识别差异点
3. 写入 `tmp/code_changes.md`，格式如下：

```markdown
## 代码变更扫描结果 - {日期}

### 目标模块：{模块名}
### 扫描仓库：{后端仓库} / {前端仓库}

#### 发现的变更
| 变更类型 | 文件/枚举 | 具体变更 | 原型是否需要更新 |
|---------|---------|---------|----------------|
| 新增字段 | order_info.channel_label | 新增渠道标签字段 | ✅ 需要（订单列表新增标签列） |
| 枚举变更 | OrderStatusEnum | 新增 PARTIAL_RETURN 状态 | ✅ 需要（状态标签新增「部分还车」） |
| 结构调整 | views/auditList | 升级审批拆分为两个入口 | ✅ 需要（原型菜单新增入口） |
| 无变更   | car_info         | 字段无变化             | ➖ 不需要更新 |

#### 如有新结构 → 需同步更新
- data-flow-map.md：新枚举/新字段补录
- index.html：新页面加导航卡片
- team-guide.md §2：新页面路径补录映射表
```

**提示词**：

```
帮我扫描 {模块} 最近的前端代码变更，重点关注：
- 有没有新增字段或枚举值
- 有没有页面结构调整（新增/删除/重组）
- 原型现有展示和线上是否有偏差

结果写到 tmp/code_changes.md
```

### 完整流程图

```
┌──────────────────────────── 阶段零：代码扫描 ──────────────────────────────┐
│                                                                            │
│  Step 0   说「拉最新代码」                                                   │
│             │   ↳ git pull ProtoHub-mada dev（docs/映射表/共享资源）             │
│             │   ↳ git pull 前端仓库（mdscr-fe-admin 等）                     │
│             │   ↳ git checkout -b protohub/{模块}-{功能}  ← 创建功能分支      │
│             ▼ GATE: Token有效、仓库已克隆、功能分支已创建                    │
│  Step 0.5 AI 遍历前端代码变更                                                │
│             │   ↳ 通过 multica gitnexus-hub skill 查最新代码                 │
│             │   ↳ 比对原型和线上的差异                                       │
│             │   ↳ 写入 tmp/code_changes.md                                  │
│             │   ↳ 如有新结构 → 同步更新映射表/导航                           │
│             ▼ CHECKPOINT: tmp/code_changes.md 已写入                        │
│                                                                            │
├──────────────────────────── 阶段一：修改 ──────────────────────────────────┤
│                                                                            │
│  Step 1  AI 评估变更类型（迭代/新页面/全局样式/模块结构）                      │
│            │                                                               │
│            ▼ CHECKPOINT: tmp/change_plan.md 已写入                         │
│                                                                            │
│  Step 2  AI 读取目标 Vue 文件（先读后改）                                     │
│            │   ↳ 定位前端仓库中的 .vue 文件路径                              │
│            │   ↳ Read 目标文件 + 相关组件/路由                               │
│            │                                                               │
│  Step 3  AI 修改/编写前端代码（Vue）                                         │
│            │   ↳ 修改现有 .vue 组件 或 创建新 .vue 文件                      │
│            │   ↳ 融入 code_changes.md 中的变更                               │
│            │   ↳ 前端代码为准，Web 复用 Element UI，小程序复用 Vant             │
│            │                                                               │
│  Step 4  构建预览（npm run dev）→ 不满意? 回到 Step 3 继续改                 │
│            │   ↳ 在前端仓库目录启动 dev server                               │
│            │   ↳ 浏览器访问预览页面                                          │
│            │                                                               │
│            ▼ GATE: 你确认「满意」                                            │
│                                                                            │
├──────────────────────────── 阶段二：推送 ──────────────────────────────────┤
│                                                                            │
│  Step 5  关联影响检查（查 data-flow-map.md，必须执行）                        │
│            │                                                               │
│  Step 6  推送前自审（6 组检查清单，AI 自动执行）                               │
│            │                                                               │
│  Step 7  AI 同步修改到 ProtoHub + 展示 diff + 建议 commit message            │
│            │   ↳ 将修改的 Vue 文件复制到 ProtoHub-mada/modules/              │
│            │   ↳ 添加快照版本标记注释（Source Repo/Base Commit/Change 等）    │
│            │   ↳ 保留目录结构映射前端仓库                                    │
│            │   ↳ 你确认 commit message                                      │
│            │                                                               │
│  Step 8  ⛔ 你说「可以推了」→ AI 推送功能分支到 ProtoHub-mada                │
│            │   ↳ git push inner protohub/{模块}-{功能}                      │
│            │   ↳ ⚠️ 不推到前端开发仓库                                      │
│            │                                                               │
│  Step 9  评审通过后 → AI 合并功能分支到 dev + 更新 data-flow-map.md          │
│            │   ↳ git checkout dev && git merge protohub/{分支}              │
│            │   ↳ git push inner dev                                        │
│            │                                                               │
│  Step 10 知识回流：AI 追加变更记录到 docs/change-log.md                      │
│                                                                            │
└─────────────────────────── ✅ 全团队同步 ────────────────────────────────┘
```

### 实际对话示例

```
你：拉最新代码，扫描一下订单模块的前端代码变更

AI：已拉取 ProtoHub-mada（dev 最新提交 98e0508）和前端仓库 mdscr-fe-admin
    扫描 mdscr-order / mdscr-fe-admin 中...

    发现变更：
    ① OrderStatusEnum 新增 PARTIAL_RETURN（部分还车）状态
    ② order-list 工具栏已有「全部导出」按钮
    ③ 无结构性页面调整
    
    建议：订单列表状态标签需补充「部分还车」状态（灰色标签）
    已写入 tmp/code_changes.md

你：好，帮我把订单列表的状态标签加上「部分还车」灰色标签

AI：（定位前端仓库中 views/sale/order/orderList.vue）
    （读取目标 Vue 文件，找到状态标签渲染逻辑）
    已修改 orderList.vue，在状态枚举中新增 PARTIAL_RETURN 标签渲染。
    正在启动 dev server 预览...
    预览地址：http://localhost:5173/sale/order/orderList

你：（预览后）满意了，可以推了

AI：将修改同步到 ProtoHub-mada/modules/02-order/list/orderList.vue
    已添加快照版本标记（Source: mdscr-fe-admin dev@a1b2c3d）
    改动摘要：orderList.vue +8 -2
    建议 commit：feat(order-list): 状态标签新增「部分还车」(PARTIAL_RETURN)
    当前在功能分支 protohub/order-list 上
    确认推送中...已推送到 protohub/order-list 分支，commit: c9f2a1b
    评审通过后可合并到 dev

你：评审通过了，合并到 dev 吧

AI：已合并 protohub/order-list 到 dev，推送成功
    data-flow-map.md 无结构变化，无需更新
```

### 跨会话恢复

新会话先读 `tmp/code_changes.md`、`tmp/change_plan.md`、`tmp/impact_check.md` 恢复上下文，从中断步骤继续。

---

## L2. 规范层

### §1 目录结构

> 加载时机：新建页面、新增模块、接入新原型时
>
> **v3.0 变化**：`modules/` 下新增 `.vue` 文件（前端代码修改版），旧的 `.html` 文件保留为历史参考。`frontend-workspace/` 存放克隆的前端仓库（gitignored）。

```
ProtoHub-mada/                            # 本地路径: /Users/weigaopeng/WorkBuddy/2026-06-03-17-10-25/
│
├── index.html                            # 模块导航首页（浏览器入口）
│
├── frontend-workspace/                   # ⭐ 前端仓库工作区（gitignored，不提交）
│   ├── mdscr-fe-admin/                   #   克隆的 mdscr-fe-admin 仓库（用于修改+预览）
│   ├── mdscr-fe-store-wx/                #   克隆的 mdscr-fe-store-wx 仓库
│   └── ...                               #   其他前端仓库按需克隆
│
├── modules/                              # 业务模块（前端代码修改版 + 历史 HTML）
│   ├── 00-login/                         # 登录
│   │   └── login.vue                     #   ⭐ v3.0 新格式：Vue 组件修改版
│   ├── 01-dashboard/                     # 工作台
│   │   ├── overview/
│   │   │   └── dashboard-overview.vue    #   运营工作台
│   │   └── store/
│   │       └── dashboard-store.vue       #   门店工作台
│   ├── 02-order/                         # 订单管理 ⚡ 核心模块
│   │   ├── list/orderList.vue            #   订单列表（对应 views/sale/order/orderList.vue）
│   │   ├── pickup/orderPickup.vue        #   订单取车
│   │   ├── return/orderReturn.vue        #   订单还车
│   │   ├── refund/orderRefund.vue        #   订单退款
│   │   └── reserve/orderReserve.vue      #   短期预留
│   ├── 03-vehicle/                       # 车辆管理
│   │   ├── list/vehicleList.vue          #   车辆列表
│   │   ├── detail/vehicleDetail.vue      #   车辆详情
│   │   └── alert/vehicleAlert.vue        #   车辆预警
│   ├── 04-pickup-return/                 # 取还车验车
│   │   └── inspect/pickupInspect.vue
│   ├── 05-car-ops/                       # 车务管理
│   │   ├── wash/caropsWash.vue           #   洗车任务
│   │   ├── fuel/caropsFuel.vue           #   加油任务
│   │   ├── maintain/caropsMaintain.vue   #   保养维修
│   │   └── prep/caropsPrep.vue           #   整备车辆
│   ├── 06-transfer/                      # 调拨调度
│   │   ├── list/transferList.vue         #   调拨任务
│   │   └── dispatch/transferDispatch.vue #   调度任务
│   ├── 07-task/                          # 任务管理
│   │   ├── list/taskList.vue             #   任务列表
│   │   └── my/taskMy.vue                 #   我的任务
│   ├── 08-contract/                      # 合同签署
│   │   └── sign/contractSign.vue
│   ├── 09-billing/                       # 费用结算
│   │   ├── verify/billingVerify.vue      #   核验费用
│   │   ├── reduce/billingReduce.vue      #   费用减免
│   │   └── repay/billingRepay.vue        #   补款列表
│   ├── 10-risk/                          # 风控审核
│   │   ├── alert/riskAlert.vue           #   风控预警
│   │   ├── process/riskProcess.vue       #   风控处理
│   │   └── user/riskUser.vue             #   风险用户
│   └── 11-store/                         # 门店管理
│       └── order/storeOrder.vue          #   门店下单
│
├── shared/                               # 跨模块共享资源（历史 HTML 原型使用）
│   ├── design-tokens/
│   │   └── tokens.css                    #   全局 CSS 变量（旧 HTML 页面使用）
│   └── components/
│       ├── layout.js                     #   侧边栏+顶栏自动渲染（旧 HTML 页面使用）
│       ├── layout.css                    #   布局样式
│       ├── header.js                     #   顶栏组件
│       ├── sidebar.js                    #   侧边栏导航组件
│       └── modal.js                      #   通用弹窗组件
│
├── templates/
│   └── vue-module-template/              # ⭐ v3.0 新模板：Vue 组件脚手架
│       ├── index.vue                     #   模板 Vue 组件
│       └── README.md                     #   模板使用说明
│
├── scripts/
│   ├── create-module.sh                  # 一键创建新模块
│   ├── deploy.sh                         # 部署到静态站点
│   ├── sync-frontend.sh                  # ⭐ v3.0 同步修改到 ProtoHub
│   └── push-to-protohub.sh              # 推送质量保障脚本
│
├── docs/
│   ├── team-guide.md                     # 👈 本文件（团队操作指南）
│   ├── style-guide.md                    # ⭐ 设计规范（前端代码样式对齐）
│   ├── data-flow-map.md                  # ⭐ 改动关联检查的核心依据 + 业务术语映射表
│   ├── change-log.md                     # 变更追溯日志（Step 10 自动追加）
│   └── ai-prompt-templates.md           # 提示词模板库
│
└── tmp/                                  # 运行时临时文件（gitignore，不提交）
    ├── code_changes.md                   # Step 0.5 产出：前端代码变更扫描结果
    ├── pull_status.md                    # Step 0 产出
    ├── change_plan.md                    # Step 1 产出
    ├── preview_result.md                 # Step 4 产出
    ├── impact_check.md                   # Step 5 产出
    ├── self_audit.md                     # Step 6 产出
    └── commit_preview.md                 # Step 7 产出
```

**文件命名规范**：`.vue` 文件使用前端仓库中的原始文件名（如 `orderList.vue`），保持与前端代码的一致性，便于比对和同步。

---

### §2 业务术语-仓库/页面映射表

> 加载时机：Step 2 变更类型评估、Step 6 关联影响检查、接入新原型时
>
> 完整版见 `docs/data-flow-map.md`（含核心枚举、上下游影响）。此处为快速索引。

#### 订单管理

| 业务术语 | 后端仓库 | 前端仓库 | 前端页面路径 | 备注 |
|---------|---------|---------|------------|------|
| 订单列表 | mdscr-order | mdscr-fe-admin | modules/02-order/list | ⚡ 核心，改动影响最广 |
| 订单取车 | mdscr-order | mdscr-fe-admin | modules/02-order/pickup | — |
| 订单还车 | mdscr-order | mdscr-fe-admin | modules/02-order/return | — |
| 订单退款 | mdscr-order | mdscr-fe-admin | modules/02-order/refund | — |
| 短期预留 | mdscr-order | mdscr-fe-admin | modules/02-order/reserve | — |

#### 车辆/车型/车龄

| 业务术语 | 后端仓库 | 前端仓库 | 前端页面路径 | 核心枚举 | 渠道参照 |
|---------|---------|---------|------------|---------|---------|
| 车辆管理 | mdscr-vehicle | mdscr-fe-admin | modules/03-vehicle/list | AssetCarStatusEnum, AssetCarBizTypeEnum | — |
| 车辆列表 | mdscr-vehicle | mdscr-fe-admin | modules/03-vehicle/list | AssetCarStatusEnum（在售/已售/在租/维修中等） | — |
| 车辆详情 | mdscr-vehicle | mdscr-fe-admin | modules/03-vehicle/detail | AssetCarStatusEnum | — |
| 车辆预警 | mdscr-vehicle | mdscr-fe-admin | modules/03-vehicle/alert | — | — |
| 车型/车型组 | mdscr-vehicle | mdscr-fe-admin | views/income/tagStrategyConfigList | CarTypeEnum, CarAgeTagEnum | 车型组：经济型/SUV/商务等 |
| 车龄标签/车龄配置 | mdscr-vehicle | mdscr-fe-admin | views/income/tagStrategyConfigList | CarAgeTagEnum（其他/半年内/一年内/两年内/三年内） | 兜底"一年内新车" |
| 渠道标签策略 | mdscr-vehicle | mdscr-fe-admin | views/income/channelTagManage | — | — |

#### 取还车/验车

| 业务术语 | 后端仓库 | 前端仓库 | 前端页面路径 | 备注 |
|---------|---------|---------|------------|------|
| 取还车验车 | mdscr-order | mdscr-fe-admin | modules/04-pickup-return/inspect | 含车损照片、里程、油量 |

#### 车务管理

| 业务术语 | 后端仓库 | 前端仓库 | 前端页面路径 | 备注 |
|---------|---------|---------|------------|------|
| 洗车任务 | mdscr-maintenance | mdscr-fe-admin | modules/05-car-ops/wash | — |
| 加油任务 | mdscr-maintenance | mdscr-fe-admin | modules/05-car-ops/fuel | — |
| 保养维修 | mdscr-maintenance | mdscr-fe-admin | modules/05-car-ops/maintain | — |
| 整备车辆 | mdscr-maintenance | mdscr-fe-admin | modules/05-car-ops/prep | — |

#### 调拨调度

| 业务术语 | 后端仓库 | 前端仓库 | 前端页面路径 | 备注 |
|---------|---------|---------|------------|------|
| 调拨任务 | mdscr-dispatch | mdscr-fe-admin | modules/06-transfer/list | — |
| 调度任务 | mdscr-dispatch | mdscr-fe-admin | modules/06-transfer/dispatch | — |

#### 任务管理

| 业务术语 | 后端仓库 | 前端仓库 | 前端页面路径 | 备注 |
|---------|---------|---------|------------|------|
| 任务列表 | mdscr-order | mdscr-fe-admin | modules/07-task/list | work_info 主表 |
| 我的任务 | mdscr-order | mdscr-fe-admin | modules/07-task/my | — |

#### 合同签署

| 业务术语 | 后端仓库 | 前端仓库 | 前端页面路径 | 备注 |
|---------|---------|---------|------------|------|
| 签署合同 | mdscr-order | mdscr-fe-admin | modules/08-contract/sign | — |

#### 费用结算

| 业务术语 | 后端仓库 | 前端仓库 | 前端页面路径 | 核心枚举 | 备注 |
|---------|---------|---------|------------|---------|------|
| 核验费用 | mdscr-order | mdscr-fe-admin | modules/09-billing/verify | — | order_fee 主表 |
| 费用减免 | mdscr-order | mdscr-fe-admin | modules/09-billing/reduce | — | — |
| 补款列表 | mdscr-order | mdscr-fe-admin | modules/09-billing/repay | PayStatusEnum（WAIT_PAY/PAID/EXPIRED） | 补差金额 extra_pay_amount |
| 车型升级 | mdscr-order | mdscr-fe-admin | views/sale/order/orderList | UpgradeTypeEnum（FREE_UPGRADE/FREE_UPGRADE_PAY_DIFF） | — |

#### 风控审核

| 业务术语 | 后端仓库 | 前端仓库 | 前端页面路径 | 备注 |
|---------|---------|---------|------------|------|
| 风控预警 | mdscr-order | mdscr-fe-admin | modules/10-risk/alert | — |
| 风控处理 | mdscr-order | mdscr-fe-admin | modules/10-risk/process | ApprovalRouteEnum（STORE_SUPERVISOR/STORE_SUPERVISOR_AREA_DIRECTOR） |
| 风险用户 | mdscr-order | mdscr-fe-admin | modules/10-risk/user | — |

#### 门店管理

| 业务术语 | 后端仓库 | 前端仓库 | 前端页面路径 | 备注 |
|---------|---------|---------|------------|------|
| 门店下单 | mdscr-store | mdscr-fe-admin | modules/11-store/order | — |
| 门店工作台 | mdscr-store | mdscr-fe-admin | modules/01-dashboard/store | — |

---

### §3 新成员环境准备（每人一次）

#### 步骤一：获取内网 Git Personal Access Token

1. 浏览器打开 [git.17usoft.com](http://git.17usoft.com) 并登录
2. 右上角头像 → **Settings** → **SSH Keys**（推荐）或 **Access Tokens**
3. **SSH Key 方式（推荐）**：
   - 本地执行 `ssh-keygen -t ed25519 -C "your-email@company.com"` 生成密钥
   - 将 `~/.ssh/id_ed25519.pub` 内容粘贴到 GitLab → Add SSH Key
   - 后续 clone/pull/push 均通过 SSH 协议，无需 Token
4. **Token 方式（备选）**：
   - 右上角头像 → **Settings** → **Access Tokens**
   - 点击 **Add new token**，配置：
     - **Token name**：`ProtoHub-你的名字`
     - **Expiration date**：选最长（如 2027-12-31）
     - **Select scopes**：勾选 `read_repository` + `write_repository`
   - 点击 **Create personal access token**，立即复制（关闭后不可见）

> ⚠️ **安全策略**：HTTP+域账号密码方式已禁用，必须使用 **SSH 协议** 或 **域账号+Token**。

#### 步骤二：克隆 ProtoHub-mada 仓库

在你的 AI 工具中发送（把 `你的Token` 替换掉）：

```
我的内网 Git 仓库是 git@git.17usoft.com:LY-MDSCR/ProtoHub-mada.git（SSH 方式）
dev 分支，帮我把仓库克隆到本地，以后每次我改原型都帮我提交上去
```

或使用 Token 方式：

```
我的内网 Git 仓库是 http://git.17usoft.com/LY-MDSCR/ProtoHub-mada.git
dev 分支，Token 是 你的Token
帮我把仓库克隆到本地，以后每次我改原型都帮我提交上去
```

AI 会自动完成克隆、配置 SSH/Token 鉴权。后续所有 pull/push 均自动使用 SSH 或 Token。

#### 步骤三：克隆前端仓库（v3.0 新增）

原型修改需要拉取生产环境前端代码。按需克隆相关前端仓库：

```
帮我把前端仓库 mdscr-fe-admin 克隆到 frontend-workspace/ 目录
仓库地址：git@git.17usoft.com:LY-MDSCR/mdscr-fe-admin.git（SSH 方式）
```

或使用 Token 方式：

```
帮我把前端仓库 mdscr-fe-admin 克隆到 frontend-workspace/ 目录
仓库地址：http://oauth2:<你的TOKEN>@git.17usoft.com/LY-MDSCR/mdscr-fe-admin.git
```

> **常用前端仓库**：mdscr-fe-admin（管理后台）、mdscr-fe-store-wx（门店小程序）、mdscr-fe-wap（C 端 H5）
>
> 不需要一次性克隆所有仓库，用到哪个克隆哪个。

#### 步骤四：安装前端依赖（v3.0 新增）

克隆前端仓库后，需要安装依赖才能构建预览：

```bash
cd frontend-workspace/mdscr-fe-admin
npm install    # 或 pnpm install / yarn install
```

#### 步骤五：了解分支管理规范

原型修改不在 dev 分支上直接改，而是创建功能分支。详见 §8 分支管理与版本追踪。

简单来说：每次修改前说「拉最新代码」，AI 会自动拉取 dev 并创建功能分支（如 `protohub/order-refund`）。修改推送到功能分支，评审通过后才合并到 dev。

#### 步骤六：验证

对 AI 说「启动前端预览」，能访问 `http://localhost:5173` 看到页面即成功。

---

### §4 不同工具操作对照

团队用不同 AI 工具没关系，核心流程一样：

#### 类型一：可直接操作本地文件的对话式 AI（推荐）

**特征**：AI 能直接读写你电脑上的文件，能执行 Git 命令。

**举例**：智能体（可操作本地文件的对话式 AI）

**操作**：直接按 L1 工作流操作，用自然语言对话完成全程。

| 你想做的事 | 对 AI 说 |
|-----------|---------|
| 开始工作前同步 | 「拉最新代码，扫描一下 [模块] 的前端代码变更」 |
| 修改原型 | 「帮我把 xxx 页面的 yyy 改成 zzz」（AI 自动定位 Vue 文件并修改） |
| 预览效果 | 「启动前端预览」或「帮我打开 xxx 页面预览」 |
| 确认推送 | 「可以推了」（推到功能分支） |
| 评审通过合并 | 「评审通过了，合并到 dev」 |
| 查看改动记录 | 「最近 5 次提交记录」 |
| 回退版本 | 「帮我把 xxx 恢复到功能分支上次提交的版本」 |
| 回退已合并的修改 | 「帮我把 xxx 的修改从 dev 上 revert 掉」 |
| 检查关联影响 | 「我改完了，帮我检查关联影响」 |
| 接入新原型 | 「帮我把 [原型路径] 接入 ProtoHub」 |
| 扫描代码变更 | 「扫描一下 [模块] 的最新前端代码变更」 |
| 克隆前端仓库 | 「帮我克隆 [仓库名] 到 frontend-workspace/」 |

#### 类型二：纯 Web 端 AI 对话工具（需手动操作 Git）

**特征**：浏览器访问，无法直接读写本地文件（ChatGPT 网页版、豆包等）

**操作方式**：
1. 用 Git 客户端拉最新代码
2. 把目标 HTML 文件内容复制给 AI
3. 描述改动需求 → AI 返回修改后代码
4. 粘贴回本地文件 → 浏览器检查
5. 满意后用 Git 客户端提交推送

> 建议优先使用类型一的工具，不需要手动 Git 操作。

---

### §5 提示词模板库

#### 修改已有页面

```
帮我修改前端仓库 mdscr-fe-admin 中的订单列表页面：
- 文件路径：src/views/sale/order/orderList.vue
- [具体改动 1]
- [具体改动 2]
保持现有其他功能不变；Web 页面复用现有 Element UI 组件和样式，小程序页面复用 Vant 组件和样式
```

**好 vs 差的描述：**

| ❌ 差 | ✅ 好 |
|-------|-------|
| 「优化一下订单列表」 | 「订单列表表格，在『手机号』列后面加一列『客户等级』，显示 VIP / 普通 / 新客」 |
| 「改一下颜色」 | 「已还车状态标签改成绿色 `#52C41A`，已取消改成灰色 `#8C8C8C`」 |
| 「加个搜索功能」 | 「搜索栏增加『订单来源』下拉筛选：携程 / 飞猪 / APP / 线下，Web 用 el-select 组件；小程序用 van-picker」 |

#### 新建页面

```
帮我在前端仓库 mdscr-fe-admin 中创建一个新页面：
- 放置位置：src/views/[模块目录]/
- 页面名称：[名称]
- 布局：[描述页面结构]
- 功能：[要有什么功能]
- 数据：[展示什么数据]
- 操作：[支持什么操作]
样式与同类型页面保持一致；Web 复用 Element UI 组件，小程序复用 Vant 组件

【重要】修改完成后，把新建的 .vue 文件同步到 ProtoHub-mada/modules/[对应模块]/，
并更新 docs/data-flow-map.md 补充数据来源和上下游关系。
```

#### 参考截图修改

```
（直接把 UI 截图拖到对话框）
参考这个截图，帮我修改前端仓库中的 [文件路径]，
按照截图的布局调整；Web 复用现有 Element UI 组件，小程序复用 Vant 组件
```

#### 全局样式修改

```
⚠️ 全局样式修改，影响所有页面，请先确认关联范围
帮我修改前端仓库中的全局样式文件，
涉及 [文件路径] 和相关页面
```

---

### §6 设计规范

> 完整规范：`docs/style-guide.md`（包含前端代码样式对齐原则、Vue 组件修改规范、Web Element UI / 小程序 Vant 组件复用规则）
> 加载时机：Step 3-4 修改前端代码时

#### 6.1 核心原则（必须遵守）

1. **前端代码驱动**：不再生成独立演示 HTML。直接修改生产环境前端 Vue 代码，用修改后的代码构建预览
2. **前端代码为准**：样式以生产环境 Vue 源码中的 `<template>` + `<style scoped>` 为唯一标准
3. **组件复用优先**：Web 优先使用前端代码中已有的 Element UI 组件和共享组件（SearchForm、SearchItem、Table 等）；小程序优先使用 Vant 组件和项目业务组件
4. **忠实修改**：修改时保持原有代码风格、组件结构、CSS 类名不变，只改需求相关的部分

#### 6.2 Vue 代码修改规范

| 规范 | 要求 |
|------|------|
| 组件类型 | Web 使用 Element UI 组件（el-table / el-form / el-descriptions 等），小程序使用 Vant 组件（van-cell / van-field / van-popup 等），不自定义替代组件 |
| 样式来源 | CSS 类名来自源码 `<style scoped>`，不添加源码中不存在的自定义类 |
| 颜色使用 | 使用源码中的 CSS 变量、Element UI 主题变量或 Vant 主题变量，不硬编码色值 |
| 新增内容 | 与原有内容使用完全一致的组件和 props |
| 模拟数据 | 使用真实枚举值（来自 Hub）和合理业务数据 |

#### 6.3 状态标签颜色规范

| 状态类型 | Element UI / Vant 类型 | 示例 |
|----------|-------------------|------|
| 成功/已完成 | `el-tag type="success"` | 已还车、已支付、正常 |
| 进行中/处理中 | `el-tag type="primary"` | 已取车、处理中、待审核 |
| 警告/待处理 | `el-tag type="warning"` | 待确认、未支付、待整备 |
| 危险/异常/取消 | `el-tag type="danger"` | 已取消、异常、已退款 |
| 中性/默认 | `el-tag type="info"` | 草稿、已关闭 |

#### 6.4 构建预览

修改 Vue 代码后，在前端仓库目录启动 dev server 预览：

```bash
cd frontend-workspace/mdscr-fe-admin
npm run dev    # 或 pnpm dev / yarn dev
# 浏览器访问 http://localhost:5173 导航到修改的页面
```

> 预览满意后，将修改的 `.vue` 文件同步到 ProtoHub-mada 的 `modules/` 目录，保持目录结构对应。

---

### §7 常见问题

**Q: 我不会写代码，能用吗？**

可以。你描述「页面上要有什么、长什么样子」，AI 来修改前端代码。预览通过 dev server 自动渲染，你只需要看效果。

**Q: 为什么不直接生成 HTML 了？**

独立 HTML 原型和实际系统容易脱节。直接修改前端 Vue 代码，预览效果和真实系统 100% 一致，开发交付时也更容易对照。

**Q: 前端仓库怎么克隆？**

对 AI 说「帮我克隆 mdscr-fe-admin 到 frontend-workspace/」。常用前端仓库：mdscr-fe-admin（管理后台）、mdscr-fe-store-wx（门店小程序）、mdscr-fe-wap（C 端 H5）。

**Q: Token 过期了怎么办？**

去 git.17usoft.com 重新生成，对 AI 说「帮我更新 Git Token 为 新Token」。

**Q: 怎么知道同事改了什么？**

对 AI 说「帮我看看最近 5 次提交记录」。

**Q: 预览页面怎么打开？**

对 AI 说「启动前端预览」，AI 会在前端仓库目录运行 `npm run dev`，然后你在浏览器访问 `http://localhost:5173`。

**Q: 多个同事同时改同一个页面怎么办？**

各自在功能分支上改（如 `protohub/order-refund-张三` 和 `protohub/order-refund-李四`），合并到 dev 时 AI 辅助解决冲突。

**Q: 怎么回退到之前的版本？**

三种方式（详见 §8.3 版本回滚）：
- 放弃本次修改：切回 dev，删除功能分支
- 回到某个中间版本：`git log` 找到 commit，`git checkout <commit> -- 文件路径`
- 回退已合并的修改：`git revert <merge-commit>`

**Q: 修改推到哪里？会推到前端开发仓库吗？**

不会。修改只推到 ProtoHub-mada 的功能分支（如 `protohub/order-refund`），**不会同步到前端开发仓库**（mdscr-fe-admin 等）。前端开发仓库只是只读的样式参考来源。

**Q: 怎么知道我的原型快照基于前端仓库的哪个版本？**

查看 ProtoHub-mada `modules/` 下 `.vue` 文件头部的快照版本标记注释，包含 `Source Repo`、`Base Commit`、`Source Path` 等信息。详见 §8.5 快照版本标记。

**Q: 新增了一个页面，还要做什么？**

除了在前端仓库中创建新 `.vue` 文件，还必须：
1. 把新文件同步到 ProtoHub-mada 的 `modules/` 目录
2. 更新 `docs/data-flow-map.md`，补充业务术语映射和上下游影响
3. 执行关联检查（Step 5）

**Q: 旧的 HTML 原型还能用吗？**

可以。`modules/` 下的旧 `.html` 文件保留为历史参考。新的修改会创建 `.vue` 文件，逐步替换旧 HTML。

**Q: 不记得某个页面的前端文件路径了怎么办？**

对 AI 说「帮我查一下订单列表在前端仓库中的路径」，AI 会通过 gitnexus-hub 或术语映射表定位。

---

### §8 分支管理与版本追踪

> 加载时机：Step 0 拉取代码前、Step 7 推送前、需要回滚时

#### 8.1 分支策略

原型修改在 **ProtoHub-mada 仓库** 中用分支管理，不涉及前端开发仓库。

```
ProtoHub-mada 分支结构：

dev                          ← 主分支（稳定，团队共享）
├── protohub/order-refund    ← 功能分支（退款审批原型）
├── protohub/vehicle-alert   ← 功能分支（车辆预警原型）
└── protohub/billing-verify  ← 功能分支（费用核验原型）
```

**核心规则**：
- **不直接推 dev**：每次修改创建功能分支，在分支上提交
- **只推 ProtoHub-mada**：功能分支只推到 ProtoHub-mada 仓库，**不同步到前端开发仓库**
- **dev 合并时机**：原型评审通过后，将功能分支合并到 dev
- **分支命名**：`protohub/{模块}-{功能简称}`，如 `protohub/order-refund`

#### 8.2 操作流程

**开始修改前**：

```bash
cd /Users/weigaopeng/WorkBuddy/2026-06-03-17-10-25

# 1. 拉取 dev 最新代码
git checkout dev
git pull inner dev

# 2. 创建功能分支
git checkout -b protohub/order-refund
```

**修改完成后推送**：

```bash
# 3. 提交修改到功能分支
git add modules/02-order/refund/orderRefund.vue
git commit -m "feat(order-refund): 退款审批新增金额展示字段"

# 4. 推送功能分支到 ProtoHub-mada（不推前端仓库）
git push inner protohub/order-refund
```

**评审通过后合并到 dev**：

```bash
# 5. 合并到 dev
git checkout dev
git merge protohub/order-refund
git push inner dev

# 6. 可选：删除功能分支
git branch -d protohub/order-refund
git push inner --delete protohub/order-refund
```

#### 8.3 版本回滚

**回滚到修改前**（放弃本次所有修改）：

```bash
git checkout dev                    # 切回 dev，放弃功能分支修改
git branch -D protohub/order-refund  # 删除功能分支
```

**回滚到某个中间版本**（继续调整）：

```bash
git log --oneline protohub/order-refund   # 查看提交历史
git checkout <commit-hash> -- modules/02-order/refund/orderRefund.vue  # 恢复某个版本
```

**回滚已合并到 dev 的修改**：

```bash
git checkout dev
git log --oneline                       # 找到合并 commit
git revert <merge-commit-hash>          # 反向提交，安全回滚
git push inner dev
```

#### 8.4 多人协作

| 场景 | 处理方式 |
|------|---------|
| 两人改同一个页面 | 各自在功能分支上改，合并时 AI 辅助解决冲突 |
| 需要基于同事的原型继续改 | `git checkout protohub/同事的分支`，在此基础上创建新分支 |
| 同事的功能分支还没合并 dev | 可以直接从功能分支拉取：`git pull inner protohub/同事的分支` |

#### 8.5 快照版本标记

每个推送到 ProtoHub-mada `modules/` 的 `.vue` 文件，在文件头部添加版本标记注释：

```vue
<!--
  ProtoHub Snapshot
  Source Repo: mdscr-fe-admin
  Source Branch: dev
  Base Commit: a1b2c3d
  Source Path: src/views/sale/order/orderRefundList/index.vue
  Modified: 2026-06-24
  Modifier: weigaopeng
  Change: 退款审批新增金额展示字段 + 审批意见区域
-->
```

> AI 在 Step 7（同步到 ProtoHub）时自动添加此注释。

#### 8.6 三版本比对

**问题**：如何知道本地版本、前端仓库最新版本、ProtoHub 快照版本的差异？

```bash
# 1. 查看 frontend-workspace 中前端仓库的当前版本
cd frontend-workspace/mdscr-fe-admin
git log --oneline -1                          # 当前 commit

# 2. 查看前端仓库远程最新版本
git fetch origin
git log --oneline origin/dev -1               # 远程最新 commit

# 3. 读取 ProtoHub 快照文件头部的 Base Commit（即快照基于哪个前端版本）

# 4. 比较前端仓库本地 vs 远程差异
git diff HEAD origin/dev -- src/views/sale/order/orderRefundList/index.vue

# 5. 比较 frontend-workspace 中的修改 vs ProtoHub 快照
diff frontend-workspace/mdscr-fe-admin/src/views/sale/order/orderRefundList/index.vue \
     /Users/weigaopeng/WorkBuddy/2026-06-03-17-10-25/modules/02-order/refund/orderRefund.vue
```

**何时需要重新拉取前端代码**：
- 首次设置：克隆前端仓库
- 前端仓库有新功能/新页面需要参考
- 快照的 Base Commit 距前端仓库最新 commit 超过 2 周
- **不需要每次修改前都全量拉取**

---

### §9 代码定位指南

> 加载时机：Step 2 读取目标 Vue 文件时

#### 三步定位法

从产品需求描述到具体代码修改点，分三步：

**第一步：术语映射表 → 定位仓库和页面路径**

查 §2 业务术语映射表（或 `docs/data-flow-map.md`），根据产品描述中的业务术语定位：

| 业务术语 | 前端仓库 | 前端页面路径 |
|---------|---------|------------|
| 订单退款 | mdscr-fe-admin | views/sale/order/orderRefundList |
| 退款审批 | mdscr-fe-admin | views/auditList/components/OrderRefund |
| 保险加购 | mdscr-fe-admin | views/sale/order/orderDetail/components/InsuranceInfo |

> 如果术语映射表没有命中，对 AI 说「帮我通过 Hub 查一下 {业务术语} 对应的前端页面路径」。

**第二步：页面路径 → 定位 Vue 文件**

```bash
# 在 frontend-workspace 中查找目标文件
find frontend-workspace/mdscr-fe-admin/src/views/sale/order/orderRefundList -name "*.vue"
```

典型页面目录结构：

```
orderRefundList/
├── index.vue              ← 列表页主体（搜索栏 + 表格 + 分页）
├── components/
│   ├── RefundDetail.vue   ← 退款详情弹窗
│   ├── RefundForm.vue     ← 退款表单
│   └── AuditDialog.vue    ← 审批弹窗
└── hooks/
    └── useRefund.ts       ← 业务逻辑（接口调用、数据处理）
```

**第三步：Vue 文件 → 定位修改点**

在 `.vue` 文件中通过 `<template>` 结构精准定位修改区域：

```vue
<template>
  <!-- ① 搜索区域 -->
  <SearchForm>
    <SearchItem label="订单号">...</SearchItem>
    <SearchItem label="退款状态">...</SearchItem>
    <!-- 🎯 PRD 说"新增筛选条件" → 改这里 -->
  </SearchForm>

  <!-- ② 表格区域 -->
  <Table>
    <el-table-column label="订单号" prop="orderNo" />
    <el-table-column label="退款金额" prop="refundAmount" />
    <!-- 🎯 PRD 说"表格新增列" → 改这里 -->
  </Table>

  <!-- ③ 详情/弹窗区域 -->
  <el-dialog title="退款详情">
    <RefundDetail :data="currentRow" />
    <!-- 🎯 PRD 说"详情页新增字段" → 改这里 -->
  </el-dialog>
</template>
```

#### 常见修改场景定位速查

| PRD 描述 | 定位区域 | 典型文件 |
|---------|---------|---------|
| "列表新增筛选条件" | ① 搜索区域 `<SearchForm>` | `index.vue` |
| "表格新增列" | ② 表格区域 `<el-table-column>` | `index.vue` |
| "详情页新增字段" | ③ 详情区域 `<el-descriptions-item>` | `Detail/index.vue` 或 `components/RefundDetail.vue` |
| "弹窗新增表单项" | ③ 弹窗区域 `<el-form-item>` | `components/AuditDialog.vue` |
| "按钮新增/调整" | 工具栏 `<el-button>` | `index.vue` 的 `<template #actionBar>` |
| "状态标签调整" | 表格列的 `<el-tag>` 渲染 | `index.vue` 或 `hooks/useXxx.ts` |
| "新增页面" | 创建新 `.vue` 文件 | 新建文件 |
| "接口字段变更" | `<script>` 中的接口调用和数据处理 | `hooks/useXxx.ts` 或 `index.vue` |

#### 对 AI 说的标准句式

```
帮我修改 {前端仓库} 中的 {页面名称}：
- 文件路径：src/views/{路径}/index.vue
- 修改内容：{具体描述}
- 定位区域：{搜索区域/表格区域/详情弹窗/工具栏}
保持其他功能不变；Web 复用现有 Element UI 组件和样式，小程序复用 Vant 组件和样式
```

> 如果不确定文件路径，省略路径让 AI 通过术语映射表或 Hub 查询定位。

---

## 附录：仓库信息速查

| 项目 | 值 |
|------|-----|
| **ProtoHub 仓库地址（SSH）** | `git@git.17usoft.com:LY-MDSCR/ProtoHub-mada.git` |
| **ProtoHub 仓库地址（Token）** | `http://oauth2:<TOKEN>@git.17usoft.com/LY-MDSCR/ProtoHub-mada.git` |
| **⚠️ 安全策略** | HTTP+域账号密码已禁用，必须用 SSH 或域账号+Token |
| **默认分支** | `dev` |
| **本地路径** | `/Users/weigaopeng/WorkBuddy/2026-06-03-17-10-25/` |
| **远程名称** | `inner` |
| **SSH Key 配置** | git.17usoft.com → Settings → SSH Keys |
| **Token 获取** | git.17usoft.com → Settings → Access Tokens |
| **Token 权限** | `read_repository` + `write_repository` |
| **数据流向文档** | `docs/data-flow-map.md` |
| **设计规范** | `docs/style-guide.md` |
| **前端工作区** | `frontend-workspace/`（gitignored，只读参考） |
| **常用前端仓库** | mdscr-fe-admin / mdscr-fe-store-wx / mdscr-fe-wap |
| **前端仓库地址（SSH）** | `git@git.17usoft.com:LY-MDSCR/{仓库名}.git` |
| **前端仓库地址（Token）** | `http://oauth2:<TOKEN>@git.17usoft.com/LY-MDSCR/{仓库名}.git` |
| **分支策略** | 功能分支 `protohub/{模块}-{功能}` → 评审通过后合并 dev |
| **推送目标** | 只推 ProtoHub-mada，不推前端开发仓库 |
| **Skill 文件** | `~/.workbuddy/skills/protohub-workflow/SKILL.md` |
| **gitnexus-hub** | multica skill 封装，MCP 地址 `http://ibd.travel.t.17usoft.com/gitnexus/mcp` |

---

> 有问题直接群里 @ 管理员，或对 AI 说「帮我看看这是什么问题」。
