# PRD 生成项目

进入本项目时，请先 `Read SKILL.md` 了解完整工作流程。

使用 `/prd-writer` 命令启动 PRD 生成流程。

## 关键约定

- **Hub 查询**：推荐使用 MCP 工具（multica `gitnexus-hub` skill 已约束调用层级），`hub_client.py` 脚本作为备选
- **图片文件**：禁止用 Read 工具查看 png/jpg/gif 等图片文件
- **文件状态机**：每步产出必须写入磁盘文件，后续步骤通过 Read 读取（不依赖上下文记忆）
