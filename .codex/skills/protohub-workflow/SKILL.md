---
name: protohub-workflow
description: >
  马达租车 ProtoHub-mada 原型工程化 Skill（v3.3 Hub+预览项目）。
  分层主干式架构（L0原则/L1流程/L2规范/L3资产）+ GATE/CHECKPOINT 机制 + 文件状态机 + SSOT 去重 + 推送前自审。
  v3.3 核心变化：原型设计作为研发版 PRD 确认后的后置流程；不依赖前端仓库 Git 权限，通过 gitnexus-hub 获取 Vue 源码 → 放入独立 Vue 预览项目修改 → npm run dev 预览；Hub 不可用时生成高保真 HTML 原型兜底。
  覆盖：① 新成员初始化 ② 日常原型迭代（10步线性流程）③ 推送质量保障（6组自审）
  ④ 多人协作冲突处理 ⑤ 新页面原型接入。
  触发词：ProtoHub / proto-hub / 原型推送 / 原型迭代 / 拉最新原型 / 可以推了 / 推送原型 / 接入ProtoHub / 前端代码修改
---

# ProtoHub-mada 原型工程化 Skill

> **版本**：v3.3（2026-07-08）| Hub 获取源码 + 独立 Vue 预览项目 + HTML 兜底 + PRD 方案确认后置入口
>
> **Changelog**：
> - v3.3（2026-07-08）：结合远程 `docs/team-guide.md`；明确原型设计流程必须放在需求大纲确认、产品方案与流程图制定、研发版 PRD 确认之后；补充 Web 使用 Element UI、小程序使用 Vant 的组件库约束
> - v3.2（2026-07-03）：移除 Git Subtree（研发主管不开放前端仓库权限）；改为通过 gitnexus-hub 获取 Vue 源码 → 放入 ProtoHub 内独立 Vue 预览项目（preview/）修改 → npm run dev 预览；Hub 不可用时生成高保真 HTML 原型兜底（方案 B）；废弃 frontend/ 和 upstream remote 相关内容
> - v3.1（2026-07-02）：Git Subtree 架构（已废弃，因前端仓库权限不可获取）
> - v3.0（2026-06-24）：原型方案重构——不再生成独立 HTML，改为拉取生产前端代码 → 修改 Vue 代码 → 构建预览
> - v2.1（2026-06-22）：新增 Step 0.5 遍历前端代码变更；修正所有 HTML 文件路径；工作流从 10 步扩展为 12 步
> - v2.0（2026-06-18）：分层架构重构（L0/L1/L2/L3）+ GATE/CHECKPOINT 机制 + 变更类型轴 + 推送前6组自审 + 文件状态机 + 知识回流 pending 池
> - v1.0（2026-06-18）：初始版本，9 节平铺式结构

> 马达租车运营管理平台原型仓库的完整协作工作流。

---

## Bundled references

本技能已随项目级技能继承 ProtoHub 参考资料：

- `references/style-guide.md`
- `references/data-flow-map.md`
- `references/team-guide.md`
- `references/quickstart.md`

当目标 ProtoHub 仓库内的 `docs/` 文件缺失时，读取这些 bundled references 作为兜底依据。

## L0. 核心原则

1. **Hub 获取源码 + 预览项目修改**：通过 gitnexus-hub 获取生产环境 Vue 源码，放入 ProtoHub 内独立 Vue 预览项目（`preview/`）中修改，用 `npm run dev` 构建预览。不依赖前端仓库 Git 权限
2. **HTML 兜底**：Hub 不可用或全新模块时，生成高保真 HTML 原型作为兜底方案；Web 页面使用 Element UI 组件形态，小程序页面使用 Vant 组件形态
3. **两阶段原则**：本地修改（拉取→获取源码→改→预览→检查）和确认推送（说"可以推了"才推）严格分离，不混在一起
4. **拉取优先**：每次开始工作前必须先拉最新 ProtoHub 代码，不拉不改
5. **关联检查必须执行**：推送前必须查 `data-flow-map.md` 确认关联影响，不可跳过
6. **Commit 规范**：`type(scope): 说明` 格式，scope 取模块名，说明用中文 20 字以内
7. **前端代码为准**：样式以生产环境源码为准，不自行定义设计体系。Web 复用 Element UI 组件和共享组件，小程序复用 Vant 组件和项目业务组件
8. **先读后改**：修改前端代码时先 Read 目标文件再改，不凭空写；未变更区域保持原样
9. **文件状态机**：每步产出必须写入磁盘（`tmp/` 目录），后续步骤通过 Read 读取，不依赖上下文记忆
10. **PRD 确认后再原型**：原型设计流程只在产品需求流程的研发版 PRD 确认后启动；如用户还在讨论大纲、产品方案、流程图或规则分支，先回到 PRD/方案流程，不进入 ProtoHub 修改

---

## L1. 工作流总览（Step -1 前置确认 + 10步线性 + GATE + CHECKPOINT）

共 10 步，三个阶段：准备（0-1）→ 修改（2-4）→ 推送（5-10）。该流程是产品需求流程 Step 8 的子流程，必须在 `.tmp/prd_confirmed.md` 或用户明确确认“PRD 已确认，开始做原型”后启动。

> **v3.2 变化**：通过 Hub 获取 Vue 源码 → 放入独立 Vue 预览项目修改 → npm run dev 预览。Hub 不可用时生成 HTML 原型兜底。

每步有 **GATE**（前置条件）和 **CHECKPOINT**（产出验证）。GATE 是物理依赖——必须满足条件才能开始本步。

| 步骤 | 做什么 | 产出 | GATE | CHECKPOINT |
|------|--------|------|------|------------|
| -1 | 前置确认 | `tmp/prototype_entry_check.md` | 需求大纲、产品方案、PRD 已确认 | 确认可进入原型设计 |
| 0 | 拉最新代码 + 创建功能分支 | `tmp/pull_status.md` | Step -1 完成；仓库已克隆、SSH/Token 有效 | pull 成功，无冲突 |
| 1 | 变更类型评估 + 获取 Vue 源码 | `tmp/change_plan.md` + `.vue` 文件 | Step 0 完成 | 类型已确定、源码已获取 |
| 2 | 读取目标 Vue 文件 | — | Step 1 完成 | 文件内容已在上下文 |
| 3 | 修改/编写前端代码（Vue） | 修改后的 `.vue` 文件 | Step 2 完成 | 文件已写入磁盘 |
| 4 | 构建预览（npm run dev） | `tmp/preview_result.md` | Step 3 完成 | 用户确认满意 |
| 5 | 关联影响检查 | `tmp/impact_check.md` | Step 4 完成 | 关联页面已列举、用户已确认 |
| 6 | 推送前自审（6组） | `tmp/self_audit.md` | Step 5 完成 | 所有检查项通过 |
| 7 | diff + commit message 预览 | `tmp/commit_preview.md` | Step 6 完成 | 用户确认 commit message |
| 8 | 执行推送 | — | Step 7 用户确认 | push 成功 |
| 9 | 更新映射表 + 知识回流 | `docs/data-flow-map.md` + `docs/change-log.md` | Step 8 完成 | 新文件/枚举已补录，变更记录已写入 |

```
Phase A（准备）：  Step -1 前置确认 → 0 拉取代码 → 1 评估+获取源码
Phase B（修改）：  Step 2-4（用户预览确认）
Phase C（推送）：  Step 5 关联检查 → 6 自审 → 7 commit预览 → 8 推送 → 9 映射+回流
```

**跨会话恢复**：新会话先 Read `tmp/code_changes.md`、`tmp/change_plan.md`、`tmp/impact_check.md` 恢复上下文，从对应步骤继续。

---

### Step -1：原型设计前置确认

🚧 **GATE**：产品需求流程已完成大纲确认、产品方案与流程图制定、研发版 PRD 确认
✅ **CHECKPOINT**：`tmp/prototype_entry_check.md` 已写入确认结果

启动 ProtoHub 原型设计前，先确认以下信息：

| 检查项 | 要求 |
|---|---|
| 需求大纲 | 已经用户确认；仍在讨论范围边界时不做原型 |
| 产品方案/流程图 | 已经完成并确认；仍在比较方案或调整流程分支时不做原型 |
| 研发版 PRD | 已经按 6 个模块生成并确认；原型只表达已确认的页面和交互 |
| 端类型 | 明确是 Web 管理后台、小程序，或两端都涉及 |
| 组件库 | Web 使用 Element UI；小程序使用 Vant；若目标源码依赖不同，以源码为准 |

写入 `tmp/prototype_entry_check.md`：

```markdown
## 原型设计前置确认
- 需求大纲：已确认 / 未确认
- 产品方案与流程图：已确认 / 未确认 / 简化流程图
- 研发版 PRD：已确认 / 未确认
- 端类型：Web / 小程序 / 多端
- 组件库：Element UI / Vant / 以源码为准
- 结论：可进入原型设计 / 返回 PRD 流程
```

若任一关键项未确认，停止 ProtoHub 修改，回到 PRD/方案流程补齐。

---

### Step 0：拉最新代码 + 创建功能分支

🚧 **GATE**：Step -1 完成；仓库已克隆到本地、SSH Key 或 Token 鉴权有效（⚠️ HTTP+密码已禁用）
✅ **CHECKPOINT**：`tmp/pull_status.md` 已写入，pull 成功无冲突，功能分支已创建

```bash
cd /Users/weigaopeng/WorkBuddy/2026-06-03-17-10-25
git checkout dev
git pull inner dev             # 拉取 ProtoHub-mada 最新代码
git log --oneline -5           # 查看最近提交

# 创建功能分支（分支名根据本次修改的模块和功能命名）
git checkout -b protohub/{模块}-{功能}
```

**AI 执行要点**：
- 本地有未提交修改 → 先提醒用户确认（stash 或 commit）
- pull 有冲突 → 进入第 5 节冲突处理流程
- **必须创建功能分支**，不在 dev 上直接修改
- 功能分支命名：`protohub/{模块}-{功能简称}`，如 `protohub/order-refund`
- 写入 `tmp/pull_status.md`：当前 HEAD hash、最近 5 条 log、功能分支名

**用户话术**：「拉最新代码」/「同步一下 Git」

---

### Step 1：变更类型评估 + 获取 Vue 源码

🚧 **GATE**：Step 0 完成
✅ **CHECKPOINT**：`tmp/change_plan.md` 已写入变更类型、目标文件、影响范围；Vue 源码已获取

> **业务术语定位**：收到产品描述（如「订单列表」「核验费用」）时，先查 `docs/data-flow-map.md` 中的「业务术语-仓库/页面映射表」，定位前端仓库和页面路径（`前端页面路径` 列），再从 Hub 获取对应 Vue 文件。

**1a. 变更类型轴**（决定流程深度）：

| 类型 | 判定 | 流程差异 |
|------|------|---------|
| 迭代修改 | 在已有 Vue 页面上改字段/按钮/样式 | 标准流程 Step 2-9，从 Hub 获取源码 |
| 新原型接入 | 编写新的 Vue 页面 | 走第 6 节专项流程（从 Hub 获取参考页面 → 编写 + 预览） |
| 全局样式变更 | 修改预览项目的全局样式/SCSS 变量 | ⚠️ 影响多页面，强制全局关联检查 |
| 模块结构变更 | 新增/删除模块目录 | 走第 6 节 + 更新文件结构说明 |

**1a-2. 端类型与组件库**：

| 端类型 | 组件库 | 执行要求 |
|---|---|---|
| Web 管理后台 | Element UI | 使用 `el-*` 组件和项目已有共享组件，不用 Ant Design、Bootstrap 或自定义组件替代 |
| 小程序 | Vant | 使用 `van-*` 组件和项目业务组件，不套用 Web 大表格、Web 弹框布局 |
| 多端 | 分别按端生成 | Web 和小程序分别生成原型，PRD 原型列分别标注 |

若目标仓库源码或依赖明确使用其他 Element 版本、Vant Weapp 或业务封装组件，以目标源码为准，但不得跨端套用组件形态。

**1b. 获取 Vue 源码（方案 A — 主路径）**：

通过 gitnexus-hub 获取生产环境 Vue 源码，放入 `preview/src/views/` 对应路径：

```bash
# 1. 查组件文件列表
python3 scripts/hub_client.py cypher --repo {仓库名} \
  --query 'MATCH (f:File) WHERE f.filePath CONTAINS "{页面路径}" RETURN f.filePath LIMIT 20'

# 2. 获取 Vue 源码（template + script + style 三部分）
python3 scripts/hub_client.py context --repo {仓库名} \
  --uid "File:{组件路径}" --content

# 3. 将源码写入 preview/src/views/{对应路径}/index.vue
# 4. 如涉及共享组件（SearchForm/Table 等），同时从 Hub 获取后放入 preview/src/components/
```

**1c. 获取源码失败时（方案 B — 兜底路径）**：

Hub 不可用或全新模块无对应页面时，生成高保真 HTML 原型：
- Web 页面使用 Element UI 组件形态；小程序页面使用 Vant 组件形态
- 基于业务描述生成 HTML 原型文件，放入 `prototypes/` 目录
- 在 PRD 原型列标注 `[HTML原型]`

**1d. 评估影响范围**：

根据变更类型，列出：
- 目标文件路径（哪些 Vue/SCSS/JS 文件会被修改）
- 影响范围（单页面 / 多页面 / 全局）
- 是否需要更新 `docs/data-flow-map.md`

将变更计划写入 `tmp/change_plan.md`。

---

### Step 2：读取目标 Vue 文件

🚧 **GATE**：Step 1 完成
✅ **CHECKPOINT**：目标 Vue 文件内容已在上下文中

**AI 执行要点**（铁律）：
- **先读后改**：用 Read 工具读取 `preview/src/views/` 下的目标 `.vue` 文件，不要凭空写
- **读相关组件**：如果涉及共享组件（SearchForm/Table 等），同时 Read `preview/src/components/` 下对应组件源码
- **读路由配置**：如果涉及新页面，参考已有页面的路由注册方式
- **读数据流**：如果涉及关联检查，同时 Read `docs/data-flow-map.md`

**用户话术模板**：

```
帮我修改前端仓库 mdscr-fe-admin 中的 src/views/sale/order/orderList.vue：
- [具体改动 1]
- [具体改动 2]
复用对应端现有组件库和样式（Web：Element UI；小程序：Vant）
```

---

### Step 3：修改/编写前端代码（Vue）

🚧 **GATE**：Step 2 完成，目标文件已读取
✅ **CHECKPOINT**：修改后的 .vue 文件已写入磁盘（前端仓库中）

**AI 修改规则**：

| 规则 | 要求 |
|------|------|
| 前端代码为准 | 直接修改 Vue 源码，不生成独立 HTML |
| 组件复用优先 | Web 使用 Element UI 组件和项目已有共享组件；小程序使用 Vant 组件和项目已有业务组件，不自定义替代 |
| 忠实修改 | 未变更区域保持原样，不做布局调整 |
| 样式一致 | 新增内容使用与原有内容一致的组件、props、CSS 类名 |
| 禁止发挥 | 不添加源文件中不存在的组件、装饰元素 |

📖 完整修改规范 → 见 L2 §1「样式规范速查」和 `docs/style-guide.md`

---

### Step 4：构建预览

🚧 **GATE**：Step 3 完成
✅ **CHECKPOINT**：`tmp/preview_result.md` 已写入，用户确认满意

**AI 执行**：
1. 在 frontend 目录启动 dev server：
   ```bash
   cd /Users/weigaopeng/WorkBuddy/2026-06-03-17-10-25/frontend
   npm run dev    # 或 pnpm dev / yarn dev
   ```
2. 用 `present_files` 工具打开 `http://localhost:5173` 供用户预览
3. 等待用户反馈
4. 不满意 → 回到 Step 3 继续修改
5. 满意 → 写入 `tmp/preview_result.md`（用户已确认），进入 Step 5

---

### Step 5：关联影响检查（⚠️ 必须执行，不可跳过）

🚧 **GATE**：Step 4 完成，用户已确认预览
✅ **CHECKPOINT**：`tmp/impact_check.md` 已写入关联页面列表、用户已确认

**AI 执行步骤**：

1. Read `docs/data-flow-map.md` 中的「改动影响速查表」
2. 根据本次修改的文件路径，列举所有可能受影响的关联页面
3. 输出格式：

```
本次修改了：preview/src/views/sale/order/orderList.vue

根据数据流向映射，以下页面可能受影响：
① src/views/sale/order/orderPickup.vue（订单取车）
② src/views/finance/billingVerify.vue（费用核验）
③ src/views/risk/process/index.vue（风控处理）

请确认这些页面是否需要同步调整后再说「可以推了」。
```

4. 写入 `tmp/impact_check.md`：修改文件、关联页面列表、用户确认状态
5. 等待用户确认

**特殊规则**：
- 变更类型=全局样式变更 → 列出**所有受影响页面**
- 变更类型=新原型接入 → 检查是否需要更新 `data-flow-map.md`

---

### Step 6：推送前自审（6组检查清单）

🚧 **GATE**：Step 5 完成，关联影响已确认
✅ **CHECKPOINT**：`tmp/self_audit.md` 已写入，所有检查项通过

📖 完整检查清单 → 见 L2 §2「推送前自审 6 组检查清单」

**自审执行顺序**：按 6 组**依次**进行，第 1 组（样式合规）强制最先执行。发现问题立即修正，不输出未通过自审的推送。

写入 `tmp/self_audit.md`：每组检查结果（通过/问题+修复）。

---

### Step 7：diff 摘要 + commit message 预览

🚧 **GATE**：Step 6 完成，自审全部通过
⛔ **BLOCKING**：展示 commit message 给用户确认
✅ **CHECKPOINT**：`tmp/commit_preview.md` 已写入，用户已确认 commit message

> **v3.2 变化**：修改后的 Vue 文件直接在 `preview/src/views/` 中，是 ProtoHub 仓库的一部分，无需 cp 同步。

**Step 7a — 展示 diff 和 commit message**：

```bash
cd /Users/weigaopeng/WorkBuddy/2026-06-03-17-10-25
git diff --stat HEAD               # 展示改动文件和行数
git add -A                          # 暂存所有改动
```

**AI 生成 commit message**（见 L2 §3 规范）：

格式：`type(scope): 说明`

展示给用户：
```
改动摘要：
  preview/src/views/sale/order/orderList.vue | +15 -3

建议 commit message：
  feat(order-list): 搜索栏增加统计卡片

确认后说「好」或提供修改意见。
```

用户确认后写入 `tmp/commit_preview.md`。

---

### Step 8：推送功能分支

🚧 **GATE**：Step 7 完成，用户已确认 commit message
✅ **CHECKPOINT**：功能分支 push 成功，展示 commit hash 和 push 结果

```bash
git commit -m "type(scope): 说明"
git push inner protohub/{模块}-{功能}    # 推送功能分支，不推 dev
```

**⚠️ 重要**：只推到 ProtoHub-mada 的功能分支，**不推到前端开发仓库**（mdscr-fe-admin 等）。

**推送失败处理**：
- 403 / 认证失败 → Token 过期，提醒用户更新（见 L2 §4 FAQ）
- 远程有新提交 → `git pull inner protohub/{分支} --rebase` 后重试，冲突走第 5 节

推送成功后展示 commit hash 和功能分支名。

---

### Step 9：评审通过后合并 dev + 更新映射表

🚧 **GATE**：Step 8 完成、**用户确认评审通过**
✅ **CHECKPOINT**：已合并到 dev，`docs/data-flow-map.md` 已更新（如需）

> 仅当用户确认评审通过后执行。合并功能分支到 dev，并更新映射表（如有结构变化）。

**AI 执行**：
1. 合并功能分支到 dev：
   ```bash
   git checkout dev
   git merge protohub/{模块}-{功能}
   git push inner dev
   ```
2. 检查 `tmp/change_plan.md` 中的变更类型
3. 如有新页面/枚举/字段 → 在 `docs/data-flow-map.md` 中补录
4. 如无结构变化 → 跳过映射表更新
5. 可选：删除已合并的功能分支

---

### Step 10：知识回流

🚧 **GATE**：Step 9 完成
✅ **CHECKPOINT**：`docs/change-log.md` 已追加本次变更记录

在 `docs/change-log.md` 追加：

```markdown
## YYYY-MM-DD | commit hash
- 变更类型：迭代修改 / 新原型接入 / 全局样式变更 / 模块结构变更
- 修改文件：{文件列表}
- 关联影响：{已确认的关联页面}
- commit message：{实际 commit message}
```

这为后续团队成员提供变更追溯，也为 AI 提供历史上下文。

---

## L2. 规范层（按使用时机分节，唯一权威）

### §1. 前端代码修改规范速查

> 加载时机：Step 3-4 修改 Vue 代码时

**核心原则**（最高优先级）：
- 直接修改前端仓库中的 Vue 源码，不生成独立 HTML 文件
- 新增内容与原有内容使用完全一致的组件和 props（Web：Element UI；小程序：Vant）
- 复用项目已有的共享组件或业务组件（Web 如 SearchForm、TablePanel；小程序如业务 Cell、Picker、Uploader 封装），不自定义替代
- 未变更区域保持原样，不做布局调整或样式重构

**组件库使用**：
- Web 页面默认使用 Element UI，组件 props 以前端项目中实际使用的为准，不自行定义
- 小程序页面默认使用 Vant，表单、选择器、上传、弹层等优先复用同模块已有写法
- 若目标仓库源码或依赖明确使用其他 Element 版本、Vant Weapp 等版本，以目标仓库实际依赖为准

**状态颜色规范**（与前端项目一致）：

| 状态类型 | 颜色 | 场景 |
|----------|------|------|
| 成功/已完成 | `#52C41A` 绿色 | 已完成、已支付、已审核 |
| 进行中/处理中 | `#1890FF` 蓝色 | 处理中、待审核、进行中 |
| 警告/待处理 | `#FAAD14` 橙色 | 待处理、待确认、即将过期 |
| 危险/异常/取消 | `#F5222D` 红色 | 已取消、异常、失败 |
| 中性/默认 | `#8C8C8C` 灰色 | 草稿、已关闭、默认状态 |

> 以上颜色为前端项目约定值。如果前端项目中使用了不同的颜色，以项目实际值为准。

**禁止行为**：
- ❌ 生成独立 HTML 文件代替修改 Vue 代码
- ❌ 引入与目标端不一致的 CDN 脚本或组件库（如 Web 后台改用 Ant Design，小程序改用 Web 表格）
- ❌ 自定义 CSS 设计体系（应复用项目已有的样式变量和 SCSS 变量）
- ❌ 在 Vue 文件中内联大段 `<style>` 覆盖项目全局样式

---

### §2. 推送前自审 6 组检查清单

> 加载时机：Step 6 推送前自审
>
> ⚠️ **执行顺序**：按 6 组**依次**进行，不可跳过或乱序。

#### 第 1 组：修改方式合规（最先执行）

- [ ] 直接修改了前端仓库中的 Vue 源码，未生成独立 HTML 文件
- [ ] 使用了目标端组件库和项目已有组件（Web：Element UI；小程序：Vant），未自定义替代
- [ ] 状态标签颜色符合前端项目约定（成功绿/进行中蓝/警告橙/危险红/中性灰）
- [ ] 未引入 CDN 脚本或自定义 CSS 设计体系

#### 第 2 组：文件完整性

- [ ] 修改的文件路径与 `tmp/change_plan.md` 一致
- [ ] 没有意外修改其他文件（`git diff --name-only` 检查）
- [ ] 修改的 `.vue` 文件在 `preview/src/views/` 下，路径正确

#### 第 3 组：关联影响已确认

- [ ] `tmp/impact_check.md` 已列举关联页面
- [ ] 用户已确认关联页面不需要同步调整（或已同步调整）
- [ ] 全局样式变更 → 所有关联页面已检查

#### 第 4 组：Vue 代码有效性

- [ ] Vue 模板语法正确（标签闭合、指令语法）
- [ ] import 路径正确（组件、API、工具函数）
- [ ] 无残留的调试代码（console.log、注释掉的测试代码）
- [ ] `npm run dev` 构建无报错

#### 第 5 组：数据流向一致性（仅变更类型=新原型接入/模块结构变更时触发）

- [ ] `docs/data-flow-map.md` 已更新新页面的数据来源和上下游关系
- [ ] 新页面放在 `preview/src/views/prototype/` 下（原型专属目录）
- [ ] 新页面文件命名符合规范（`{模块编号}-{页面名}.vue`）

#### 第 6 组：commit message 合规

- [ ] 格式为 `type(scope): 说明`
- [ ] type 正确（feat/refactor/fix/style/docs/chore）
- [ ] scope 为模块名（去路径前缀和扩展名）
- [ ] 说明用中文，20 字以内，具体描述做了什么
- [ ] 多文件时以影响最大的文件为主，附加 `(+N files)`

6 组全部通过后，方可进入 Step 7。

---

### §3. Commit Message 规范

> 加载时机：Step 7 生成 commit message 时

格式：`type(scope): 说明`

| type | 含义 | 示例 |
|------|------|------|
| `feat` | 新增功能/页面 | `feat(order-list): 搜索栏增加统计卡片` |
| `refactor` | 重构/重写 | `refactor(vehicle-detail): 重写车辆状态展示逻辑` |
| `fix` | 修复问题 | `fix(order-pickup): 修复时间选择器无法选今天的问题` |
| `style` | 样式调整 | `style(global): 统一表格行 hover 背景为浅红` |
| `docs` | 文档更新 | `docs(data-flow-map): 新增调度模块数据流向` |
| `chore` | 脚本/配置 | `chore(scripts): 新增 push-to-protohub.sh` |

**生成规则**：
1. `scope` 填写主要改动的模块/文件名（去掉路径前缀和扩展名）
2. 说明用中文，20 字以内，具体描述做了什么
3. 涉及多个文件时，以影响最大的文件为主，附加 `(+N files)` 说明

---

### §4. FAQ

> 加载时机：遇到问题时

**Q: Token 过期了怎么办？**

> ⚠️ 安全策略：HTTP+域账号密码方式已禁用，必须使用 **SSH 协议** 或 **域账号+Token** 方式。

**方式一（推荐）：SSH 协议**——无需 Token，配置一次 SSH Key 即可永久使用：
```bash
# 首次配置 SSH Key（如尚未配置）
ssh-keygen -t ed25519 -C "your-email@company.com"
# 将公钥 ~/.ssh/id_ed25519.pub 添加到 git.17usoft.com → Settings → SSH Keys

# 使用 SSH 地址克隆/更新 remote
git remote set-url inner git@git.17usoft.com:LY-MDSCR/ProtoHub-mada.git
```

**方式二：域账号 + Token**——Token 过期需重新生成：
```bash
# 去 git.17usoft.com → Settings → Access Tokens 重新生成
git remote set-url inner http://oauth2:<NEW_TOKEN>@git.17usoft.com/LY-MDSCR/ProtoHub-mada.git
```

**Q: 推送时报 403 / 认证失败怎么办？**

- **SSH 方式**：检查 `ssh -T git@git.17usoft.com` 是否连通，SSH Key 是否已添加到 GitLab
- **Token 方式**：Token 可能过期或权限不足，按上面步骤重新生成并更新 remote URL。Token 权限需要 `read_repository` + `write_repository`

**Q: 前端仓库 npm install 很慢怎么办？**

前端仓库依赖较多，建议使用淘宝镜像：
```bash
npm config set registry https://registry.npmmirror.com
npm install
```

**Q: npm run dev 启动失败怎么办？**

检查 Node.js 版本是否匹配（前端项目通常要求 Node 16+），清除缓存重试：
```bash
rm -rf node_modules package-lock.json
npm install
npm run dev
```

**Q: 如何查看当前仓库状态？**
```bash
cd /Users/weigaopeng/WorkBuddy/2026-06-03-17-10-25
git status
git log --oneline -10
```

**Q: Hub 不可用怎么办？**

Hub 不可用时走方案 B（HTML 兜底）：
1. 标注 `原型待补充（Hub 不可用）`
2. 如急需原型，基于业务描述生成高保真 HTML 原型（Web 使用 Element UI 组件形态，小程序使用 Vant 组件形态）
3. HTML 原型文件放入 `prototypes/` 目录
4. Hub 恢复后补获取 Vue 源码，转为方案 A 的 Vue 原型

**Q: preview/ 项目的依赖版本怎么和线上保持一致？**

从 Hub 获取目标仓库的 `package.json`，提取关键依赖版本（Vue、Element UI、Vant 等），同步到 `preview/package.json`：
```bash
python3 scripts/hub_client.py context --repo {仓库名} --uid "File:package.json" --content
```

---

## 5. 多人协作冲突处理

### 5.1 ProtoHub 内部冲突（Step 0 中 git pull 发生）

当 `git pull inner dev` 发生冲突时（同事改了同一个文件）：

**AI 应执行**：
1. 展示冲突文件列表（`git status`）
2. 展示冲突内容（`git diff` 或读取冲突文件）
3. 让用户决策：
   - 「保留我的版本」→ `git checkout --ours <file>` + `git add`
   - 「保留同事版本」→ `git checkout --theirs <file>` + `git add`
   - 「两个都要」→ AI 手动合并两段内容
4. 冲突解决后执行 `git add -A && git commit -m "merge: 解决与同事的合并冲突"`

### 5.2 避免冲突的最佳实践

- 每次开始工作前一定先拉取（Step 0 不可跳过）
- 一次会话只改一个页面/模块（L0 原则 8）
- 改完立即推，不要积压多次改动一起推
- 不同产品同学尽量不同时改同一个 Vue 文件
- 原型新增页面放 `preview/src/views/prototype/`，减少与迭代修改的冲突

### 5.3 推送时被拒（Step 8 中远程有新提交）

```bash
git pull inner protohub/{分支} --rebase
git push inner protohub/{分支}
```

若 rebase 产生冲突，按 5.1 处理。

### 5.4 原型隔离策略（从根源减少冲突）

| 策略 | 说明 |
|------|------|
| **专属目录隔离** | 原型新增页面统一放 `preview/src/views/prototype/`，与从 Hub 获取的已有页面分离 |
| **组件二次封装** | 不改从 Hub 获取的共享组件源码，新建 ProtoXxx.vue 继承封装 |
| **配置文件分离** | 原型配置放 `preview/.env.prototype`，不修改预览项目基础配置 |

---

## 6. 新原型接入流程

> 当变更类型=新原型接入时（Step 1 评估），走本节流程。

v3.2 中通过 Hub 获取参考页面源码，在 `preview/src/views/prototype/` 下创建新页面。

### Step A. 确认原型归属模块

根据 PRD 功能对应关系，确定页面放在哪个模块目录（在 `preview/src/views/prototype/` 下按模块组织）：

```
preview/src/views/prototype/         # 原型专属目录
├── order/                           # 订单相关原型
├── vehicle/                         # 车辆相关原型
├── billing/                         # 计费相关原型
└── ...                              # 按需创建
```

### Step B. 从 Hub 获取参考页面 + 创建新页面

1. 从 Hub 获取同模块已有页面作为参考：
```bash
python3 scripts/hub_client.py context --repo {仓库名} \
  --uid "File:src/views/sale/order/index.vue" --content
```
2. 在 `preview/src/views/prototype/{模块}/` 下创建新的 Vue 页面
3. 参照获取的参考页面的组件使用方式和代码结构

**AI 执行要点**：
- 先从 Hub 获取同模块的已有页面，学习组件使用方式和代码结构
- 新页面必须复用目标端组件库和项目已有组件（Web：Element UI；小程序：Vant）
- Hub 中没有参考页面时，走方案 B 生成 HTML 原型

### Step C. 构建预览

```bash
cd /Users/weigaopeng/WorkBuddy/2026-06-03-17-10-25/preview
npm run dev
```

用 `present_files` 打开预览地址供用户确认。

### Step D. 更新数据流向映射

在 `docs/data-flow-map.md` 中添加新页面的数据来源、核心字段和上下游影响关系。

### Step E. 进入标准推送流程

完成 Step A-D 后，回到标准流程 Step 5（关联检查）→ Step 6（自审）→ Step 7-9（推送+回流）。

---

## 7. 常用操作速查

| 你想做的事 | 对 AI 说 |
|-----------|---------|
| 开始工作前同步 | 「拉最新代码」 |
| 查看最近改动 | 「最近 5 次提交记录」 |
| 查看谁改了哪个模块 | 「最近谁改了订单模块」 |
| 确认推送 | 「可以推了」 |
| 回退某个文件 | 「帮我把 orderList.vue 恢复到上次提交版本」 |
| 回退到某个版本 | 「帮我把 xxx 页面恢复到昨天下午的版本」 |
| 更新 Token | 「帮我更新 ProtoHub Token 为 新Token」 |
| 新建模块 | 「帮我在 preview/src/views/prototype/ 下新建一个 xxx 模块」 |
| 查找页面路径 | 「帮我列出 订单模块 的所有页面」 |
| 构建预览 | 「启动前端 dev server 预览一下」 |
| 从 Hub 获取源码 | 「从 Hub 获取 orderList.vue 的源码」 |
| Hub 不可用 | 「Hub 不可用，生成 HTML 原型」 |

---

## 8. 文件结构说明

```
ProtoHub-mada/                        # 本地路径: /Users/weigaopeng/WorkBuddy/2026-06-03-17-10-25/
├── preview/                          # 独立 Vue 预览项目（产品团队自主维护）
│   ├── src/views/                    # Vue 页面源码（从 Hub 获取 + 修改）
│   │   ├── sale/order/               # 从 Hub 获取的已有页面
│   │   ├── prototype/                # 原型专属目录（新增页面放这里）
│   │   └── ...
│   ├── src/components/               # 共享组件（从 Hub 获取后放入）
│   ├── package.json                  # 预览依赖（按端与线上组件库版本对齐）
│   ├── vite.config.ts
│   └── .env.prototype                # 原型配置
├── prototypes/                       # HTML 原型归档（方案 B 兜底时使用）
├── shared/                           # 历史共享资源
├── scripts/
│   ├── hub_client.py                 # Hub API 客户端（获取 Vue 源码）
│   └── push-to-protohub.sh           # 推送质量保障脚本
├── docs/
│   ├── team-guide.md                 # 团队完整使用手册
│   ├── style-guide.md                # 前端代码修改规范
│   ├── data-flow-map.md              # ⭐ 改动关联检查的核心依据
│   ├── change-log.md                 # 变更追溯日志
│   └── ai-prompt-templates.md        # 提示词模板库
└── tmp/                              # 运行时临时文件（gitignore）
    ├── pull_status.md                # Step 0 产出
    ├── change_plan.md                # Step 1 产出
    ├── preview_result.md             # Step 4 产出
    ├── impact_check.md               # Step 5 产出
    ├── self_audit.md                 # Step 6 产出
    └── commit_preview.md             # Step 7 产出
```

---

## 9. 关键信息速查

| 项目 | 值 |
|------|-----|
| **内网 Git 仓库（SSH）** | `git@git.17usoft.com:LY-MDSCR/ProtoHub-mada.git` |
| **内网 Git 仓库（HTTP+Token）** | `http://oauth2:<TOKEN>@git.17usoft.com/LY-MDSCR/ProtoHub-mada.git` |
| **⚠️ 安全策略** | HTTP+域账号密码已禁用，必须用 SSH 或域账号+Token |
| **默认分支** | `dev` |
| **本地工作目录** | `/Users/weigaopeng/WorkBuddy/2026-06-03-17-10-25/` |
| **远程名称** | `inner`（内网 Git） |
| **Vue 预览项目** | `preview/`（独立预览项目，组件库按目标端与线上对齐） |
| **原型专属目录** | `preview/src/views/prototype/` |
| **HTML 原型归档** | `prototypes/`（方案 B 兜底时使用） |
| **前端预览命令** | `cd preview && npm run dev` |
| **Vue 源码获取** | `python3 scripts/hub_client.py context --repo {仓库} --uid "File:{路径}" --content` |
| **SSH Key 配置** | git.17usoft.com → 头像 → Settings → SSH Keys |
| **Token 获取路径** | git.17usoft.com → 头像 → Settings → Access Tokens |
| **Token 权限** | `read_repository` + `write_repository` |
| **数据流向文档** | `docs/data-flow-map.md` |
| **前端代码修改规范** | `docs/style-guide.md` |
| **gitnexus-hub** | multica skill 封装，MCP 地址 `http://ibd.travel.t.17usoft.com/gitnexus/mcp` |

---

## 10. 关键提醒

1. **方案 A 为主**：通过 Hub 获取 Vue 源码 → 放入 `preview/` 修改 → npm run dev 预览
2. **方案 B 兜底**：Hub 不可用或全新模块时，生成高保真 HTML 原型放入 `prototypes/`
3. **禁止跳过关联检查**：Step 5 是推送前的硬性门槛，不可跳过
4. **禁止积压推送**：一次会话只改一个页面/模块，改完立即推
5. **文件状态机**：每步产出写入 `tmp/` 目录，后续步骤通过 Read 读取，不依赖上下文记忆
6. **Token 安全**：Token 嵌入在 remote URL 中，不要在对话中暴露给非授权人员
7. **分支管理**：Step 0 必须创建功能分支 `protohub/{模块}-{功能}`，Step 8 推送功能分支，不直接推 dev。评审通过后 Step 9 合并 dev
8. **不推前端仓库**：修改只推到 ProtoHub-mada，**禁止推到前端开发仓库**（mdscr-fe-admin 等）
9. **快照版本标记**：从 Hub 获取源码时，在 `.vue` 文件头部添加来源标记注释（Source Repo / Source Path / Change 等）
10. **代码定位三步法**：① 术语映射表 → 仓库和页面路径；② Hub 查询 → Vue 文件；③ `<template>` 结构 → 修改区域。详见 team-guide.md §9
