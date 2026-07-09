# 步骤 3：系统感知

> 加载时机：模式识别完成后，需要从 GitNexus Hub 获取相关代码上下文时加载。

根据步骤 2 识别的模式，从 GitNexus Hub 获取相关代码上下文。

> **⚠️ Hub 访问方式**：Hub 已部署正式环境（`http://ibd.travel.t.17usoft.com/gitnexus/mcp`），multica 平台封装了 `gitnexus-hub` skill 约束调用层级深度。两种访问方式：
> - **MCP 工具**（推荐）：`mcp__gitnexus-hub__cypher` / `context` / `query`（使用前先用 ToolSearch 加载）
> - **hub_client.py 脚本**（备选）：MCP 不可用或需精确控制参数时使用
>
> **⚠️ 仓库覆盖（2026-06-16 补充）**：Hub 主要索引了**前端 Vue 仓库**和 BFF 层。后端 Java 仓库（mdscr-order, mdscr-vehicle 等）**不在 Hub 索引中**，无法通过 Hub 查后端枚举/计费逻辑。需要后端逻辑时：①用前端仓库查 UI 组件逻辑（推断后端接口行为）②查术语映射表获取枚举信息 ③用领域知识推断并标注 `[来自已有领域知识]`。
>
> ```bash
> # 列仓库
> python3 scripts/hub_client.py list-repos --search vehicle --indexed
> # Cypher 查询
> python3 scripts/hub_client.py cypher --repo LY-MDSCR__mdscr-fe-admin --query 'MATCH (f:File) WHERE f.filePath CONTAINS "xxx" RETURN f.filePath LIMIT 20'
> # 获取符号源码
> python3 scripts/hub_client.py context --repo LY-MDSCR__mdscr-fe-admin --uid "File:src/views/xxx/index.vue" --content
> # 关键词搜索
> python3 scripts/hub_client.py query --repo LY-MDSCR__mdscr-fe-admin --query "关键词" --goal "搜索目标"
> ```

## 3a. 模块定位

**瓦力需求优先从标题和描述中提取模块信息**：
- 标题中的 `【】` 标签通常标识模块（如 `【自营租车】` → 订单模块）
- 需求描述中的页面名称、功能名称映射到术语映射表
- 瓦力"产品线"字段直接标识所属系统

在「术语映射表」中查找业务术语对应的仓库和页面。映射表没有时用脚本 `query` 搜索。

## 3b. 按需求类型采集

| 类型 | 采集重点 |
|------|---------|
| 迭代 | 从 Hub 获取相关枚举值、现有页面结构、执行流。把枚举翻译成业务语言 |
| 新模块 | Hub 可能没有数据。只查映射表确认所属系统，查类似模块作为参考 |
| 外部对接 | 查数据推送/接收的代码路径，了解当前数据流向 |

Hub 采集清单（迭代类需求重点执行）：

| 查什么 | 脚本命令 | 查哪个仓库 | 用途 |
|--------|---------|-----------|------|
| 业务枚举 | `hub_client.py context --uid "Enum:{path}:{name}"` | 后端仓库 | PRD 的"枚举"字段值 |
| 数据字段 | `hub_client.py cypher --query 'MATCH (p:Property)...'` | 后端仓库 | PRD 的"字段"定义 |
| 页面结构 | `hub_client.py cypher --query 'MATCH (f:File) WHERE f.filePath CONTAINS "views"...'` | **前端**仓库 | 了解有哪些页面和组件 |
| 执行流 | `hub_client.py cypher --query 'MATCH (p:Process)...'` | 后端仓库 | 了解业务操作流程 |

**前后端仓库关系**：映射表记录的是后端仓库和对应的前端仓库。查页面结构时用前端仓库，查枚举和执行流时用后端仓库。

**前端仓库定位策略**（按优先级）：
1. **映射表有记录** → 直接用映射表中的前端仓库名
2. **映射表没有** → 先尝试 `mdscr-fe-admin`（通用后台前端），在其中搜索相关页面路径
3. **fe-admin 搜不到** → 用脚本 `hub_client.py list-repos --search {关键词} --indexed` 列出匹配仓库
4. **仍然找不到** → 用脚本 `hub_client.py query` 跨仓库搜索页面文件名，或在后端仓库中查找 Controller 层的 URL 映射推断页面路径

**已知前端仓库清单**（Hub 实测）：
- `mdscr-fe-admin` — 通用后台管理前端（采购、订单、审核等）
- `mdscr-fe-wap` / `mdscr-fe-wap-biz` / `mdscr-fe-wap-marketing` — H5 移动端
- `mdscr-fe-bff-maintenance` — 维修相关 BFF 层
- `mdscr-fe-store-wx` / `mdscr-fe-pms-wx` / `mdscr-fe-pms-alipay` — 小程序端

## 3b-2. 受影响页面骨架分析（迭代类需求必做）

对每个受影响的页面，从**前端仓库**获取当前页面骨架：
1. 用脚本 `hub_client.py cypher` 查页面目录下的文件列表，了解页面包含哪些组件
2. 用脚本 `hub_client.py context --content` 查关键组件，提取页面的当前结构
3. 翻译为 PM 视角的页面骨架：

```
采购单列表页当前骨架：
  筛选：采购单号、供应商名称、创建时间、采购进度
  列表：单号、供应商、金额、采购进度、结算状态、创建时间、操作
  操作：查看详情、编辑、提交、删除
```

这个骨架在步骤 4 展示给产品确认（"我理解的当前页面对吗？"），在步骤 5 作为变更基线（"在现有基础上改什么"）。

Hub 查询注意事项（均通过 `hub_client.py` 脚本执行）：
- 中文搜索效果差（实测"采购单创建"返回空结果），优先用英文关键词或代码中的类名/函数名
- 查 Enum 分两步：
  1. 先用 `hub_client.py cypher --query 'MATCH (e:Enum) WHERE e.filePath CONTAINS "enums" RETURN e.name, e.filePath'`
  2. 从返回结果中取完整 filePath，构造 UID：`Enum:{filePath}:{枚举名}`
  3. 用 `hub_client.py context --uid "{UID}" --content` 获取枚举源码
- 脚本返回错误信息时：根据错误提示调整参数重试
- 脚本返回空结果时：尝试换一个关键词搜索，或使用映射表中的其他枚举名
- Hub 完全不可用时（脚本报连接错误）：**硬阻断，不降级继续**。向用户输出阻断消息，说明 Hub 不可用导致无法获取系统现状数据（枚举值、页面结构、字段定义），生成的 PRD 会严重缺失关键信息。给出排查指引（检查网络、检查 hub_client.py 配置、是否需要建索引），等用户说「继续」后重新检测。如果是新模块类需求且确认 Hub 中确实没有该模块数据（不是连接问题），可以跳过系统感知继续。

## 3c. 翻译为业务摘要

将 Hub 返回的代码信息翻译为 PM 能理解的业务语言：

```
Hub 返回：PurchaseSettlementStatusEnum → PENDING_SETTLEMENT(1,"待结算"), SETTLEMENT_PROGRESS(2,"结算中")...
翻译为：采购单结算状态有 4 种：待结算、结算中、已完成、终止
```

翻译规则：
- 不提代码、函数名、文件路径
- 只描述：页面、操作、字段、状态
- 用中文业务术语

## 3d. LightRAG 业务上下文（如果已部署）

从 LightRAG 查询涉及模块的历史需求变更、相关业务规则、类似功能在其他模块的实现。未部署则跳过。

---

# Hub 查询模板

系统感知时按以下模板构造 Hub 查询：

## 查枚举值（两步）

**第一步：获取枚举列表和完整路径**
```json
{
  "name": "cypher",
  "arguments": {
    "repo": "{后端仓库，如 LY-MDSCR/mdscr-purchase}",
    "query": "MATCH (e:Enum) WHERE e.filePath CONTAINS \"enums\" RETURN e.name, e.filePath ORDER BY e.name"
  }
}
```
返回：所有枚举的名称和完整文件路径。从中筛选与当前需求相关的枚举。

**第二步：获取具体枚举值**
```json
{
  "name": "context",
  "arguments": {
    "repo": "{后端仓库}",
    "uid": "Enum:{第一步返回的filePath}:{枚举名}",
    "content": true
  }
}
```
返回：Java 枚举源码，提取 `(code, "中文描述")` 对，翻译为 PRD 的枚举值列表。

**注意**：如果 context 返回 `"status": "ambiguous"`，从 candidates 中选择 kind 为空字符串的条目（Enum 本体），不要选 kind 为 "Constructor" 的条目。

## 查前端页面结构
```json
{
  "name": "cypher",
  "arguments": {
    "repo": "{前端仓库，如 LY-MDSCR/mdscr-fe-admin}",
    "query": "MATCH (f:File) WHERE f.filePath CONTAINS \"{页面路径}\" RETURN f.filePath LIMIT 30"
  }
}
```
返回：该页面下的所有文件，推断页面包含的组件和功能。

## 查前端 Vue 组件源码（原型生成用）

**第一步：获取组件文件列表**
```json
{
  "name": "cypher",
  "arguments": {
    "repo": "{前端仓库}",
    "query": "MATCH (f:File) WHERE f.filePath CONTAINS \"{页面路径}\" RETURN f.filePath LIMIT 20"
  }
}
```

**第二步：获取具体组件源码**
```json
{
  "name": "context",
  "arguments": {
    "repo": "{前端仓库}",
    "uid": "File:{第一步返回的filePath}",
    "content": true
  }
}
```
返回：Vue SFC 完整源码（template + script + style），从中提取页面结构用于原型生成。

**注意**：Vue 文件在 Hub 中是 File 类型节点，不是 Class/Component。UID 格式为 `File:{filePath}`，不带冒号后缀。

## 查后端执行流
```json
{
  "name": "query",
  "arguments": {
    "repo": "{后端仓库}",
    "search_query": "{英文关键词}",
    "limit": 10,
    "content": false
  }
}
```
返回：匹配的代码符号和执行流，了解业务操作的代码映射。

## 查影响面
```json
{
  "name": "impact",
  "arguments": {
    "repo": "{后端仓库}",
    "target": "{目标符号名}",
    "direction": "upstream",
    "depth": 2
  }
}
```
返回：修改该符号的影响范围，用于 PRD 的"关联影响"章节。

## 查数据字段（Property 节点）
```json
{
  "name": "cypher",
  "arguments": {
    "repo": "{后端仓库}",
    "query": "MATCH (p:Property) WHERE p.filePath CONTAINS \"{文件路径}\" RETURN p.name, p.type ORDER BY p.name"
  }
}
```
返回：指定文件内的属性名和类型，了解数据结构。注意：Property 节点的字段名可能因索引版本不同有差异，如果查询报错，去掉 `p.type` 只返回 `p.name`。
