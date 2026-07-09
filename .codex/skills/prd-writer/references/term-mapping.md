# 术语映射表

> 加载时机：系统感知阶段需要定位业务模块对应的代码仓库时加载，或步骤 8 知识回流时加载以追加新映射。

业务术语和代码仓库/页面的对应关系。系统感知时使用此表定位模块。

| 业务术语 | 后端仓库 | 前端仓库 | 前端页面路径 | 核心枚举 |
|---------|---------|---------|------------|---------|
| 采购单 | LY-MDSCR/mdscr-purchase | mdscr-fe-admin | views/applyList/components/PurchaseOrder | PurchaseProgressEnum, PurchaseSettlementStatusEnum, FormStatusEnum |
| 需求单 | LY-MDSCR/mdscr-purchase | mdscr-fe-admin | views/applyList/components/RequirementOrder | RequirementTypeEnum, RequirementApplyStatusEnum, RequiresProgressEnum |
| 付款计划 | LY-MDSCR/mdscr-purchase | mdscr-fe-admin | views/paymentPlan | PaymentStatusEnum, PaymentTypeEnum, PrepaidStatusEnum |
| 结算单 | LY-MDSCR/mdscr-purchase | mdscr-fe-admin | views/applyList/components/SettlementOrder | SettlementStatusEnum, SettlementTypeEnum, PurchaseSettlementStatusEnum |
| 订单 | LY-MDSCR/mdscr-order | mdscr-fe-admin | views/sale/order | CarRentStatusEnum, BusinessTypeEnum, CarTypeEnum |
| 订单退款（原路） | LY-MDSCR/mdscr-order | mdscr-fe-admin | views/sale/order/orderRefundList/components/FeeAndDepositOriginalRefund | OrderRefundStatusEnum, FeeRefundTypeEnum, OrderRefundTypeEnum |
| 订单退款（非原路） | LY-MDSCR/mdscr-order | mdscr-fe-admin | views/sale/order/orderRefundList/components/FeeNonOriginalRefund | OrderUnOriginalRefundPayStatusEnum, OrderUnOriginalRefundPayTypeEnum |
| 退款审批 | LY-MDSCR/mdscr-order | mdscr-fe-admin | views/auditList/components/OrderRefund | AuditStatusEnum, OrderRefundStatusEnum |
| 退款记录 | LY-MDSCR/mdscr-order | mdscr-fe-admin | views/sale/order/orderDetail/components/RefundRecord | OrderRefundStatusEnum, RefundNotifyCodeEnum |
| 退款通知 | LY-MDSCR/mdscr-order | — | — | RefundNotifyCodeEnum |
| 押金退款 | LY-MDSCR/mdscr-order | mdscr-fe-admin | views/sale/order/orderRefundList/components/CreditNoDepositRefund | OrderDepositRefundListQueryFunction |
| 加油/电费退款 | LY-MDSCR/mdscr-order | mdscr-fe-admin | views/sale/order/orderDetail/components/OilBatteryRefund | — |
| 退款附件/凭证 | LY-MDSCR/mdscr-order | — | — | AttachmentTypeEnum |
| 退款发起 | LY-MDSCR/mdscr-order | mdscr-fe-admin | views/applyList/components/OrderRefund | OrderRefundStatusEnum, RefundSourceEnum |
| 车辆管理 | LY-MDSCR/mdscr-vehicle | — | — | AssetCarStatusEnum, AssetCarBizTypeEnum |
| 车龄标签/车龄配置 | LY-MDSCR/mdscr-vehicle | mdscr-fe-admin | views/income/tagStrategyConfigList | CarAgeTagEnum |
| 车型/车型组 | LY-MDSCR/mdscr-vehicle | mdscr-fe-admin | views/income/tagStrategyConfigList | CarTypeEnum, CarAgeTagEnum |
| 渠道标签策略 | LY-MDSCR/mdscr-vehicle | mdscr-fe-admin | views/income/channelTagManage | — |
| 活动管理 | LY-MDSCR/mdscr-revenue | mdscr-fe-admin | — | — |
| 收益调价 | LY-MDSCR/mdscr-revenue | mdscr-fe-admin | — | — |
| 资产退出 | LY-MDSCR/mdscr-purchase | mdscr-fe-admin | views/applyList/components/AssetExitOrder | AssetRevocateTypeEnum, AssetRevocateFeeEnum |
| 车辆备品 | LY-MDSCR/mdscr-purchase | mdscr-fe-admin | views/vehicleSpare | AssetCarMaterialBoundTypeEnum |
| 门店耗材 | LY-MDSCR/mdscr-purchase | mdscr-fe-admin | views/storeConsumable | — |
| 固定资产 | LY-MDSCR/mdscr-purchase | mdscr-fe-admin | views/fixedAsset | AssetTypeEnum, AssetLevelEnum |
| 门店物资设置 | LY-MDSCR/mdscr-purchase | mdscr-fe-admin | views/storeMaterialConfig | — |
| 应急收车 | — | mdscr-fe-admin | views/applyList/components/EmergencyTask | — |
| 车辆维修 | LY-MDSCR/mdscr-maintenance | mdscr-fe-bff-maintenance | views/applyList/components/VehicleRepair | RepairTypeEnum, MaintenanceSettleStatusEnum |
| 审核列表 | — | mdscr-fe-admin | views/auditList | AuditStatusEnum |
| 申请列表 | — | mdscr-fe-admin | views/applyList | — |
| 采购工作台 | — | mdscr-fe-admin | views/purchaseWorkbench | — |
| 数据导出 | — | mdscr-fe-admin | views/dataExportLogs | — |
| 违章管理 | LY-MDSCR/mdscr-order | mdscr-fe-admin | — | CarViolationStatusEnum, CarViolationDepositStatusEnum |
| 订单取消 | LY-MDSCR/mdscr-order | mdscr-fe-admin | — | CancelTypeEnum, CancelReasonCodeEnum |
| 车辆调度 | LY-MDSCR/mdscr-dispatch | — | — | — |
| 车辆交付 | LY-MDSCR/mdscr-vehicle | — | — | CarDeliveryStatusEnum, CarDeliveryImportStatusEnum |
| 设备管理 | LY-MDSCR/mdscr-device | — | — | CarDeviceMessageTypeEnum, CarDeviceServiceStatusEnum |
| 财务中台 | LY-MDSCR/mdscr-finance | — | — | — |
| 占位/锁车 | LY-MDSCR/mdscr-occupy | — | — | — |
| 工作用车 | — | mdscr-fe-admin | views/applyList/components/WorkVehicle | WorkVehicleTypeEnum, FerryReasonEnum |
| 工作用车审批 | — | mdscr-fe-admin | views/auditList/components/WorkVehicle | AuditStatusEnum |
| 车辆调拨 | — | mdscr-fe-admin | views/applyList/components/VehicleDispatch | CAR_ALLOCATE_APPLY |
| 车辆调拨审批 | — | mdscr-fe-admin | views/auditList/components/VehicleDispatch | AuditStatusEnum |
| 预约用车（短预留） | — | mdscr-fe-admin | views/applyList/components/ShortReserve | CAR_STOCK_RESERVE |
| 车辆调度列表 | LY-MDSCR/mdscr-dispatch | mdscr-fe-admin | views/vehicle/vehicleManage/vehicleDeployList | — |
| 调度任务列表 | LY-MDSCR/mdscr-dispatch | mdscr-fe-admin | views/scheduling/taskList | TaskStatusEnum |
| 油损费用 | LY-MDSCR/mdscr-order | mdscr-fe-admin | views/sale/order/orderList/components/ConfirmFee | — |
| 油损自动扣款 | LY-MDSCR/mdscr-order | mdscr-fe-admin | views/sale/order/orderList/components/OilDamageDeduction | — |
| 补款转押金扣款 | LY-MDSCR/mdscr-order | mdscr-fe-admin | views/sale/order | DepositDeductionEnum [待确认] |
| 飞猪合并扣款限制 | LY-MDSCR/mdscr-order | mdscr-fe-admin | views/sale/order | FeizhuDeductionLimitEnum [待确认] |
| 油电费计算明细 | LY-MDSCR/mdscr-order | mdscr-fe-admin | views/sale/order/orderDetail/components/FeeTable + views/sale/order/orderDetail/components/ReturnSettleFeesRecord | — [自动 2026-07-01] |

## 映射表中标注"待确认"的处理

当映射表中标注了"待确认"（如车龄标签的前端仓库），说明上次 PRD 生成时未能定位到确切的前端仓库。需要在系统感知阶段（步骤 3）用脚本 `hub_client.py list-repos --search {关键词} --indexed` 来定位。找到后更新映射表。

## 使用方式

1. 从用户输入中提取业务关键词
2. 在映射表第一列查找匹配项（支持模糊匹配，如"退款"匹配"订单退款""退款审批""退款通知"等）
3. 用对应的后端仓库查枚举和执行流，用前端仓库 + 前端页面路径查页面结构
4. 用核心枚举名查 Hub 的 `context` 获取枚举值
5. **映射表未命中时**：用脚本 `hub_client.py query --query {关键词}` 搜索，在返回结果中识别相关仓库和页面

## 映射表维护（自进化规则）

- 每次 PRD 生成完成后，如果涉及了新模块或新页面，将新的术语映射追加到此表
- 标注"待确认"的条目，在下次定位成功后更新为确切值
- 如果 Hub 中出现了映射表未收录的仓库或页面，在下次系统感知时自动补充
- 映射表中的"核心枚举"列用于快速定位该模块的业务词汇，不需要穷举所有枚举
