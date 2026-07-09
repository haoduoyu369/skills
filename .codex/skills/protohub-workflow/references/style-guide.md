# 前端代码修改规范 v3.1

> **核心原则**：不再生成独立演示 HTML。通过拉取生产环境前端代码，直接修改或编写新的 Vue 代码，再用修改后的代码构建预览页面。
>
> 更新：v3.1（2026-07-07）— 补充端类型与组件库规则：Web 默认 Element UI，小程序默认 Vant
> - v3.0（2026-06-24）— 从"原型生成规范"改为"前端代码修改规范"
> - v2.0（2026-06-22）— 从自定义设计体系改为前端代码样式对齐

---

## 0. 样式对齐原则（最高优先级）

### 0.1 基本原则

| 原则 | 说明 |
|------|------|
| **前端代码为准** | 原型样式以实际前端 Vue 源码中的 `<template>` + `<style scoped>` 为唯一标准，不自行定义设计体系 |
| **组件复用优先** | Web 优先使用 Element UI 组件和共享组件（SearchForm、SearchItem、Table 等）；小程序优先使用 Vant 组件和项目已有业务组件，不自行编写替代组件 |
| **样式忠实复制** | 从 Hub 获取 Vue 源码后，原样复制组件结构、CSS 类名、scoped styles，不做样式发挥 |
| **设计令牌对齐** | 颜色使用前端代码中的 CSS 变量、Element UI 主题变量或 Vant 主题变量，不硬编码自定义色值 |

### 0.2 端类型与组件库选择

| 端类型 | 默认组件库 | 修改/原型要求 | 常用组件 |
|---|---|---|---|
| Web 管理后台 | Element UI | 使用 `el-*` 组件和项目已有共享组件，不用其他 UI 库替代 | `el-form`、`el-select`、`el-table`、`el-dialog`、`el-upload`、`el-pagination`、`el-tag` |
| 小程序 | Vant | 使用 `van-*` 组件和项目已有业务组件，不套用 Web 后台大表格布局 | `van-cell`、`van-field`、`van-picker`、`van-popup`、`van-button`、`van-uploader`、`van-radio`、`van-tabs` |

说明：若目标仓库源码或依赖明确使用其他 Element 版本、Vant Weapp 等具体版本，以目标仓库实际依赖为准，但不得跨端替换组件库。

### 0.3 前端代码修改流程

```
1. 通过 gitnexus-hub（multica skill）定位目标页面 Vue 源码路径
2. 在 frontend-workspace/ 中克隆或更新前端仓库
3. 读取目标 .vue 文件的 <template> + <script> + <style scoped>
4. 根据需求直接修改 Vue 代码（改字段/加组件/调样式）
5. npm run dev 构建预览，在浏览器中确认效果
6. 将修改后的 .vue 文件同步到 ProtoHub-mada/modules/ 目录
```

> **v3.0 变化**：不再通过 Hub 获取源码后"生成 HTML"，而是直接在前端仓库中修改 Vue 源码并构建预览。

### 0.4 前端技术栈

| 维度 | 前端实际技术栈 | 修改方式 |
|------|--------------|---------|
| 框架 | 以目标仓库为准 | 直接修改目标页面文件 |
| UI 库 | Web：Element UI；小程序：Vant | 直接使用项目已安装的组件库 |
| 样式 | 组件库主题 + scoped CSS + 项目已有样式 | 直接修改 `<style scoped>` 或对应样式文件 |
| 主色 | `#E63935`（红色系） | 使用项目已配置的主题变量 |
| 共享组件 | Web：SearchForm / SearchItem / Table；小程序：业务 Cell / Picker / Uploader 封装 | 直接 import 使用，无需还原 |

> **v3.1 变化**：不再默认按 Element Plus 生成。先判断端类型，再选择 Web 的 Element UI 或小程序的 Vant。

### 0.5 共享组件使用规则

前端代码中的共享组件直接 import 使用，不需要还原为底层结构：

| 共享组件 | 使用方式 | 注意事项 |
|---------|---------|---------|
| `SearchForm` | `import SearchForm from '@/components/SearchForm.vue'` | 保持原有 props 传参方式 |
| `SearchItem` | 在 SearchForm 插槽中使用 | 保持原有插槽写法 |
| `Table` | `import Table from '@/components/Table.vue'` | 保持原有 columns 配置 |
| `el-descriptions` | 直接使用 Element UI / 实际 Web 组件库组件 | 保持原有 :column 属性 |
| `van-field` / `van-cell` | 直接使用 Vant 或项目业务封装组件 | 保持同页面字段顺序、label、placeholder、校验提示 |

> **v3.0 变化**：不再需要把共享组件"还原"为底层组件库结构。直接在前端项目中使用已封装的共享组件。

---

## 1. 色彩系统（前端代码对齐）

### 1.1 主色系（来自 ProtoHub tokens.css，与前端一致）

```css
:root {
  --color-primary: #E63935;
  --color-primary-hover: #D43430;
  --color-primary-active: #C1302C;
  --color-primary-light: #FFF0F0;
  --color-primary-bg: #FFF5F5;
}
```

### 1.2 语义色映射（组件库对齐）

| 场景 | 色值 | 组件库变量 | CSS 变量 |
|------|------|------------------|---------|
| 主操作、链接 | `#E63935` | `--el-color-primary` | `--color-primary` |
| 成功状态 | `#67C23A` | `--el-color-success` | `--color-success` |
| 警告提示 | `#E6A23C` | `--el-color-warning` | `--color-warning` |
| 危险操作 | `#F56C6C` | `--el-color-danger` | `--color-danger` |
| 信息/中性 | `#909399` | `--el-color-info` | `--color-info` |
| 文字主色 | `#303133` | `--el-text-color-primary` | `--color-text-primary` |
| 文字常规 | `#606266` | `--el-text-color-regular` | `--color-text-regular` |
| 文字次要 | `#909399` | `--el-text-color-secondary` | `--color-text-secondary` |
| 边框色 | `#DCDFE6` | `--el-border-color` | `--border-color` |
| 页面背景 | `#F0F2F5` | — | `--page-bg` |
| 内容区背景 | `#FFFFFF` | — | `--content-bg` |

### 1.3 状态色规范

| 状态 | 标签类型 | 背景色 | 文字色 |
|------|---------|--------|--------|
| 成功/通过 | `el-tag type="success"` | `#F0F9EB` | `#67C23A` |
| 警告/待处理 | `el-tag type="warning"` | `#FDF6EC` | `#E6A23C` |
| 危险/异常 | `el-tag type="danger"` | `#FEF0F0` | `#F56C6C` |
| 信息/中性 | `el-tag type="info"` | `#F4F4F5` | `#909399` |
| 主色/品牌 | `el-tag type="primary"` | `#FFF0F0` | `#E63935` |

---

## 2. 字体系统

```css
body {
  font-family: -apple-system, BlinkMacSystemFont, 'PingFang SC', 'Microsoft YaHei', sans-serif;
  font-size: 14px;
  line-height: 1.5;
}
```

| 层级 | 字号 | 字重 | 组件对应 |
|------|------|------|------------------|
| 页面标题 | 18-20px | 600 | 自定义标题区 |
| 卡片标题 | 16px | 600 | `el-card header` |
| 正文/表格 | 14px | 400 | `el-table` 默认 |
| 表格表头 | 13px | 500 | `el-table th` |
| 标签/辅助 | 12px | 400 | `el-tag` / `el-form-item__label` |

---

## 3. 布局结构（前端代码参考）

> **v3.0 变化**：以下结构仅供理解前端代码组织方式，修改时直接在 Vue 文件中操作，不需要"还原"。

### 3.1 页面整体布局

前端项目典型页面结构（通过路由和布局组件自动渲染）：

```
┌──────────────────────────────────────────────────┐
│  侧边栏（sidebar, 220px, #2B2F3A）  │  顶栏（56px）  │
│                                      ├──────────────┤
│  · 模块1                              │              │
│  · 模块2（active）                     │   内容区      │
│  · 模块3                              │   #F0F2F5     │
│                                      │              │
└──────────────────────────────────────────────────┘
```

> 布局组件由前端项目的 Layout 组件自动渲染，修改页面时只需关注内容区。

### 3.2 列表页标准结构（参考）

前端项目中典型列表页使用共享组件（直接 import 使用，无需还原）：

```html
<div class="app-container">
  <!-- 搜索区：SearchForm + SearchItem 还原 -->
  <el-form>
    <el-row :gutter="12">
      <el-col :sm="24" :md="12" :lg="8" :xl="6">
        <el-form-item label="订单号">
          <el-input placeholder="请输入" clearable />
        </el-form-item>
      </el-col>
      <!-- 更多筛选项... -->
      <el-col :sm="24" :md="12" :lg="8" :xl="6">
        <el-form-item>
          <el-button type="primary">查询</el-button>
          <el-button>重置</el-button>
        </el-form-item>
      </el-col>
    </el-row>
  </el-form>

  <!-- 表格区：Table 还原 -->
  <div class="table-container">
    <!-- actionBar 插槽 -->
    <div class="action-bar">
      <el-button type="primary">新增</el-button>
      <el-button>导出</el-button>
    </div>
    <!-- 表格 -->
    <el-table :data="tableData" border>
      <el-table-column prop="orderNo" label="订单号" />
      <!-- 更多列... -->
      <el-table-column label="操作" fixed="right">
        <template #default="{ row }">
          <el-button link type="primary">详情</el-button>
        </template>
      </el-table-column>
    </el-table>
    <!-- 分页 -->
    <el-pagination layout="total, sizes, prev, pager, next, jumper" />
  </div>
</div>
```

### 3.3 详情页标准结构（参考）

```html
<div class="app-container">
  <el-descriptions :column="2" border>
    <el-descriptions-item label="订单号">ZC202605011234567</el-descriptions-item>
    <el-descriptions-item label="退款原因">车辆故障</el-descriptions-item>
    <!-- 更多字段... -->
  </el-descriptions>
</div>
```

### 3.4 弹框标准结构（参考）

```html
<el-dialog title="审批通过" width="500px">
  <el-form>
    <el-form-item label="备注" required>
      <el-input type="textarea" />
    </el-form-item>
  </el-form>
  <template #footer>
    <el-button @click="dialogVisible = false">取消</el-button>
    <el-button type="primary">确定</el-button>
  </template>
</el-dialog>
```

---

## 4. 修改规范

### 4.1 必须遵守

- ✅ 直接在前端仓库中修改 Vue 源码，不生成独立 HTML
- ✅ 修改时保持原有 `<template>` 结构和 `<style scoped>` 样式风格
- ✅ 使用目标端组件库（Web：Element UI；小程序：Vant），不自定义替代组件
- ✅ 共享组件或业务组件直接 import 使用（Web 如 SearchForm / SearchItem / Table；小程序如业务 Cell / Picker / Uploader 封装），不还原为底层结构
- ✅ 颜色使用 CSS 变量或对应组件库主题变量，不硬编码
- ✅ 新增内容与原有内容使用完全一致的组件和 props
- ✅ 模拟数据使用真实枚举值（来自 gitnexus-hub）和合理业务数据

### 4.2 禁止行为

- ❌ 生成独立 HTML 文件代替修改 Vue 代码
- ❌ 自定义设计体系（不使用目标端组件库，自己写 CSS 组件库）
- ❌ 用 Bootstrap、Ant Design 等其他 UI 框架替代 Web 的 Element UI，或用 Web 组件替代小程序 Vant
- ❌ 添加源码中不存在的自定义 CSS 类（Tailwind 工具类除外）
- ❌ 添加源码中不存在的装饰组件、标注样式
- ❌ 改变字段顺序、删减字段、添加源码中不存在的字段（PRD 变更除外）

### 4.3 页面无标注原则

修改后的页面展示的是**部署后的真实页面状态**，不加任何标注装饰：
- 无橙色边框、无"PRD新增"标签、无灰色删除线
- 变更说明放在 PRD 文档中，不侵入页面代码

---

## 5. ProtoHub 仓库历史样式（仅旧 HTML 页面使用）

> ⚠️ **v3.0 说明**：以下样式仅适用于 ProtoHub-mada 仓库内旧的 `.html` 文件（`shared/design-tokens/tokens.css`）。
> 新的修改通过前端仓库 Vue 代码进行，不使用以下样式。本节仅作历史参考。

### 5.1 设计令牌

| CSS 变量 | 用途 | 值 |
|---------|------|-----|
| `--color-primary` | 品牌主色 | `#E63935` |
| `--color-primary-hover` | 主色悬停 | `#D43430` |
| `--color-primary-light` | 主色浅色 | `#FFF0F0` |
| `--sidebar-bg` | 侧边栏背景 | `#2B2F3A` |
| `--sidebar-width` | 侧边栏宽度 | `220px` |
| `--header-height` | 顶栏高度 | `56px` |
| `--page-bg` | 页面背景 | `#F0F2F5` |
| `--content-bg` | 内容区背景 | `#FFFFFF` |
| `--color-text-primary` | 主文字 | `#303133` |
| `--color-text-regular` | 常规文字 | `#606266` |
| `--border-color` | 边框色 | `#DCDFE6` |

### 5.2 引入方式

```html
<!-- ProtoHub 仓库内页面必须引入 -->
<link rel="stylesheet" href="../../shared/design-tokens/tokens.css">
<script src="../../shared/components/layout.js"></script>
```

---

## 6. 质量验证清单

前端代码修改后，逐项检查：

| 检查项 | 通过标准 |
|--------|---------|
| 修改方式 | 直接修改了 Vue 源码，未生成独立 HTML |
| 组件类型一致 | 新增元素与源码中最相似元素使用相同端组件库组件 |
| Props 一致 | 新增元素的 props（clearable / filterable / collapse-tags 等）与同级元素一致 |
| 共享组件 | 直接 import 使用 SearchForm/Table 等，未还原为底层结构 |
| 样式来源 | CSS 类名来自源码 `<style scoped>`，无自定义类（Tailwind 工具类除外） |
| 无标注装饰 | 页面上无红色高亮、角标、删除线等标注元素 |
| 模拟数据 | 使用真实枚举值和合理业务数据，不用"测试1""数据2" |
| 构建通过 | `npm run dev` 能正常启动，页面无编译错误 |
| 同步到 ProtoHub | 修改的 .vue 文件已复制到 ProtoHub-mada/modules/ 目录 |

---

_最后更新：2026-07-07_
