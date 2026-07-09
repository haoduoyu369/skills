# MANIFEST

## Skills

- `.codex/skills/prd-writer`
  - `SKILL.md`
  - `CLAUDE.md`
  - `references/*.md`
  - `scripts/hub_client.py`
  - `scripts/render_mermaid.py`
  - `scripts/screenshot.py`
  - `scripts/validate_prototype.py`
  - `scripts/mermaid.min.js`
  - `scripts/restart-od.sh`
- `.codex/skills/structured-prd-writer`
  - `SKILL.md`
  - `references/style-guide.md`
- `.codex/skills/protohub-workflow`
  - `SKILL.md`
  - `references/team-guide.md`
  - `references/quickstart.md`
  - `references/style-guide.md`
  - `references/data-flow-map.md`
- `.codex/skills/historical-context-query`
  - `SKILL.md`
- `.codex/skills/rds-api-query`
  - `SKILL.md`
  - `api-payload-reference.md`
  - `order-connection-reference.md`
  - `store-connection-reference.md`
  - `violation-connection-reference.md`
  - `.gitignore`

## Excluded

- `.DS_Store`
- `x-auth-token.txt`
- `*.pyc`
- personal token / secret files

## Notes

- RDS query skill is included as an optional downstream tool without credential files.
- ProtoHub workflow is included because PRD confirmation can hand off into prototype design.
- Historical context query is included because the product design flow may call it before PRD writing.
