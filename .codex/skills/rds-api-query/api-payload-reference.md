# RDS `sql/manager/query` 请求体说明

接口：`POST https://rdsapi.tcdba.17usoft.com/sql/manager/query`

## 请求头（除 `Content-Type` 外）

| Header | 说明 |
|--------|------|
| `x-auth-token` | RDS 平台鉴权；过期后从控制台同源请求复制新值（见 `SKILL.md` / `x-auth-token.txt` / `RDS_X_AUTH_TOKEN`） |

**无需** `Cookie`。

## 顶层字段（车辆库示例见同目录 `violation-connection-reference.md`）

以下字段用于标识连接与上下文；**具体值随库/环境/账号权限变化**，其它库以浏览器 Network 中实际请求为准。

| 字段 | 示例与作用 |
|------|------------|
| `maxLevel` | 树/会话上下文，如 `20` |
| `readInstanceIp` / `readInstancePort` | 只读实例 |
| `instanceIp` / `instancePort` | 当前实例（常与只读一致） |
| `databaseName` | 逻辑库全名，如 `TETravelMDSCRVehicle` |
| `logicName` | 常与 `databaseName` 相同 |
| `databaseTypeName` / `databaseTypeId` | 如 `MySql` / `4` |
| `environment` | 如 `product`、`uat`、`test` |
| `environmentLevel` | 环境级别数值 |
| `directType` | 如 `instance` |
| `databaseId` / `projectId` | 平台侧库、项目 ID |
| `type` | 如 `table` |
| `name` / `table` | 当前上下文表名，如 `car_violation` |
| `tableRemark` | 表备注 |
| `writeInstanceIp` / `writeInstancePort` | 写实例（查询场景常为空/0） |
| `middleware` | 布尔 |
| `fields` | 可为 `[]` |
| `tables` | **可为空对象 `{}`**；不要求携带控制台导出的大型表 → 列名映射 |
| **`sql`** | **必填**：执行的 SQL 字符串 |

## 推荐报文形态（`tables` 为空）

与 [violation-connection-reference.md](violation-connection-reference.md) 一致：连接元数据 + `"tables": {}` + `sql`。请求头仅带 `x-auth-token`。

## SQL 字段格式示例

```json
"sql": "SELECT * FROM `car_violation` WHERE id = 1 LIMIT 100;"
```

预发表常用 `_pre` 后缀（如 `car_violation_pre`）。
