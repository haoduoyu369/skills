---
name: historical-context-query
description: >
  在做任何需求分析、PRD 编写、原型设计之前，先查询历史上下文的专用 skill。
  包含两个子能力：
  ① gitnexus-hub 查代码逻辑（优先用术语映射表定位仓库 + Cypher 模板构造查询）；
  ② toca-wiki 查历史需求（优先用 MCP 工具，降级用浏览器脚本）。
  最终输出结构化「历史上下文摘要」供后续分析使用。
  触发词：查历史代码、查代码逻辑、查瓦力需求、读瓦力、参考历史需求、系统现状、gitnexus、
         hub 查询、先查代码、Phase -1、历史上下文、context query。
---

# 历史上下文查询 Skill（Phase -1）

## 定位

在着手**任何需求分析、PRD 编写、原型设计**之前，先把「现有系统长什么样」搞清楚。

本 skill 解决的核心问题：
- 新需求与现有系统可能冲突 → 先查代码再分析，避免方案写完发现和已有逻辑打架
- 历史需求有可以复用的设计方案 → 先查瓦力，避免重复设计已解决的问题
- 枚举值/字段名/接口名写错 → 直接从代码里取，不靠记忆

---

## 工作流

```
输入需求关键词
    │
    ├── Step -1.1  查 gitnexus-hub 代码逻辑（必做）
    │     ├── a. 术语映射表定位仓库
    │     ├── b. Cypher 模板查结构
    │     └── c. context 获取源码/枚举
    │
    ├── Step -1.2  查 toca-wiki 历史需求（可选）
    │     ├── 优先：toca-wiki skill
    │     └── 降级：node 浏览器脚本
    │
    └── Step -1.3  整合输出历史上下文摘要
```

---

## Step -1.1 — 查询 gitnexus-hub 代码逻辑（必做）

### 第一步：术语映射表定位仓库

从用户输入中提取**业务关键词**，在下方术语映射表中查找对应仓库和页面路径。

**映射表未命中时**：用 Hub `query` 工具搜索英文关键词，从返回结果中识别仓库。

```
映射表命中 → 用表中的后端仓库查枚举/执行流，用前端仓库+页面路径查页面结构
映射表未命中 → 用 Hub `query` 工具搜索关键词，识别仓库后走后续步骤
```

### 第二步：按 Cypher 模板构造查询

**Hub 访问方式**（两种，按场景选择）：

1. **MCP 工具**（推荐）：multica 平台封装了 `gitnexus-hub` skill，约束了调用层级深度，可直接使用以下 MCP 工具（使用前先用 ToolSearch 加载）：
   - `mcp__gitnexus-hub__cypher` — 图数据库 Cypher 查询
   - `mcp__gitnexus-hub__context` — 获取符号源码
   - `mcp__gitnexus-hub__query` — 全文搜索
2. **hub_client.py 脚本**（备选）：MCP 工具不可用或需要精确控制参数时使用
   ```bash
   python3 ~/.workbuddy/skills/prd-writer/scripts/hub_client.py cypher --repo {仓库} --query '{Cypher}'
   ```

#### 查枚举值（两步法）

```json
// 第一步：列出枚举文件
{
  "name": "cypher",
  "arguments": {
    "repo": "{后端仓库，如 LY-MDSCR/mdscr-order}",
    "query": "MATCH (e:Enum) WHERE e.filePath CONTAINS 'enums' AND e.name CONTAINS '{枚举名关键词}' RETURN e.name, e.filePath ORDER BY e.name"
  }
}

// 第二步：获取枚举源码（提取 code → 中文描述映射）
{
  "name": "context",
  "arguments": {
    "repo": "{后端仓库}",
    "uid": "Enum:{第一步 filePath}:{枚举类名}",
    "content": true
  }
}
```

> ⚠️ 如果 context 返回 `"status": "ambiguous"`，从 candidates 中选 kind 为空字符串的条目（Enum 本体），不选 kind 为 "Constructor" 的条目。

#### 查前端页面结构

```json
{
  "name": "cypher",
  "arguments": {
    "repo": "{前端仓库，如 LY-MDSCR/mdscr-fe-admin}",
    "query": "MATCH (f:File) WHERE f.filePath CONTAINS '{页面路径关键词}' RETURN f.filePath LIMIT 30"
  }
}
```

#### 查前端 Vue 组件源码（原型生成用）

```json
// 第一步：文件列表
{
  "name": "cypher",
  "arguments": {
    "repo": "{前端仓库}",
    "query": "MATCH (f:File) WHERE f.filePath CONTAINS '{页面路径}' RETURN f.filePath LIMIT 20"
  }
}

// 第二步：获取源码（template + script + style）
{
  "name": "context",
  "arguments": {
    "repo": "{前端仓库}",
    "uid": "File:{第一步 filePath}",
    "content": true
  }
}
```

#### 查后端执行流（关键业务逻辑）

```json
{
  "name": "query",
  "arguments": {
    "repo": "{后端仓库}",
    "search_query": "{英文关键词，如 upgrade car free limit}",
    "limit": 10,
    "content": false
  }
}
```

#### 查影响面（改动扩散分析）

```json
{
  "name": "impact",
  "arguments": {
    "repo": "{后端仓库}",
    "target": "{目标符号名，如 UpgradeCarApplyService}",
    "direction": "upstream",
    "depth": 2
  }
}
```

### 第三步：提取关键信息

从 Hub 返回结果中提取：

| 维度 | 提取内容 |
|------|---------|
| **枚举值** | 完整的 code → 中文描述映射，用于后续 PRD 中的枚举值引用 |
| **数据字段** | 现有数据模型字段，确认新字段是否已存在 |
| **接口参数** | 现有接口入参/出参，确认变更范围 |
| **业务逻辑** | 现有校验规则、条件分支，避免新需求与之冲突 |
| **页面结构** | 现有页面的组件层级，确认新增内容的插入位置 |
| **代码缺陷** | 在查询过程中发现的已知 Bug 或缺失逻辑（主动标记） |

### Hub 查询注意事项

- 优先用**英文关键词**或代码中的类名/函数名搜索（中文效果差）
- 返回空结果时：换关键词重试，或用映射表中的枚举名代替
- Hub 完全不可用时：跳过代码查询，降级为「从零追问」模式（在摘要中注明"Hub 不可用"）
- **并行查询**：不同仓库的查询可以并发发出，节省时间

---

## Step -1.2 — 查询 toca-wiki 历史需求（可选）

### 触发条件

满足以下任一条件时执行：
- 用户提供了瓦力需求链接（`toca.17u.cn/wiki?fid=xxx`）
- 用户说「参考之前那个需求」「有历史需求可以看吗」
- 本次需求是历史需求的迭代版本

不满足时跳过，不主动去搜索。

### 执行方式（优先级从高到低）

**方式 1 — toca-wiki skill**（推荐）

```bash
node ~/.workbuddy/skills/toca-wiki/scripts/fetch-wiki.js "<瓦力需求URL>"
```

脚本会：
1. 自动读取 `~/.toca-wiki/api-key` 注入 Cookie 鉴权（无需手动登录）
2. 如果 API Key 不生效，自动降级弹出浏览器手动登录一次
3. 返回需求文档完整文本（含图片链接）

> 首次运行需约 1 分钟安装 Playwright + Chromium，之后秒级执行。

**方式 2 — 直接使用 WebFetch**（降级备选）

```
URL 可访问时：用 WebFetch 直接抓取页面 HTML
URL 需要鉴权时：回到方式 1
```

### 提取内容

从瓦力需求文档中提取：

```markdown
- 需求背景：当时要解决什么问题
- 设计方案：采用了什么方案，选择了什么路径
- 关键决策：有哪些方案被否定，原因是什么
- 遗留 TODO：当时未解决或标注"下期做"的内容
- 相关数据字段/接口：已定义的规范
```

---

## Step -1.3 — 整合历史上下文摘要

将 Step -1.1 和 Step -1.2 的结果整合，输出以下格式的摘要，供 Phase 0 使用：

```markdown
## 历史上下文摘要

### 涉及仓库
| 仓库 | 查询内容 | 关键发现 |
|------|---------|---------|
| LY-MDSCR/mdscr-order | 升级枚举、业务逻辑 | UpgradeCarApplyStatusEnum 六态、当前阈值 ¥300 |
| LY-MDSCR/mdscr-fe-admin | 页面结构 | auditList 审批列表含 11 列、弹窗 800px |

### 关键代码逻辑
- **{业务模块}**：[系统] {逻辑描述，e.g. MinApplyFee = ¥300，差值<300不触发审批}
- **{页面/组件}**：[系统] {现有实现，e.g. 升级弹窗仅订单状态=待取车时展示}

### 代码缺陷 / 注意点
- [系统] {发现的 Bug 或缺失逻辑，如"无每日限额字段，无补差价分流"}
- [系统] {需要在需求中一并修复的历史遗留问题}

### 历史需求参考（如有）
- 需求链接：{URL}
- 关键设计决策：{可借鉴的决策}
- 已被否定方案：{及其原因}
- 遗留 TODO：{当时未解决的问题}

### 对本次需求的影响
- {影响点 1，e.g. "字段 X 需新增，不能复用现有字段"}
- {影响点 2，e.g. "审批流已有 LightFlow 配置，本次只需新增节点"}
```

---

## 术语映射表（自营租车系统 MDSCR）

业务关键词 → 仓库 + 页面路径速查表。

| 业务术语 | 后端仓库 | 前端仓库 | 前端页面路径 | 核心枚举 |
|---------|---------|---------|------------|---------|
| 订单 | LY-MDSCR/mdscr-order | mdscr-fe-admin | views/sale/order | CarRentStatusEnum, BusinessTypeEnum |
| 订单退款（原路） | LY-MDSCR/mdscr-order | mdscr-fe-admin | views/sale/order/orderRefundList/components/FeeAndDepositOriginalRefund | OrderRefundStatusEnum, FeeRefundTypeEnum |
| 订单退款（非原路） | LY-MDSCR/mdscr-order | mdscr-fe-admin | views/sale/order/orderRefundList/components/FeeNonOriginalRefund | OrderUnOriginalRefundPayStatusEnum |
| 退款审批 | LY-MDSCR/mdscr-order | mdscr-fe-admin | views/auditList/components/OrderRefund | AuditStatusEnum |
| 退款记录 | LY-MDSCR/mdscr-order | mdscr-fe-admin | views/sale/order/orderDetail/components/RefundRecord | OrderRefundStatusEnum |
| 保险加购 | LY-MDSCR/mdscr-order | mdscr-fe-admin | views/sale/order/orderDetail/components/InsuranceInfo | InsuranceTypeEnum, FeeTypeEnum |
| 车型升级 | LY-MDSCR/mdscr-order | mdscr-fe-admin | views/sale/order/orderList/components/LineOperation/hooks/useVehicleModelUpgrade.ts | UpgradeCarApplyStatusEnum |
| 升级审批 | LY-MDSCR/mdscr-order | mdscr-fe-admin | views/auditList/components/UpgradeCar | UpgradeCarApplyStatusEnum |
| 升级申请 | LY-MDSCR/mdscr-order | mdscr-fe-admin | views/applyList/components/UpgradeCar | UpgradeCarApplyStatusEnum |
| 违章管理 | LY-MDSCR/mdscr-order | mdscr-fe-admin | — | CarViolationStatusEnum |
| 门店管理 | LY-MDSCR/mdscr-store | mdscr-fe-store-wx | — | StoreStatusEnum |
| 车辆管理 | LY-MDSCR/mdscr-vehicle | — | — | AssetCarStatusEnum, AssetCarBizTypeEnum |
| 车型/车型组 | LY-MDSCR/mdscr-vehicle | — | — | CarTypeEnum |
| 设备管理（GPS） | LY-MDSCR/mdscr-device | mdscr-fe-admin | views/device/gps | CarDeviceMessageTypeEnum |
| 调度管理 | LY-MDSCR/mdscr-dispatch | mdscr-fe-admin | views/scheduling | — |
| 占用/锁车 | LY-MDSCR/mdscr-occupy | — | — | — |
| 收入/收益 | LY-MDSCR/mdscr-revenue | mdscr-fe-admin | — | — |
| 财务管理 | LY-MDSCR/mdscr-finance | — | — | — |
| 车辆维护 | LY-MDSCR/mdscr-maintenance | — | — | MaintenanceStatusEnum |
| 门店工作台 | — | mdscr-fe-admin | views/workbenchStore | — |
| 监督管理 | — | mdscr-fe-admin | views/supervision | — |
| 费用合计 | LY-MDSCR/mdscr-order | mdscr-fe-admin | views/sale/order/orderDetail/components/FeeDetail | FeeTypeEnum |
| 短信通知 | LY-MDSCR/mdscr-order | — | — | — |
| **升级类型** | mdscr-order: UpgradeTypeEnum | mdscr-fe-admin | 订单列表→车型升级弹窗 | FREE_UPGRADE / FREE_UPGRADE_PAY_DIFF |
| **补差金额** | mdscr-order: extra_pay_amount | mdscr-fe-admin | 审批列表/订单详情→创单记录 | — |
| **支付状态** | mdscr-order: PayStatusEnum | mdscr-fe-admin | 订单详情→创单记录→补款 | WAIT_PAY / PAID / EXPIRED |
| **车型分组** | mdscr-vehicle: car_series.group_id | — | 审批列表 | TETravelMDSCRVehicle 库查询 |
| **审批路由** | mdscr-order: ApprovalRouteEnum | mdscr-fe-admin: auditList | 审批列表 | STORE_SUPERVISOR / STORE_SUPERVISOR_AREA_DIRECTOR |
| **区总审批** | mdscr-store: AREA_DIRECTOR 角色 | — | 审批列表 | 门店→城市→区域→AREA_DIRECTOR 匹配 |
| **限额配置** | mdscr-opms: OrderSystemConfig | — | 配置管理 | upgrade_daily_limit_per_day / upgrade_total_limit_max |

**前端仓库清单**：
- `mdscr-fe-admin` — 通用后台管理（采购、订单、审核等）
- `mdscr-fe-store-wx` — 门店微信小程序
- `mdscr-fe-store-admin` — 门店管理后台
- `mdscr-fe-wap` — 用户端 WAP
- `mdscr-fe-wap-biz` — 业务端 WAP
- `mdscr-fe-mall-wx` — 商城小程序
- `mdscr-fe-pms-wx` / `mdscr-fe-pms-alipay` — PMS 端小程序

---

## 适用场景与跳过条件

| 场景 | 建议 |
|------|------|
| 迭代需求（修改现有功能） | ✅ 必须执行 -1.1，查清楚现有逻辑再分析 |
| 全新需求（与现有系统无关联） | ⚠️ 可选，但建议做一轮映射表匹配 |
| 用户提供了瓦力链接 | ✅ 执行 -1.2 |
| 用户说「不需要参考历史」 | ⬜ 跳过，直接进入需求分析 |
| Hub 连接超时/不可用 | ⬜ 跳过 -1.1，摘要中注明「Hub 不可用，未查代码逻辑」 |

---

## 快速查询检查清单

每次执行 Step -1.1 时，对照以下清单确认查询覆盖度：

- [ ] 已在术语映射表中匹配业务关键词
- [ ] 已查目标模块的**业务枚举**（code → 中文描述）
- [ ] 已查**现有数据字段**（避免新增字段已存在）
- [ ] 已查**前端页面结构**（确认修改位置）
- [ ] 已查**关键后端逻辑**（Service / Controller 层）
- [ ] 已识别**代码缺陷**（顺手记录在摘要 "代码缺陷" 区域）

---

## 参考配置

- **gitnexus-hub MCP 地址**（正式环境）：`http://ibd.travel.t.17usoft.com/gitnexus/mcp`
- **multica skill 封装**：multica 平台封装了 `gitnexus-hub` skill，约束大模型调用 MCP 时的层级深度，推荐优先使用
- **toca-wiki 脚本路径**：`~/.workbuddy/skills/toca-wiki/scripts/fetch-wiki.js`
- **toca-wiki API Key 存放**：`~/.toca-wiki/api-key`
- **Hub 支持的仓库数量**：149 个（LY-MDSCR/ 前缀）
