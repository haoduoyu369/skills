# Step 8：产品原型设计详细规则

> 加载时机：在“需求大纲已确认 → 产品方案/流程图已制定并确认 → 研发版 PRD 已完成并确认”之后，需要为有 UI 变更的页面修改前端 Vue 代码时加载。未完成 PRD 确认时，不进入原型设计。
>
> **v3.5 变化**：原型设计流程纳入产品需求步骤，位于固定 6 模块研发版 PRD 完成并确认之后；执行时以 ProtoHub-mada 远程 `docs/team-guide.md` 为主基线，并结合当前 Hub+preview 路径。Web 页面默认使用 Element UI，小程序页面默认使用 Vant；具体组件版本以目标前端仓库源码和依赖为准。通过 gitnexus-hub 获取源码，放入 ProtoHub-mada 的独立预览项目（`preview/`）中修改；Hub 不可用时生成高保真 HTML 原型兜底（方案 B）。

## 8-0. 前置门禁

| 门禁 | 要求 |
|---|---|
| 大纲确认 | `.tmp/requirements_outline.md` 已根据用户确认更新 |
| 方案确认 | `.tmp/solution_brief.md` 已记录推荐方案、业务模型、流程图/建模决策和用户确认 |
| PRD 确认 | `.tmp/prd_confirmed.md` 已记录 PRD 确认结果 |
| ProtoHub 基线 | 优先读取远程 `docs/team-guide.md`，以团队原型流程主基线为准 |

说明：原型用于验证已确认的页面布局和交互，不用于替代需求大纲确认、产品方案讨论、流程图制定或 PRD 确认。

## 8-1. 端类型与组件库选择

生成原型前先判断目标页面所属端，再决定组件库和组件形态。

| 端类型 | 默认组件库 | 原型组件要求 | 常用组件 |
|---|---|---|---|
| Web 管理后台 | Element UI | 使用 `el-*` 组件和项目已有共享组件，不使用 Ant Design、Bootstrap 或自定义组件替代 | `el-form`、`el-select`、`el-table`、`el-dialog`、`el-upload`、`el-pagination`、`el-tag` |
| 小程序 | Vant | 使用 `van-*` 组件形态，不套用 Web 端表格/弹框布局 | `van-cell`、`van-field`、`van-picker`、`van-popup`、`van-button`、`van-uploader`、`van-radio`、`van-tabs` |

说明：

a. 若目标源码或 `package.json` 明确使用其他 Element 版本、Vant Weapp 或其他组件库版本，以目标仓库实际依赖为准，但页面形态仍必须跟同端已有页面保持一致。  
b. Web 原型不得把 Element UI 表单、表格替换成自定义 HTML 表格；小程序原型不得直接复用 Web 后台的大表格布局。  
c. 同一需求同时涉及 Web 和小程序时，分别生成对应端原型，并在 PRD 原型列区分链接。

## 8-2. 前端代码修改原则（最高优先级）

直接修改前端仓库中的 Vue 源码，复用已有组件和样式。

| 原则 | 说明 |
|------|------|
| **前端代码为准** | 原型样式以实际前端 Vue 源码中的 `<template>` + `<style scoped>` 为唯一标准，不自行定义设计体系 |
| **组件复用优先** | Web 优先使用 Element UI 组件和共享组件（SearchForm、SearchItem、Table 等）；小程序优先使用 Vant 组件和项目已有业务组件，不自行编写替代组件 |
| **样式忠实复制** | 从 Hub 获取 Vue 源码后，原样复制组件结构、CSS 类名、scoped styles，不做样式发挥 |
| **设计令牌对齐** | 颜色使用前端代码中的 CSS 变量、Element UI 主题变量或 Vant 主题变量，不硬编码自定义色值 |

**禁止的替代方案**：

| 前端实际组件 | 禁止的替代 |
|-------------|----------|
| `SearchForm` → `el-form > el-row(:gutter=12) > el-col(:sm=24,:md=12,:lg=8,:xl=6)` | `el-form :inline="true"` |
| `Table` → `[actionBar] + el-table(border) + el-pagination` | 自定义 `<table>` 标签 |
| `el-descriptions` → `el-descriptions(:column=N) > el-descriptions-item` | 自定义 label-value 布局 |
| `el-select` | 替换成 `el-table` 或自定义下拉 |
| `van-cell` / `van-field` / `van-popup` | 替换成 Web 端 `el-table` / `el-dialog` |

## 8-3. 获取 Vue 组件源码

对每个需要原型的页面，通过 `hub_client.py` 脚本获取前端 Vue 源码：

```bash
# 1. 查组件文件列表
python3 scripts/hub_client.py cypher --repo {仓库名} \
  --query 'MATCH (f:File) WHERE f.filePath CONTAINS "{页面路径}" RETURN f.filePath LIMIT 20'

# 2. 获取关键组件源码（根据变更类型选择）
python3 scripts/hub_client.py context --repo {仓库名} \
  --uid "File:{filePath}" --content

# 3. 获取共享组件源码（重要！这些决定页面布局）
#    - src/components/SearchForm/index.vue → el-form > el-row(gutter=12) > SearchItem
#    - src/components/SearchItem/index.vue → el-col(sm=24, md=12, lg=8, xl=6) > el-form-item
#    - src/components/Table/index.vue → [actionBar] + el-table(border) + el-pagination

# 4. 获取页面 scoped styles（<style> 部分）：
#    context 返回的 content 包含 template + script + style，三部分都要读取
```

组件选择规则：
  - 列表筛选/表格列变更 → 获取 index.vue（含 SearchForm + Table）
  - 详情页字段变更 → 获取 DetailInfo/index.vue 或 Detail/index.vue
  - 审批弹框变更 → 获取 Pass/index.vue 或 Reject/index.vue
  - 新建/编辑弹框变更 → 获取 components/Create/index.vue 或 Edit/index.vue

## 8-4. 解析页面结构

从 Vue 源码的 `<template>` + `<style>` 部分提取页面骨架：

| Vue 组件 | 提取信息 |
|---------|---------|
| `SearchForm` + `SearchItem` | 筛选项标签、控件类型、**响应式网格（el-row + el-col）** |
| `Table` + `el-table-column` | 表格列标签、**actionBar 插槽、分页** |
| `el-descriptions` + `el-descriptions-item` | 详情字段标签、列宽比例 |
| `el-form` + `el-form-item` | 表单字段标签、必填、校验规则 |
| `el-button` | 按钮文本、展示条件 |
| `<style scoped>` | **自定义 CSS 类名和样式** |

**原型范围原则（重要）**：

原型必须展示**完整页面**（让人一眼看出是哪个页面或弹框），但只**修改** PRD 涉及的组件。

| 原则 | 要求 |
|------|------|
| 展示完整页面 | 原型要包含页面的主要区域（搜索区、表格区、详情区、操作区），让人能辨认出是哪个页面 |
| 只改该改的组件 | PRD 改了哪个组件就修改哪个。其他组件忠实复制 Vue 源码，不做任何调整 |
| 源码忠实度优先 | 未变更字段必须原样复制 Vue 模板结构（标签、顺序、属性），不做布局调整 |
| 禁止设计发挥 | 不添加源码中不存在的组件、布局、装饰元素 |

**页面各区域的处理方式**：

| 区域 | 处理方式 |
|------|------|
| PRD 变更的组件 | 忠实复制 + 叠加变更，**展示部署后的真实状态**（无标注装饰） |
| 同页面的其他组件 | 忠实复制 Vue 源码，填入模拟数据，不做修改 |
| 页面标题/面包屑 | 从源码中提取，如实展示（源码没有则不加） |
| PRD 未提及的弹框/子组件 | 如果源码中作为页面的一部分存在，保留其触发按钮/入口；不展开弹框内容 |
| 表格数据行 | 填入 2-3 行模拟数据，展示表格完整结构 |

**"忠实复制"的含义（100% 还原目标）**：
- 从 Hub 获取 Vue 源码的 `<template>` + `<style scoped>` 部分（两部分都要读）
- 原样复制组件结构（el-table-column 的 label、el-descriptions-item 的 label/width 等）
- 将模板变量（`{{ xxx }}`）替换为合理的模拟数据
- **复现 scoped styles**：将 `<style scoped>` 中的 CSS 粘贴到原型 `<style>` 中
- **使用共享组件的真实渲染结构**（见下方 HTML 技术规格）
- 不改变字段顺序、不删减字段、不添加字段

## 8-5. 叠加 PRD 变更 + 修改 Vue 代码

基于 Vue 源码修改前端代码——100% 保留页面结构，只叠加 PRD 变更。

**生成前：变更融入分析（强制输出，不填完不许写代码）**：

原型展示的是**部署后的真实页面状态**。变更说明放在底部文档区，页面上**不加任何标注装饰**（无橙色边框、无"PRD新增"标签、无灰色删除线）。

对每个 PRD 变更点，**必须在对话中输出以下分析**（不输出则视为未执行）：

```
【变更融入分析】
变更点 N：{PRD 要求的变更，一句话}
  a. 影响哪个组件？ → {组件路径，Hub 获取的}
  b. 该组件的渲染本质？ → {一句话概括：el-select 多选下拉 / el-table 行列表 / el-descriptions 键值对 / el-form 表单...}
  c. 原有元素中最相似的一个？ → {标签名 + props 列表，直接从源码复制}
  d. 新元素与 c 的差异清单：{逐一列出，每项必须有理由}
     - 差异 1：{差异} — 理由：{为什么需要不同}
     - 差异 2：...
     - 无差异：{确认完全一致}
  e. 是否有字段应该移除？ → {是/否，列出}
  f. 新旧字段会同时出现在页面上吗？ → {是 → 停下重新设计 / 否 → 继续}
  g. 网格/布局对齐检查：{新增后总字段数能否被 column 整除？是否需要 span 属性？}
```

分析完后，对照以下**已知失败模式**自查（这些是真实犯过的错）：

| 失败模式 | 具体案例 | 根因 | 自查问题 |
|---------|---------|------|---------|
| 组件替换 | PRD 说"列表增加列"，把 el-select 下拉选项替换成 el-table | "列表"被理解为表格，实际是 el-select 的 option 列表 | 我是否在替换组件类型？能否在原有组件上扩展？ |
| 新旧共存 | 搜索表单同时展示被删除的"车型商品ID"和新增的"车型商品" | 想展示变更对比，但原型应展示部署后状态 | 删除的字段是否还在页面上？新旧是否同时出现？ |
| props 缺失 | 新增的多选 el-select 没加 collapse-tags，导致纵向撑开 | 只关注功能，没检查同级组件的通用 props | 新元素的 props 是否与最相似的原有元素完全一致？ |
| 网格断裂 | el-descriptions(column=2) 追加 5 个字段，末尾原有字段和新字段混在同一行 | 只考虑"追加"，没算网格对齐 | 新增后总字段数的行布局是否合理？是否需要 span 分隔？ |
| 自定义样式 | 给 el-option 加 flex 多列布局的自定义 CSS，原源码只有纯文本 | 想展示更多信息就加 CSS，没考虑原有组件的渲染方式 | 自定义 CSS 在源码中有没有对应？能否用组件自带能力实现？ |

变更融入的核心原则：

| 变更类型 | 正确做法 | 错误做法 |
|---------|---------|---------|
| 新增字段（el-descriptions） | 用与其他字段完全一致的 el-descriptions-item，注意 span 属性保持网格对齐 | 加橙色边框、加"PRD新增"标签 |
| 新增列（el-table-column） | 与其他列一样的 header 和 cell 样式 | 加特殊背景色、加标注 |
| 新增表单项（el-form-item） | 与同级 form-item 一样的结构和 props | 加特殊边框 |
| 新增下拉选项信息 | 在 el-option slot 内横向扩展信息列 | 把 el-select 替换成 el-table |
| 替换字段（删旧加新） | 移除旧字段，新字段放在原位置 | 同时展示旧字段（灰化）和新字段 |
| 删除字段 | 从页面上完全移除 | 保留灰化/删除线版本 |
| 修改字段 | 展示修改后的最终状态 | 同时展示修改前和修改后 |

### Vue 代码修改规范

- 在前端仓库中直接修改/新增 `.vue` 文件（不生成独立 HTML）
- 按端使用前端项目已有组件：Web 使用 Element UI 和共享组件；小程序使用 Vant 和项目已有业务组件（直接 import，不需要 CDN）
- **Web 页面必须使用共享组件的真实结构**：
  - SearchForm → `el-form > el-row(:gutter=12) > el-col(:sm=24, :md=12, :lg=8, :xl=6)` 响应式网格
  - Table → `[actionBar] + el-table(border) + el-pagination`
  - 不要用 `el-form :inline="true"` 代替 SearchForm 的网格布局
- **小程序页面必须使用 Vant 的移动端结构**：
  - 表单输入 → `van-field`
  - 选项选择 → `van-popup + van-picker` 或项目已有选择器
  - 附件上传 → `van-uploader`
  - 操作按钮 → `van-button`
  - 列表信息 → `van-cell` / 业务列表组件，不使用 Web 大表格
- 模拟数据使用真实枚举值（来自 Hub）+ 合理业务数据
- **新增内容必须与原有内容使用完全一致的组件和 props**（如 collapse-tags、max-collapse-tags、clearable 等）
- 复用 Vue 源码中的 scoped style 类名
- 变更说明放在 PRD 文档中，**页面上不做任何标注**
- **禁止**：自定义 `.section` 卡片包装、源码中不存在的装饰组件、PRD 未要求的交互元素、标注 CSS 类（`.prd-new`、`.prd-del` 等）、生成独立 HTML 文件代替修改 Vue 代码

文件修改位置：`preview/src/views/{页面路径}/index.vue`（ProtoHub 预览项目内，源码从 Hub 获取）

**修改后：逐元素比对（必须执行，输出比对表）**：

Vue 代码修改完后，在对话中输出以下比对表：

| 元素 | 原有元素（从源码） | 新增/修改后 | 组件类型一致？ | props 一致？ | 布局方向一致？ |
|------|-----------------|-----------|--------------|-------------|--------------|
| {每个变更涉及的元素} | {标签 + 组件 + props} | {标签 + 组件 + props} | ✓/✗ | ✓/✗ | ✓/✗ |

任何 ✗ 项必须修正或给出理由。

**额外核对**：
- [ ] 原组件的每个字段都在 Vue 代码中，且顺序、标签、宽度属性与源码一致
- [ ] 新增字段都有 PRD 依据，位置合理（在相关字段附近）
- [ ] 没有 PRD 未提及的额外组件、弹框、区域
- [ ] 没有自定义的页面装饰（标题栏、图例、分区线等，除非源码本身就有）
- [ ] 没有自定义 CSS 类（除非源码的 `<style scoped>` 中有对应）
- [ ] 删除的字段已从 Vue 代码完全移除
- [ ] `npm run dev` 构建通过，无编译错误

## 8-6. 回填 PRD 原型列

生成后，将 PRD 三列表格的原型列更新为：

```markdown
| 功能点 | 原型 | 说明 |
|--------|------|------|
| 审批详情-新增展示 | [📐 查看原型](preview/src/views/{页面路径}/index.vue) | a. 还车时间：只读展示... |
```

同一页面有多处变更时，共用一个 Vue 文件，多行链接到同一文件。

## 8-7. 独立验证（子 agent 执行，修改后必须执行）

Vue 代码修改完后，用 Agent 工具派生一个**验证 agent**，独立检查修改后的 Vue 代码与源码的一致性。

验证 agent **只检查、不修改**，返回差异报告。主 agent 根据报告修复问题。

调用方式：
```
Agent({
  description: "原型验证",
  prompt: "<下方验证 agent 提示词>"
})
```

**验证 agent 提示词模板**（主 agent 填写 {变量} 后传入）：

```
你是一个前端代码验证员。你的任务是逐字段比对修改后的 Vue 代码和原始 Vue 源码的一致性。
你不修改任何文件，只输出差异报告。

## 输入
- 修改后的 Vue 文件：{Vue文件绝对路径，如 preview/src/views/xxx/index.vue}
- Vue 源码仓库：{仓库名，如 LY-MDSCR__mdscr-fe-admin}
- Vue 源码组件路径：{组件路径列表，用逗号分隔}
- PRD 变更清单：{变更描述列表}

## 获取源码方法
用以下命令从 Hub 获取 Vue 源码：
```bash
python3 scripts/hub_client.py context --repo "{仓库名}" --uid "File:{组件路径}" --content
```
输出中 `=====` 分隔线之间的内容即为 Vue 源码（包含 template + script + style）。

同时读取修改后的 Vue 文件：
```bash
cat {修改后的Vue文件路径}
```

## 检查项（逐项输出结果）

### 1. 字段完整性
比对源码 <template> 中的每个字段（Web：el-form-item / el-descriptions-item / el-table-column；小程序：van-field / van-cell / van-uploader）：
- 源码中的字段是否都在修改后的 Vue 代码中？（排除 PRD 要求删除的）
- 修改后的 Vue 代码中是否有源码不存在的字段？（排除 PRD 要求新增的）
- 字段顺序是否与源码一致？

### 2. 组件形态一致性
对每个 PRD 新增/修改的元素：
- 它使用的组件类型（Web：el-select / el-input / el-table 等；小程序：van-field / van-popup / van-picker 等）是否与源码中最相似的元素一致？
- 如果不一致，标记为【组件替换】问题

### 3. Props 一致性
对每个 PRD 新增的元素：
- 列出源码中最相似元素的所有 props（collapse-tags / clearable / filterable / max-collapse-tags 等）
- 列出修改后 Vue 代码中新增元素的所有 props
- 逐项比对，缺失的标记为【props 缺失】问题

### 4. 自定义 CSS 检查
扫描修改后 Vue 文件的 <style scoped> 标签：
- 列出所有 CSS 类名
- 与源码 <style scoped> 中的类名比对
- 源码中不存在的类名标记为【自定义样式】问题

### 5. 已删除字段残留
如果 PRD 要求删除某个字段：
- 检查修改后的 Vue 代码中是否仍有该字段
- 如果有，标记为【残留字段】问题

### 6. 新旧共存检查
如果 PRD 要求替换某个字段（删旧加新）：
- 检查修改后的 Vue 代码中是否同时出现旧字段和新字段
- 如果是，标记为【新旧共存】问题

### 7. 构建验证
检查 `npm run dev` 是否能正常编译：
- 如果有编译错误，标记为【构建失败】问题

## 输出格式
对每个检查项，输出：
- ✅ 通过：{简要说明}
- ❌ 问题：{具体描述} → 建议修复：{怎么改}

最后给出总结：
- 问题数：X 个
- 严重程度：高/中/低
- 是否需要修复后重新验证：是/否
```

**主 agent 处理验证报告**：
- 如果报告有 ❌ 项：逐项修复 Vue 代码，然后重新构建预览
- 如果报告全部 ✅：继续下一步
- 修复后不需要再次调用验证 agent（避免无限循环），主 agent 自行确认修复正确

## 降级处理

- Hub 不可用（脚本连接失败） → 走方案 B 生成高保真 HTML 原型，Web 使用 Element UI 组件形态，小程序使用 Vant 组件形态，放入 `prototypes/` 目录
- Vue 源码获取失败 → 标注 `原型待补充（Hub 不可用）`
- Vue 源码过于复杂无法准确修改 → 标注 `[简化原型]`
- 非 UI 变更 → 原型列写 `无 UI 变更`
