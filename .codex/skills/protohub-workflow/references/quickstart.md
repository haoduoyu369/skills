# ProtoHub-mada 快速上手

> 3 分钟读完，任何 AI 工具都能用。完整手册见 `docs/team-guide.md`。
>
> 历史说明：本文保留 v3.1 Git Subtree 快速上手口径。当前主流程以 `SKILL.md` v3.3 为准：原型设计需在需求大纲、产品方案/流程图、研发版 PRD 确认后启动；通过 gitnexus-hub 获取 Vue 源码并放入 `preview/` 修改，Hub 不可用时才生成 HTML 兜底。组件库要求：Web 使用 Element UI，小程序使用 Vant。

---

## 你是什么工具？

| 你的工具 | 怎么用 |
|---------|--------|
| **智能体** | 直接打开本目录，Skill 自动加载，对 AI 说话即可 |
| **其他 AI 工具** | 把本文件内容粘贴给 AI，加上你的需求 |

---

## 一、首次使用（每人一次）

```bash
# 1. 克隆 ProtoHub 仓库（⚠️ HTTP+密码已禁用，使用 SSH 或 Token）
# 方式一（推荐）：SSH 协议
git clone -b dev git@git.17usoft.com:LY-MDSCR/ProtoHub-mada.git
# 方式二：域账号 + Token
git clone -b dev http://oauth2:<你的TOKEN>@git.17usoft.com/LY-MDSCR/ProtoHub-mada.git
cd ProtoHub-mada

# 2. 配置鉴权（按克隆方式选择其一）
#    SSH 方式：无需额外配置，跳过本步
#    Token 方式：配置 remote URL（去 git.17usoft.com → Settings → Access Tokens 创建）
#    Token 权限勾选：read_repository + write_repository
git remote rename origin inner
# SSH：git remote set-url inner git@git.17usoft.com:LY-MDSCR/ProtoHub-mada.git
# Token：git remote set-url inner http://oauth2:<你的TOKEN>@git.17usoft.com/LY-MDSCR/ProtoHub-mada.git

# 3. 添加上游前端仓库 remote（Git Subtree 同步用）
git remote add upstream git@git.17usoft.com:LY-MDSCR/mdscr-fe-admin.git
# 或 Token：git remote add upstream http://oauth2:<TOKEN>@git.17usoft.com/LY-MDSCR/mdscr-fe-admin.git

# 4. 验证
git pull inner dev
git fetch upstream

# 5. 安装前端依赖（frontend/ 已通过 Git Subtree 内嵌）
cd frontend
npm install
npm run dev    # 启动预览
```

---

## 二、日常改原型（4 句话）

```
1.「拉最新代码，检查一下上游有没有更新」
2.「帮我把 [frontend/src/views/页面路径] 的 [具体改动]」
3.（预览后）「满意了，帮我检查关联影响」
4.「可以推了」
```

就这 4 步。AI 会自动处理拉取、上游同步检查、修改 Vue 代码、构建预览、关联检查、commit、推送。

---

## 三、核心规则（AI 必须遵守）

1. **前端代码驱动**：直接修改 `frontend/` 目录中的 Vue 源码（Git Subtree 同步），不生成独立 HTML
2. **先拉后改**：不拉最新代码不准改
3. **先读后改**：改之前必须先 Read 目标 Vue 文件，不凭空写
4. **「可以推了」才推**：用户不说不推
5. **关联检查不可跳过**：推送前必须查 `docs/data-flow-map.md`
6. **组件复用优先**：Web 使用 Element UI 组件和项目已有共享组件，小程序使用 Vant 组件和项目业务组件，不自定义替代
7. **一次一模块**：一次只改一个页面，改完立即推
8. **原型隔离**：新增页面放 `frontend/src/views/prototype/`，避免与上游冲突

---

## 四、Commit 规范

格式：`type(scope): 说明`

| type | 场景 | 示例 |
|------|------|------|
| feat | 新功能 | `feat(order-list): 搜索栏增加统计卡片` |
| fix | 修复 | `fix(order-pickup): 修复时间选择器问题` |
| refactor | 重构 | `refactor(vehicle-detail): 重写状态展示` |
| style | 样式 | `style(global): 统一表格 hover 背景` |
| docs | 文档 | `docs(data-flow-map): 新增调度模块` |

---

## 五、前端代码修改规范

v3.1 起前端代码通过 Git Subtree 内嵌在 `frontend/` 目录，路径与上游完全一致。

**修改流程**：
1. Read `frontend/src/views/` 下的目标 `.vue` 文件
2. 直接修改 Vue 模板、脚本、样式
3. `cd frontend && npm run dev` 构建预览
4. 满意后直接 commit（无需 cp 同步，文件已在 ProtoHub 仓库中）

**状态颜色规范**（与前端项目一致）：

| 状态类型 | 颜色 |
|----------|------|
| 成功/已完成 | `#52C41A` 绿色 |
| 进行中/处理中 | `#1890FF` 蓝色 |
| 警告/待处理 | `#FAAD14` 橙色 |
| 危险/异常/取消 | `#F5222D` 红色 |
| 中性/默认 | `#8C8C8C` 灰色 |

**禁止行为**：
- ❌ 生成独立 HTML 文件
- ❌ 引入 CDN 脚本
- ❌ 自定义 CSS 设计体系

---

## 六、目录结构

```
ProtoHub-mada/
├── frontend/                   # 前端代码（Git Subtree，路径与上游一致）
│   ├── src/views/              # Vue 页面源码（修改目标）
│   │   ├── sale/order/         # 上游已有页面（直接修改）
│   │   ├── prototype/          # 原型专属目录（新增页面放这里，永不冲突）
│   │   └── ...
│   ├── package.json
│   └── vite.config.ts
├── shared/                     # 历史共享资源（仅旧 HTML 页面使用）
├── docs/                       # 文档
│   ├── team-guide.md           # 完整操作手册
│   ├── style-guide.md          # 前端代码修改规范
│   ├── data-flow-map.md        # ⭐ 改动关联检查依据
│   ├── change-log.md           # 变更日志
│   ├── upstream-sync-log.md    # 上游同步记录
│   └── conflict-resolution.md  # 冲突解决手册
├── scripts/                    # 脚本工具
└── tmp/                        # 运行时临时文件（不提交）
```

---

## 七、给非智能体 AI 的完整提示词

如果你用的是其他 AI 工具，把以下内容粘贴给它：

```
你是 ProtoHub-mada 原型仓库的协作助手。请遵循以下规则：

1. v3.1 Git Subtree 架构：前端代码在 frontend/ 目录中（Git Subtree 同步），路径与上游一致
2. 修改前先 Read 目标 .vue 文件，不凭空写
3. Web 使用 Element UI 组件和项目已有共享组件；小程序使用 Vant 组件和项目业务组件，不自定义替代
4. 修改后用 cd frontend && npm run dev 构建预览
5. 新增页面放 frontend/src/views/prototype/ 下，避免与上游冲突
6. 推送前查 docs/data-flow-map.md 确认关联影响
7. Commit 格式：type(scope): 中文说明
8. 我说「可以推了」才执行 git push
9. 每次只改一个页面，改完立即推

现在请帮我：[你的需求]
```

---

## 八、遇到问题

| 问题 | 解决 |
|------|------|
| Token 过期 | git.17usoft.com → Settings → Access Tokens 重新生成 |
| 推送 403 | Token 权限不足，需 `read_repository` + `write_repository` |
| 推送被拒 | `git pull inner dev --rebase` 后重试 |
| npm install 慢 | `npm config set registry https://registry.npmmirror.com` |
| npm run dev 失败 | 检查 Node.js 版本，清除 `node_modules` 重装 |
| 不确定改哪 | 查 `docs/data-flow-map.md` 业务术语映射表 |
| 上游同步冲突 | 按 `docs/conflict-resolution.md` 分层规则处理 |
| upstream 不存在 | `git remote add upstream git@git.17usoft.com:LY-MDSCR/mdscr-fe-admin.git` |
