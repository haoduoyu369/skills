# Pending 映射池（人工 review 后手动合并入 term-mapping.md）

> 新增时间：2025-06-25
> 关联需求：PRD-车型升级免费升级价格管控细化

## 新增术语

| 业务术语 | 后端仓库 | 前端仓库 | 前端页面路径 | 备注 |
|---------|---------|---------|------------|------|
| 双上限额度 | mdscr-order | — | — | 每日 ¥50 + 总价 ¥350 的免费升级免额框架 |
| 升级类型区分 | mdscr-order: UpgradeTypeEnum | mdscr-fe-admin: vehicle.ts | 车型升级弹窗 / 审批列表 / 申请列表 | FREE_UPGRADE / FREE_UPGRADE_PAY_DIFF |
| 补差价支付 | mdscr-order | mdscr-fe-admin | 车型升级弹窗 → 支付链接 | 超额部分用户线上支付后发车 |
| 区总审批 | mdscr-order: ApprovalRouteEnum | mdscr-fe-admin: auditList/UpgradeCar | 审批列表 | 超额+商务车/豪华车时增加区总节点 |
| 车型分组（商务车/豪华车） | mdscr-vehicle: car_series.group_id | — | — | 用于判断是否需要区总审批 |
| 计费车型ID | mdscr-order: billing_car_model_id | — | — | 升级后更新，续租/换车差价时取正确的日租金 |
| 企微通知模板 | mdscr-order: 通知模板 | — | — | 全免时触发，防止线下收费 |
| 换车差价记录 | mdscr-order: AdminOrderChangeCarService | — | — | 从换车当天10:00起算 |
| 限额配置 | mdscr-opms: OrderSystemConfig | — | — | upgrade_daily_limit(50) / upgrade_total_limit(350) |

---

> 新增时间：2026-07-01
> 关联需求：PRD-应急收车费与应急工单强绑定

## 新增术语

| 业务术语 | 后端仓库 | 前端仓库 | 前端页面路径 | 备注 |
|---------|---------|---------|------------|------|
| 应急工单（风控管理-应急收车列表） | 待确认 | mdscr-fe-admin | views/supervision [待确认] | 与"申请列表-应急收车(EmergencyTask)"不同，这是风控管理模块下的应急收车数据 |
| 发起补款 | mdscr-order [推断] | mdscr-fe-admin | views/sale/order/orderList/components/SupplementPayment/index.vue | 补款弹框主组件，含补款类型选择(el-select)+收款方式+金额+备注 |
| 补款费用类型枚举 | — | mdscr-fe-admin: @/enum/constantsEnum/sale.ts | SUPPLEMENT_FEE_TYPE (Map) | EMERGENCY_RETURN_CAR_FEE='应急收车费', UNEXPECT_VEHICLE_DAMAGE='车损费用', UNEXPECT_LEND_DRIVING_LICENSE='出借行驶证费用' 等 |
| 补款费用类型逻辑 | — | mdscr-fe-admin | views/sale/order/orderList/components/SupplementPayment/composables/useFeeType.ts | 从 SUPPLEMENT_FEE_TYPE Map 构建 feeTypeList，按渠道过滤 |
| 非车损补款表单 | — | mdscr-fe-admin | views/sale/order/orderList/components/SupplementPayment/components/CommonFeeForm.vue | 补款金额(input+元)+补款备注(textarea)，押金扣款时展示凭证上传 |

> 注：发起补款组件路径已通过 Hub 确认。风控管理-应急收车列表前端路径仍待确认（可能在 views/supervision 下）。
