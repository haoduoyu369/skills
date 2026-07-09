# 数据流向映射文档

> 版本：v2.0（2026-06-22）| 新增：业务术语-仓库/页面映射表（对齐 prd-writer v2.0 术语映射规范）
>
> 记录各模块/页面的业务术语映射、数据来源、上下游影响关系。
> **每次新增或修改模块/页面后，必须同步更新本文档。**

---

## 目录

- [使用说明](#使用说明)
- [业务术语-仓库/页面映射表（AI 系统感知核心）](#业务术语-仓库页面映射表ai-系统感知核心)
- [模块总览](#模块总览)
- [详细数据流向映射](#详细数据流向映射)
- [改动影响速查表](#改动影响速查表)
- [更新记录](#更新记录)

---

## 使用说明

### 什么时候需要查这篇文档？

| 场景 | 查哪个章节 |
|------|----------|
| 要改某个页面，不确定关联影响 | [改动影响速查表](#改动影响速查表) |
| AI 做系统感知，定位业务术语对应的代码位置 | [业务术语-仓库/页面映射表](#业务术语-仓库页面映射表ai-系统感知核心) |
| 新增模块/页面，填写数据来源 | [详细数据流向映射](#详细数据流向映射)（复制模板追加） |
| 产品评审前确认关联覆盖 | [详细数据流向映射](#详细数据流向映射) |

### 字段说明

| 字段 | 含义 |
|------|------|
| **业务术语** | 产品描述中使用的业务名称 |
| **后端仓库** | 对应的后端微服务仓库名（`mdscr-*`） |
| **前端仓库** | 对应的前端仓库名（`mdscr-fe-*`） |
| **前端页面路径** | ProtoHub 内 HTML 文件路径 / 前端仓库 views 路径 |
| **核心枚举** | 该页面涉及的关键枚举类型 |
| **数据来源** | 原型阶段的模拟数据来源标注（`order_info` / `car_info` 等） |
| **上游依赖** | 改了哪些页面的数据，会影响本页面 |
| **下游影响** | 本页面的数据改动，会影响哪些页面 |

---

## 业务术语-仓库/页面映射表（AI 系统感知核心）

> 加载时机：Step 2 变更类型评估、Step 6 关联影响检查、接入新原型时、AI 做系统感知时。
>
> **AI 使用说明**：收到产品描述的业务术语（如「订单列表」「核验费用」），先查此表定位仓库 + 页面路径，再读对应 HTML 文件。

### 订单管理

| 业务术语 | 后端仓库 | 前端仓库 | 前端页面路径（ProtoHub） | 核心枚举 | 渠道参照 |
|---------|---------|---------|------------------------|---------|---------|
| 订单列表 | mdscr-order | mdscr-fe-admin | modules/02-order/list/order-list.html | OrderStatusEnum, PayStatusEnum | ⚡ 核心，改动影响最广 |
| 订单取车 | mdscr-order | mdscr-fe-admin | modules/02-order/pickup/order-pickup.html | — | — |
| 订单还车 | mdscr-order | mdscr-fe-admin | modules/02-order/return/order-return.html | — | — |
| 订单退款 | mdscr-order | mdscr-fe-admin | modules/02-order/refund/order-refund.html | RefundStatusEnum | — |
| 短期预留 | mdscr-order | mdscr-fe-admin | modules/02-order/reserve/order-reserve.html | ReserveStatusEnum | — |
| 车型升级 | mdscr-order | mdscr-fe-admin | views/sale/order/orderList（行内弹窗） | UpgradeTypeEnum（FREE_UPGRADE/FREE_UPGRADE_PAY_DIFF） | — |
| 升级审批 | mdscr-order | mdscr-fe-admin | views/auditList/components/UpgradeCar | ApprovalRouteEnum（STORE_SUPERVISOR/STORE_SUPERVISOR_AREA_DIRECTOR） | — |
| 退款审批 | mdscr-order | mdscr-fe-admin | views/auditList/components/OrderRefund | — | — |

### 车辆/车型/车龄

| 业务术语 | 后端仓库 | 前端仓库 | 前端页面路径（ProtoHub） | 核心枚举 | 渠道参照 |
|---------|---------|---------|------------------------|---------|---------|
| 车辆管理 | mdscr-vehicle | mdscr-fe-admin | modules/03-vehicle/list/vehicle-list.html | AssetCarStatusEnum, AssetCarBizTypeEnum | — |
| 车辆列表 | mdscr-vehicle | mdscr-fe-admin | modules/03-vehicle/list/vehicle-list.html | AssetCarStatusEnum（在售/已售/在租/维修中等） | — |
| 车辆详情 | mdscr-vehicle | mdscr-fe-admin | modules/03-vehicle/detail/vehicle-detail.html | AssetCarStatusEnum | — |
| 车辆预警 | mdscr-vehicle | mdscr-fe-admin | modules/03-vehicle/alert/vehicle-alert.html | — | — |
| 车型/车型组 | mdscr-vehicle | mdscr-fe-admin | views/income/tagStrategyConfigList | CarTypeEnum, CarAgeTagEnum | 车型组：经济型/SUV/商务等 |
| 车龄标签/车龄配置 | mdscr-vehicle | mdscr-fe-admin | views/income/tagStrategyConfigList | CarAgeTagEnum（其他/半年内/一年内/两年内/三年内） | 兜底"一年内新车" |
| 渠道标签策略 | mdscr-vehicle | mdscr-fe-admin | views/income/channelTagManage | — | — |

### 取还车/验车

| 业务术语 | 后端仓库 | 前端仓库 | 前端页面路径（ProtoHub） | 核心枚举 | 备注 |
|---------|---------|---------|------------------------|---------|------|
| 取还车验车 | mdscr-order | mdscr-fe-admin | modules/04-pickup-return/inspect/pickup-inspect.html | — | 含车损照片、里程、油量快照 |

### 车务管理

| 业务术语 | 后端仓库 | 前端仓库 | 前端页面路径（ProtoHub） | 核心枚举 | 备注 |
|---------|---------|---------|------------------------|---------|------|
| 洗车任务 | mdscr-maintenance | mdscr-fe-admin | modules/05-car-ops/wash/carops-wash.html | — | work_info 驱动 |
| 加油任务 | mdscr-maintenance | mdscr-fe-admin | modules/05-car-ops/fuel/carops-fuel.html | — | — |
| 保养维修 | mdscr-maintenance | mdscr-fe-admin | modules/05-car-ops/maintain/carops-maintain.html | — | — |
| 整备车辆 | mdscr-maintenance | mdscr-fe-admin | modules/05-car-ops/prep/carops-prep.html | — | 还车后自动触发 |

### 调拨调度

| 业务术语 | 后端仓库 | 前端仓库 | 前端页面路径（ProtoHub） | 核心枚举 | 备注 |
|---------|---------|---------|------------------------|---------|------|
| 调拨任务 | mdscr-dispatch | mdscr-fe-admin | modules/06-transfer/list/transfer-list.html | — | — |
| 调度任务 | mdscr-dispatch | mdscr-fe-admin | modules/06-transfer/dispatch/transfer-dispatch.html | — | — |

### 任务管理

| 业务术语 | 后端仓库 | 前端仓库 | 前端页面路径（ProtoHub） | 核心枚举 | 备注 |
|---------|---------|---------|------------------------|---------|------|
| 任务列表 | mdscr-order | mdscr-fe-admin | modules/07-task/list/task-list.html | TaskStatusEnum | work_info 主表 |
| 我的任务 | mdscr-order | mdscr-fe-admin | modules/07-task/my/task-my.html | — | 按用户过滤 |

### 合同签署

| 业务术语 | 后端仓库 | 前端仓库 | 前端页面路径（ProtoHub） | 备注 |
|---------|---------|---------|------------------------|------|
| 签署合同 | mdscr-order | mdscr-fe-admin | modules/08-contract/sign/contract-sign.html | — |

### 费用结算

| 业务术语 | 后端仓库 | 前端仓库 | 前端页面路径（ProtoHub） | 核心枚举 | 备注 |
|---------|---------|---------|------------------------|---------|------|
| 核验费用 | mdscr-order | mdscr-fe-admin | modules/09-billing/verify/billing-verify.html | — | order_fee 主表 |
| 费用减免 | mdscr-order | mdscr-fe-admin | modules/09-billing/reduce/billing-reduce.html | — | — |
| 补款列表 | mdscr-order | mdscr-fe-admin | modules/09-billing/repay/billing-repay.html | PayStatusEnum（WAIT_PAY/PAID/EXPIRED） | 补差金额 extra_pay_amount |

### 风控审核

| 业务术语 | 后端仓库 | 前端仓库 | 前端页面路径（ProtoHub） | 核心枚举 | 备注 |
|---------|---------|---------|------------------------|---------|------|
| 风控预警 | mdscr-order | mdscr-fe-admin | modules/10-risk/alert/risk-alert.html | — | — |
| 风控处理 | mdscr-order | mdscr-fe-admin | modules/10-risk/process/risk-process.html | ApprovalRouteEnum | — |
| 风险用户 | mdscr-order | mdscr-fe-admin | modules/10-risk/user/risk-user.html | — | — |

### 门店管理

| 业务术语 | 后端仓库 | 前端仓库 | 前端页面路径（ProtoHub） | 备注 |
|---------|---------|---------|------------------------|------|
| 门店下单 | mdscr-store | mdscr-fe-admin | modules/11-store/order/store-order.html | — |
| 门店工作台 | mdscr-store | mdscr-fe-admin | modules/01-dashboard/store/dashboard-store.html | — |
| 运营工作台 | mdscr-order | mdscr-fe-admin | modules/01-dashboard/overview/dashboard-overview.html | — |

### 全局共享资源

| 业务术语 | 类型 | 路径 | 影响范围 |
|---------|------|------|---------|
| 设计令牌 | CSS | shared/design-tokens/tokens.css | ⚠️ 所有页面（全局生效） |
| 布局组件 | JS | shared/components/layout.js | ⚠️ 所有页面（侧边栏+顶栏） |
| 导航首页 | HTML | index.html | 新增/删除模块必须更新 |

---

## 模块总览

> 新增模块时，在本节追加一行，并在下方补充完整映射。

| 模块 | 页面清单 | 核心数据表 | 主要影响范围 |
|------|---------|----------|-------------|
| 00-login | 登录页 | 用户认证 | 所有需登录的页面 |
| 01-dashboard | 运营工作台 / 门店工作台 | order_info / car_info | 各业务模块汇总入口 |
| 02-order | 订单列表 / 取车 / 还车 / 退款 / 预留 | **order_info**（核心） | 车辆、车务、费用、风控、合同 |
| 03-vehicle | 车辆列表 / 详情 / 预警 | **car_info** | 订单、车务、调拨 |
| 04-pickup-return | 取还车验车 | order_info + car_info | 订单状态、费用结算 |
| 05-car-ops | 洗车 / 加油 / 保养 / 整备 | work_info + car_info | 车辆状态、订单关联 |
| 06-transfer | 调拨任务 / 调度任务 | car_info | 车辆列表、门店管理 |
| 07-task | 任务列表 / 我的任务 | **work_info** | 各业务模块触发 |
| 08-contract | 签署合同 | order_info | 订单状态 |
| 09-billing | 核验费用 / 减免 / 补款 | **order_info + order_fee** | 订单、合同 |
| 10-risk | 风控预警 / 处理 / 风险用户 | order_info + 风控规则 | 订单、取还车 |
| 11-store | 门店下单 | order_info | 订单列表 |

---

## 详细数据流向映射

### 00-login 登录页

| 项目 | 内容 |
|------|------|
| **数据来源** | 用户认证系统（原型：本地 JS 校验） |
| **核心展示字段** | 用户名、密码、登录按钮 |
| **上游依赖** | 无 |
| **下游影响** | 所有需登录页面的鉴权状态 |
| **关联页面** | 全部（登录态失效时跳转至此） |

---

### 01-dashboard 工作台

#### overview 运营工作台

| 项目 | 内容 |
|------|------|
| **数据来源** | order_info（订单汇总）、car_info（车辆汇总）、work_info（任务汇总） |
| **核心展示字段** | 今日订单数、今日取车、今日还车、异常订单、车辆在线数、待处理任务 |
| **上游依赖** | 02-order（订单数据）、03-vehicle（车辆数据）、07-task（任务数据） |
| **下游影响** | 无（纯展示汇总） |
| **关联页面** | 02-order/list（点击订单跳转）、07-task/list（点击任务跳转） |

#### store 门店工作台

| 项目 | 内容 |
|------|------|
| **数据来源** | 同运营工作台，但范围限定当前门店 |
| **核心展示字段** | 本门店今日订单、待取车、待还车、车辆状态 |
| **上游依赖** | 02-order、03-vehicle（限定门店维度） |
| **下游影响** | 无 |
| **关联页面** | 02-order/list（门店过滤）、11-store/order（门店下单） |

---

### 02-order 订单管理（⚡ 核心模块）

> ⚠️ **订单模块是数据中枢**，绝大多数模块都依赖 order_info 表。
> 修改订单相关字段（如订单状态、订单标签）时，必须检查所有下游页面。

#### list 订单列表

| 项目 | 内容 |
|------|------|
| **数据来源** | **order_info**（主表） |
| **核心展示字段** | 马达订单号、渠道订单号、订单来源、订单类型、6个订单标签（状态/支付/免押/合同/渠道/保险）、客户信息、车辆信息、取还车信息、订单状态、租期、任务信息、下单时间、实际取还时间 |
| **上游依赖** | 无（顶层入口） |
| **下游影响** | 02-order/pickup、02-order/return、08-contract/sign、09-billing/verify、10-risk/process |
| **关联页面** | **所有订单相关操作页**（取车/还车/退款/预留/合同/费用/风控） |

#### pickup 订单取车

| 项目 | 内容 |
|------|------|
| **数据来源** | order_info（订单状态变更）、car_info（车辆状态变更） |
| **核心展示字段** | 订单信息、取车时间、车辆检查项、客户签字 |
| **上游依赖** | 02-order/list（订单数据） |
| **下游影响** | 订单状态变更 → 09-billing（费用启动计算）、04-pickup-return（验车） |
| **关联页面** | 04-pickup-return/inspect、09-billing/verify |

#### return 订单还车

| 项目 | 内容 |
|------|------|
| **数据来源** | order_info（订单状态变更）、car_info（车辆状态变更） |
| **核心展示字段** | 订单信息、还车时间、里程、油量、车辆检查项 |
| **上游依赖** | 02-order/list |
| **下游影响** | 订单状态变更 → 09-billing（费用结算）、05-car-ops/prep（整备触发） |
| **关联页面** | 04-pickup-return/inspect、09-billing/verify、05-car-ops/prep |

#### refund 订单退款

| 项目 | 内容 |
|------|------|
| **数据来源** | order_info + order_fee（费用数据） |
| **核心展示字段** | 退款金额、退款原因、退款状态 |
| **上游依赖** | 02-order/list、09-billing/verify |
| **下游影响** | 订单状态（已取消/已退款） |
| **关联页面** | 09-billing/verify、09-billing/repay |

#### reserve 短期预留

| 项目 | 内容 |
|------|------|
| **数据来源** | order_info（预留状态） |
| **核心展示字段** | 预留订单号、预留时长、预留状态 |
| **上游依赖** | 02-order/list |
| **下游影响** | 车辆状态（预留中不可接单） |
| **关联页面** | 03-vehicle/list（车辆状态） |

---

### 03-vehicle 车辆管理

#### list 车辆列表

| 项目 | 内容 |
|------|------|
| **数据来源** | **car_info**（主表） |
| **核心展示字段** | 车牌号、车型、状态（可用/租赁中/维修中/预警）、所在门店 |
| **上游依赖** | 02-order（订单占用车辆时状态变更）、05-car-ops（车务占用时状态变更） |
| **下游影响** | 02-order/pickup（取车车辆选择）、06-transfer（调拨车辆选择） |
| **关联页面** | 03-vehicle/detail、02-order/pickup、06-transfer/list |

#### detail 车辆详情

| 项目 | 内容 |
|------|------|
| **数据来源** | car_info + order_info（历史订单）+ work_info（维修记录） |
| **核心展示字段** | 车辆基础信息、当前状态、历史订单、维修/保养记录 |
| **上游依赖** | 03-vehicle/list |
| **下游影响** | 无（纯展示） |
| **关联页面** | 05-car-ops（发起车务）、02-order（查看历史订单） |

#### alert 车辆预警

| 项目 | 内容 |
|------|------|
| **数据来源** | car_info（预警规则触发） |
| **核心展示字段** | 预警类型、预警车辆、预警时间、处理状态 |
| **上游依赖** | 03-vehicle/list（车辆数据） |
| **下游影响** | 05-car-ops（触发整备/维修）、07-task（生成处理任务） |
| **关联页面** | 05-car-ops/prep、05-car-ops/maintain、07-task/list |

---

### 04-pickup-return 取还车验车

#### inspect 取还车验车

| 项目 | 内容 |
|------|------|
| **数据来源** | order_info + car_info（取还车时的车辆状态快照） |
| **核心展示字段** | 验车照片、车损记录、里程、油量、验车结果 |
| **上游依赖** | 02-order/pickup、02-order/return |
| **下游影响** | 09-billing（车损费用）、10-risk（异常验车记录） |
| **关联页面** | 09-billing/verify、10-risk/process |
| **文件路径** | `modules/04-pickup-return/inspect/pickup-inspect.html` |

---

### 05-car-ops 车务管理

> 车务模块的操作结果会反馈到车辆状态（03-vehicle）。

#### wash 洗车任务

| 项目 | 内容 |
|------|------|
| **数据来源** | work_info（洗车工单） |
| **上游依赖** | 03-vehicle/alert（预警触发）、05-car-ops/prep（整备触发） |
| **下游影响** | 03-vehicle/list（车辆状态更新为可用） |
| **关联页面** | 03-vehicle/list、07-task/list |

#### fuel 加油任务

| 项目 | 内容 |
|------|------|
| **数据来源** | work_info + car_info |
| **上游依赖** | 02-order/return（还车时油量检查） |
| **下游影响** | 03-vehicle/list、09-billing（加油费用） |
| **关联页面** | 09-billing/verify |

#### maintain 保养维修

| 项目 | 内容 |
|------|------|
| **数据来源** | work_info + car_info |
| **上游依赖** | 03-vehicle/alert（预警触发） |
| **下游影响** | 03-vehicle/list（车辆状态）、09-billing（维修费用） |
| **关联页面** | 03-vehicle/alert、09-billing/verify |

#### prep 整备车辆

| 项目 | 内容 |
|------|------|
| **数据来源** | work_info + car_info |
| **上游依赖** | 02-order/return（还车后触发整备） |
| **下游影响** | 03-vehicle/list（整备完成后状态变为可用） |
| **关联页面** | 03-vehicle/list、02-order/list（可用车辆数） |

---

### 06-transfer 调拨调度

#### list 调拨任务

| 项目 | 内容 |
|------|------|
| **数据来源** | car_info（调拨车辆）+ 门店信息 |
| **上游依赖** | 03-vehicle/list（选择调拨车辆） |
| **下游影响** | 03-vehicle/list（车辆所在门店变更）、11-store/order（目标门店订单能力） |
| **关联页面** | 03-vehicle/list、11-store/order |

#### dispatch 调度任务

| 项目 | 内容 |
|------|------|
| **数据来源** | car_info + 实时位置 |
| **上游依赖** | 03-vehicle/list |
| **下游影响** | 03-vehicle/list（调度后状态） |
| **关联页面** | 03-vehicle/list |

---

### 07-task 任务管理

#### list 任务列表

| 项目 | 内容 |
|------|------|
| **数据来源** | **work_info**（主表） |
| **上游依赖** | 03-vehicle/alert、05-car-ops（各车务操作生成任务）、10-risk（风控生成处理任务） |
| **下游影响** | 各业务模块（任务完成后状态回写） |
| **关联页面** | 几乎全部（任务来源分散在各模块） |

#### my 我的任务

| 项目 | 内容 |
|------|------|
| **数据来源** | work_info（按当前用户过滤） |
| **上游依赖** | 07-task/list |
| **下游影响** | 同 07-task/list |
| **关联页面** | 07-task/list |

---

### 08-contract 合同签署

#### sign 签署合同

| 项目 | 内容 |
|------|------|
| **数据来源** | order_info（订单关联）+ 合同模板 |
| **上游依赖** | 02-order/list（选择订单签署合同） |
| **下游影响** | 02-order/list（订单标签「是否签署合同」更新） |
| **关联页面** | 02-order/list（订单标签展示） |

---

### 09-billing 费用结算

> ⚠️ **费用模块依赖 order_info 和 order_fee**，订单模块的字段变更可能影响费用计算逻辑。

#### verify 核验费用

| 项目 | 内容 |
|------|------|
| **数据来源** | **order_fee**（主表）+ order_info |
| **核心展示字段** | 订单号、费用明细（租金/保险费/服务费/油费/车损费）、应收金额、已收金额 |
| **上游依赖** | 02-order/list、04-pickup-return（验车车损）、05-car-ops（加油/维修费用） |
| **下游影响** | 02-order/list（订单欠款状态） |
| **关联页面** | 02-order/list、04-pickup-return/inspect、05-car-ops/fuel、05-car-ops/maintain |

#### reduce 费用减免

| 项目 | 内容 |
|------|------|
| **数据来源** | order_fee + 减免规则 |
| **上游依赖** | 09-billing/verify |
| **下游影响** | 09-billing/verify（费用重新计算） |
| **关联页面** | 09-billing/verify |

#### repay 补款列表

| 项目 | 内容 |
|------|------|
| **数据来源** | order_fee（欠款记录） |
| **核心枚举** | PayStatusEnum（WAIT_PAY / PAID / EXPIRED） |
| **上游依赖** | 09-billing/verify（费用核验后生成欠款） |
| **下游影响** | 02-order/list（订单支付状态更新） |
| **关联页面** | 02-order/list、09-billing/verify |

---

### 10-risk 风控审核

#### alert 风控预警

| 项目 | 内容 |
|------|------|
| **数据来源** | 风控规则引擎 + order_info |
| **上游依赖** | 02-order/list（订单数据接入风控规则） |
| **下游影响** | 10-risk/process（生成处理任务）、02-order/list（订单风控标记） |
| **关联页面** | 02-order/list、10-risk/process、07-task/list |

#### process 风控处理

| 项目 | 内容 |
|------|------|
| **数据来源** | 风控预警记录 + order_info |
| **核心枚举** | ApprovalRouteEnum（STORE_SUPERVISOR / STORE_SUPERVISOR_AREA_DIRECTOR） |
| **上游依赖** | 10-risk/alert |
| **下游影响** | 02-order/list（订单状态）、07-task（处理任务关闭） |
| **关联页面** | 02-order/list、07-task/list |

#### user 风险用户

| 项目 | 内容 |
|------|------|
| **数据来源** | 风控用户名单 + order_info（历史订单） |
| **上游依赖** | 10-risk/alert（标记风险用户） |
| **下游影响** | 02-order/list（新订单自动风控标记） |
| **关联页面** | 02-order/list（下单时校验） |

---

### 11-store 门店管理

#### order 门店下单

| 项目 | 内容 |
|------|------|
| **数据来源** | order_info（新增）+ car_info（可选车辆） |
| **上游依赖** | 03-vehicle/list（可选车辆）、01-dashboard/store（门店信息） |
| **下游影响** | 02-order/list（新增订单）、03-vehicle/list（车辆状态占用） |
| **关联页面** | 02-order/list、03-vehicle/list |

---

## 改动影响速查表

> 改了 A 模块，还要检查哪些模块？用这张表快速查。

| 如果你改了... | 必须检查的关联模块 |
|-------------|-------------------|
| **02-order/list**（订单列表字段/标签） | pickup、return、08-contract/sign、09-billing/verify、10-risk/process、11-store/order |
| **02-order/pickup**（取车逻辑） | 03-vehicle/list（车辆状态）、09-billing/verify（费用启动） |
| **02-order/return**（还车逻辑） | 03-vehicle/list、05-car-ops/prep（整备触发）、09-billing/verify（费用结算） |
| **03-vehicle/list**（车辆字段/状态） | 02-order/pickup（取车选车）、06-transfer/list（调拨选车）、11-store/order（门店下单选车） |
| **04-pickup-return/inspect**（验车项） | 09-billing/verify（车损费用）、10-risk/alert（异常记录） |
| **05-car-ops**（任意子页面） | 03-vehicle/list（车辆状态回写）、09-billing/verify（费用） |
| **09-billing/verify**（费用字段/逻辑） | 02-order/list（订单欠款状态）、09-billing/repay（补款列表） |
| **10-risk/alert**（风控规则展示） | 02-order/list（订单风控标记）、10-risk/process |
| **shared/design-tokens/tokens.css** | ⚠️ **所有页面**（全局生效） |
| **shared/components/layout.js** | ⚠️ **所有页面**（导航和高亮逻辑） |

---

## 更新记录

| 日期 | 更新内容 | 操作人 |
|------|---------|--------|
| 2026-06-04 | 新建文档，填入当前 13 个模块的初步映射 | 韦高鹏 |
| 2026-06-22 | v2.0 重构：新增业务术语-仓库/页面映射表（对齐 prd-writer v2.0），完善核心枚举，路径更新为新目录结构 | AI |
| 2026-06-22 | v2.1 路径修正：所有 HTML 文件路径对齐实际文件名（pickup-inspect/carops-*/transfer-dispatch/task-my/dashboard-overview/dashboard-store）；dashboard 路径修正为含子目录的完整路径 | AI |

> **操作人填写说明**：每次更新此文档后，在表格追加一行，注明日期、变更内容、你的名字。
