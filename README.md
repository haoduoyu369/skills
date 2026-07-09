# 产品方案设计工具包 / prd-writer

版本：2026-07-09

主 skill：`prd-writer`（固定 6 模块研发版 PRD 生成工具）。

仓库为单 skill 仓库，根目录即为 `prd-writer` 的入口。

## 通过 URL 导入

第三方 skill 导入工具可直接使用：

```
https://github.com/haoduoyu369/skills
```

工具会在仓库根目录读取 `SKILL.md`。

## 包含内容

仓库根即为 skill 入口：

```
/
├── SKILL.md                # 主入口
├── CLAUDE.md
├── MANIFEST.md
├── README.md
├── .gitignore
├── references/
│   ├── examples.md
│   ├── feedback_log.md
│   ├── pending_mapping.md
│   ├── prd-template.md
│   ├── prototype-rules.md
│   ├── self-audit-checklist.md
│   ├── system-sensing.md
│   ├── term-mapping.md
│   ├── walle-parser.md
│   ├── 原型生成方案.md
│   └── 踩坑记录.md
└── scripts/
    ├── hub_client.py
    ├── render_mermaid.py
    ├── screenshot.py
    ├── validate_prototype.py
    ├── mermaid.min.js
    └── restart-od.sh
```

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

把仓库根的所有内容复制到目标项目的 `.codex/skills/prd-writer/` 下：

```bash
# 在仓库根目录执行
mkdir -p /path/to/target-project/.codex/skills/prd-writer
cp -R SKILL.md CLAUDE.md MANIFEST.md README.md references scripts /path/to/target-project/.codex/skills/prd-writer/
```

如果目标项目已有同名 skill，请先备份或确认覆盖策略。

## 鉴权和本机配置

本包不包含任何个人鉴权文件。

- GitNexus Hub、Toca Wiki、Chrome 登录态等能力依赖使用方本机环境和权限。
- `prd-writer/scripts/mermaid.min.js` 已打包，用于本地渲染流程图。

## 分发前检查

已排除：

- `.DS_Store`
- `x-auth-token.txt`
- `*.pyc`
- 个人 token / secret 文件
