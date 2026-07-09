# 产品方案设计工具包

版本：2026-07-09

这个包用于分发最新的产品方案设计流程给同事。核心能力是生成固定 6 模块研发版 PRD，并在 PRD 确认后衔接 ProtoHub 原型流程。

## 包含内容

| 目录 | 用途 |
|---|---|
| `.codex/skills/prd-writer` | 主产品方案设计 / PRD 生成工具，已更新为固定 6 模块研发版 PRD |
| `.codex/skills/structured-prd-writer` | 结构化需求拆解工具，Phase 6 已同步为固定 6 模块研发版 PRD |
| `.codex/skills/protohub-workflow` | PRD 确认后的 ProtoHub 原型下游流程 |
| `.codex/skills/historical-context-query` | 需求分析前的历史上下文 / 代码逻辑查询流程 |
| `.codex/skills/rds-api-query` | 可选 RDS 只读查询工具说明，不包含个人鉴权 token |

## PRD 固定模块

研发版 PRD 只包含以下 6 个一级模块：

1. 需求版本管理
2. 需求背景
3. 流程图
4. 功能清单
5. 详细需求
6. 验收用例

版本规则：

- 评审时为 `V1.0`
- 评审通过后按评审意见修改为 `V1.1`
- 后续开发、测试提 bug 单引发需求调整时按 `V1.2`、`V1.3` 继续递增

## 安装方式

把本包里的 `.codex/skills/*` 复制到目标项目的 `.codex/skills/` 下。

示例：

```bash
cp -R .codex/skills/* /path/to/target-project/.codex/skills/
```

如果目标项目已有同名 skill，请先备份或确认覆盖策略。

## 使用建议

1. 写 PRD 时优先使用 `prd-writer`。
2. 输入文本本身层级复杂、规则分支多时，使用 `structured-prd-writer`。
3. 做需求分析前，如需要查历史代码或历史需求，先使用 `historical-context-query`。
4. PRD 确认后再进入 `protohub-workflow` 原型流程。

## 鉴权和本机配置

本包不包含任何个人鉴权文件。

- `rds-api-query/x-auth-token.txt` 未打包，同事如需用 RDS 查询，需要自行配置。
- GitNexus Hub、Toca Wiki、Chrome 登录态等能力依赖同事本机环境和权限。
- `prd-writer/scripts/mermaid.min.js` 已打包，用于本地渲染流程图。

## 分发前检查

已排除：

- `.DS_Store`
- `x-auth-token.txt`
- `*.pyc`
- 个人 token / secret 文件
