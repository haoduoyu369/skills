---
name: rds-api-query
description: >-
  通过 TCDBA RDS HTTP 接口执行只读 SQL 并解析 JSON 结果。请求为 POST
  https://rdsapi.tcdba.17usoft.com/sql/manager/query，报文为连接元数据、
  `sql` 与可为空的 `tables` 组成的 JSON。仅需请求头 `x-auth-token` 鉴权（无需 Cookie）。
  在用户需要以接口替代浏览器控制台进行 RDS 查询、或提及 rdsapi / sql/manager/query 时使用。
  车辆库连接快照见本目录 violation-connection-reference.md；订单库见 order-connection-reference.md；门店/停车场库见 store-connection-reference.md；请求体说明见 api-payload-reference.md。
  库名与环境映射与 rds-database-query 技能一致。
---

# RDS 接口查询（HTTP）

用内部 RDS 查询 API 替代浏览器自动化，适合脚本化与 Agent 直接发请求。

## 接口

- **URL**：`https://rdsapi.tcdba.17usoft.com/sql/manager/query`
- **方法**：`POST`
- **Header**：
  - `Content-Type: application/json`（建议 UTF-8 正文）
  - `x-auth-token`：RDS 接口鉴权串，形如 `rds:<数字>:<十六进制片段>:<数字>:<数字>`；过期后替换

**说明**：当前口径下**不需要** `Cookie`，仅 `x-auth-token` 即可通过鉴权。

## x-auth-token 来源（按优先级）

1. 用户在本轮对话中粘贴的 `x-auth-token` 值（整串，无引号）
2. 环境变量 `RDS_X_AUTH_TOKEN`
3. 本技能目录下本地文件 `x-auth-token.txt`（单行）— 已列入 `.gitignore`，勿提交仓库

若返回鉴权失败，请用户在浏览器 **Network** 中打开同域下的查询请求，复制请求头里的 `x-auth-token` 更新 `x-auth-token.txt` 或环境变量。

## 请求体

- **字段说明**：见 [api-payload-reference.md](api-payload-reference.md)
- **`tables`**：允许为 **`{}`（空对象）**，无需携带控制台导出的大型表元数据
- **车辆库快照**：同目录 [violation-connection-reference.md](violation-connection-reference.md) 为 `TETravelMDSCRVehicle` / `car_violation` 示例。**订单库快照**：[order-connection-reference.md](order-connection-reference.md)（`TETravelMDSCROrder`）。**门店/停车场库快照**：[store-connection-reference.md](store-connection-reference.md)（`TETravelMDSCRStore` / `parking_lot`）。均含 `"tables": {}`；一般只需改 **`sql`** 与（若环境变化）连接相关字段。其它库需用户从控制台抓包替换 `databaseId`、`projectId`、`instanceIp` / `readInstanceIp`、`databaseName`、`environment` 等

**SQL 规则**（与 `rds-database-query` 一致）：

- 仅 `SELECT`；禁止 DML/DDL
- 默认 `LIMIT 100`，最大 `LIMIT 1000`，避免 `SELECT *`（除非用户明确要求且表很小）

## 执行方式（Windows / Agent）

请求体建议写入临时 `.json` 文件，避免 PowerShell 对 `-d` 字符串的错误解析。

```bash
curl.exe -sS -X POST "https://rdsapi.tcdba.17usoft.com/sql/manager/query" ^
  -H "Content-Type: application/json; charset=utf-8" ^
  -H "x-auth-token: <鉴权串>" ^
  --data-binary "@path\to\payload.json"
```

PowerShell：

```powershell
$headers = @{
  "Content-Type"   = "application/json; charset=utf-8"
  "x-auth-token"   = $env:RDS_X_AUTH_TOKEN  # 或 (Get-Content ".cursor\skills\rds-api-query\x-auth-token.txt" -Raw).Trim()（相对仓库根）
}
Invoke-RestMethod -Uri "https://rdsapi.tcdba.17usoft.com/sql/manager/query" `
  -Method Post -Headers $headers -Body (Get-Content "payload.json" -Raw -Encoding UTF8)
```

## 响应与展示

- 解析返回 JSON：`success`、`msg`；成功时再取 `result` 内 `list`、列 `fields` 等（以实际响应为准）
- 失败时向用户展示 `msg` 与 HTTP 状态码
- 向用户展示所用 **SQL**、**库/环境** 与结果摘要；可整理为 Markdown 表（列多时截断或只展示前 N 行并说明）

## 与违章统计技能

执行 `car_violation` 相关统计时，可与 [violation-data-statistics/SKILL.md](../violation-data-statistics/SKILL.md) 对齐口径；HTTP 路径用本技能 + [violation-connection-reference.md](violation-connection-reference.md) 作连接模板。

## 与订单押金统计技能

执行 `order_deposit_detail` 相关统计时，见 [order-deposit-data-statistics/SKILL.md](../order-deposit-data-statistics/SKILL.md)；连接模板使用 [order-connection-reference.md](order-connection-reference.md)（库 `TETravelMDSCROrder`）。

## 数据库名与环境映射

与 [rds-database-query/SKILL.md](../rds-database-query/SKILL.md) 中表一致：`mdscrVehicle` → `TETravelMDSCRVehicle`，`mdscrOrder`（若团队使用该简称）→ `TETravelMDSCROrder`；生产从库 `environment` 一般为 `product`；预发表名常用 `_pre` 后缀，以业务约定为准。

非快照库或未在本文档列出时：**不要编造** `databaseId` / `projectId` / 实例地址，应请用户提供控制台抓到的报文片段或连接快照 JSON。
