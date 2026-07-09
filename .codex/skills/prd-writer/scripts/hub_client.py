#!/usr/bin/env python3
"""
GitNexus Hub 客户端——通过 HTTP API 直接访问远程 Hub，获取公司仓库的代码信息。

解决的问题：
  Hub 已部署到正式环境（http://ibd.travel.t.17usoft.com/gitnexus/mcp）。
  multica 平台封装了 gitnexus-hub skill，约束大模型调用 MCP 时的层级深度。
  本脚本直接调用 Hub HTTP API，适用于需要精确控制查询参数的场景，
  也可作为 MCP 工具不可用时的备选方案。

用法：
  # 列出所有仓库
  python3 scripts/hub_client.py list-repos

  # 列出已索引的仓库（过滤掉未索引的）
  python3 scripts/hub_client.py list-repos --indexed

  # Cypher 查询（查文件列表、枚举、属性等）
  python3 scripts/hub_client.py cypher --repo LY-MDSCR__mdscr-fe-admin \
    --query 'MATCH (f:File) WHERE f.filePath CONTAINS "tagStrategy" RETURN f.filePath LIMIT 10'

  # 获取符号上下文（含源码）
  python3 scripts/hub_client.py context --repo LY-MDSCR__mdscr-fe-admin \
    --uid "File:src/views/income/tagStrategyConfigList/index.vue" --content

  # 获取符号上下文（不含源码，只看引用关系）
  python3 scripts/hub_client.py context --repo LY-MDSCR__mdscr-fe-admin \
    --uid "Enum:src/enums/CarAgeTagEnum.ts:CarAgeTagEnum"

  # 关键词搜索执行流
  python3 scripts/hub_client.py query --repo LY-MDSCR__mdscr-fe-admin \
    --query "TagStrategy tag strategy config"

  # 搜索仓库（按关键词过滤）
  python3 scripts/hub_client.py list-repos --search vehicle

输出：
  - list-repos: 仓库列表（registry_name + 索引状态）
  - cypher: 查询结果的 markdown 表格
  - context: 符号的引用关系 + 源码（如果 --content）
  - query: 匹配的执行流和符号
"""

import argparse
import json
import sys
import urllib.request
import urllib.error

HUB_URL = "http://ibd.travel.t.17usoft.com/gitnexus/mcp"
TIMEOUT = 30  # 秒

# 缓存 session id（同一进程内复用）
_session_id = None


def _initialize_session() -> str:
    """MCP 协议要求先 initialize 获取 session id，后续请求需带上。"""
    global _session_id
    if _session_id:
        return _session_id

    payload = {
        "jsonrpc": "2.0",
        "id": 0,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "hub_client.py", "version": "1.0.0"}
        }
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        HUB_URL,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            # session id 在响应头中
            _session_id = resp.headers.get("mcp-session-id") or resp.headers.get("Mcp-Session-Id")
            resp.read()  # 消费响应体
    except urllib.error.URLError as e:
        print(f"错误：Hub initialize 失败（{HUB_URL}）：{e}", file=sys.stderr)
        sys.exit(1)

    if not _session_id:
        print("错误：Hub initialize 未返回 session id", file=sys.stderr)
        sys.exit(1)

    return _session_id


def call_hub(tool_name: str, arguments: dict) -> dict:
    """调用 Hub MCP 工具，返回解析后的结果。"""
    session_id = _initialize_session()

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments
        }
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        HUB_URL,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "Mcp-Session-Id": session_id,
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            raw = resp.read().decode("utf-8")
    except urllib.error.URLError as e:
        print(f"错误：无法连接 Hub（{HUB_URL}）：{e}", file=sys.stderr)
        sys.exit(1)

    # 解析 SSE 格式：响应可能是纯 JSON 或多行 data: 格式
    for line in raw.split("\n"):
        line = line.strip()
        if line.startswith("data:"):
            line = line[5:]
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue

        # MCP 响应格式：result.content[0].text 里是 JSON 字符串
        if "result" in msg:
            content_list = msg["result"].get("content", [])
            is_error = msg["result"].get("isError", False)
            if content_list and "text" in content_list[0]:
                text = content_list[0]["text"]
                if is_error:
                    print(f"Hub 错误：{text}", file=sys.stderr)
                    sys.exit(1)
                try:
                    return json.loads(text)
                except json.JSONDecodeError:
                    # 有些工具返回纯文本而非 JSON（如 query 空结果）
                    return {"raw_text": text}
        if "error" in msg:
            print(f"Hub 错误：{msg['error']}", file=sys.stderr)
            sys.exit(1)

    print("错误：Hub 响应格式无法解析", file=sys.stderr)
    print(f"原始响应（前 500 字符）：{raw[:500]}", file=sys.stderr)
    sys.exit(1)


def cmd_list_repos(args):
    """列出仓库。"""
    result = call_hub("list_repos", {})

    repos = result if isinstance(result, list) else []

    # 关键词过滤
    if args.search:
        keyword = args.search.lower()
        repos = [r for r in repos if keyword in r.get("registry_name", "").lower()
                 or keyword in r.get("path_with_namespace", "").lower()]

    # 只展示已索引的
    if args.indexed:
        repos = [r for r in repos if r.get("indexed") or r.get("gitnexus_graph_generated")]

    if not repos:
        print("未找到匹配的仓库")
        return

    # 输出表格
    print(f"{'仓库名（registry_name）':<50} {'路径':<45} {'索引状态'}")
    print("-" * 110)
    for r in repos:
        name = r.get("registry_name", "?")
        path = r.get("path_with_namespace", "?")
        indexed = "✅" if r.get("indexed") or r.get("gitnexus_graph_generated") else "❌"
        status = r.get("gitnexus_graph_status", "")
        status_str = indexed
        if status and status != "indexed":
            status_str += f" ({status})"
        print(f"{name:<50} {path:<45} {status_str}")

    print(f"\n共 {len(repos)} 个仓库")


def cmd_cypher(args):
    """执行 Cypher 查询。"""
    if not args.repo:
        print("错误：cypher 命令需要 --repo 参数", file=sys.stderr)
        sys.exit(1)

    result = call_hub("cypher", {"repo": args.repo, "query": args.query})

    if isinstance(result, dict):
        md = result.get("markdown", "")
        row_count = result.get("row_count", 0)
        if md:
            print(md)
            print(f"\n（{row_count} 行结果）")
        else:
            print("查询无结果")
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_context(args):
    """获取符号上下文。"""
    if not args.repo or not args.uid:
        print("错误：context 命令需要 --repo 和 --uid 参数", file=sys.stderr)
        sys.exit(1)

    arguments = {"repo": args.repo, "uid": args.uid}
    if args.content:
        arguments["content"] = True

    result = call_hub("context", arguments)

    if isinstance(result, dict) and "symbol" in result:
        sym = result["symbol"]

        # 输出基本信息
        print(f"名称：{sym.get('name', '?')}")
        print(f"路径：{sym.get('filePath', '?')}")
        print(f"UID：{sym.get('uid', '?')}")

        # 如果有源码，输出源码
        content = sym.get("content", "")
        if content:
            print(f"\n{'='*60}")
            print("源码：")
            print(f"{'='*60}")
            print(content)
            print(f"{'='*60}")
            print(f"（源码长度：{len(content)} 字符）")

        # 如果有引用关系，输出引用
        refs = result.get("references", {})
        if refs:
            print(f"\n引用关系：")
            print(json.dumps(refs, indent=2, ensure_ascii=False)[:2000])
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False)[:5000])


def cmd_query(args):
    """搜索执行流和符号。"""
    if not args.repo:
        print("错误：query 命令需要 --repo 参数", file=sys.stderr)
        sys.exit(1)

    # Hub API 的参数名是 search_query（不是 query）
    arguments = {"repo": args.repo, "search_query": args.query}
    if args.goal:
        arguments["goal"] = args.goal
    if args.limit:
        arguments["limit"] = int(args.limit)

    result = call_hub("query", arguments)

    if isinstance(result, dict):
        # 输出 processes
        processes = result.get("processes", [])
        if processes:
            print(f"=== 执行流（{len(processes)} 个）===")
            for p in processes:
                label = p.get("heuristicLabel", p.get("name", "?"))
                print(f"  - {label}")

        # 输出 symbols
        symbols = result.get("process_symbols", result.get("symbols", []))
        if symbols:
            print(f"\n=== 相关符号（{len(symbols)} 个）===")
            for s in symbols[:20]:
                name = s.get("name", "?")
                fp = s.get("filePath", "?")
                kind = s.get("kind", "")
                print(f"  - [{kind}] {name} → {fp}")

        # 输出 definitions
        defs = result.get("definitions", [])
        if defs:
            print(f"\n=== 独立定义（{len(defs)} 个）===")
            for d in defs[:10]:
                name = d.get("name", "?")
                fp = d.get("filePath", "?")
                print(f"  - {name} → {fp}")

        if not processes and not symbols and not defs:
            print("搜索无结果")
            print(json.dumps(result, indent=2, ensure_ascii=False)[:1000])
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False)[:5000])


def main():
    parser = argparse.ArgumentParser(
        description="GitNexus Hub 客户端——直接访问远程 Hub HTTP API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", help="子命令")

    # list-repos
    p_list = sub.add_parser("list-repos", help="列出仓库")
    p_list.add_argument("--indexed", action="store_true", help="只显示已索引的仓库")
    p_list.add_argument("--search", type=str, help="按关键词过滤仓库名")

    # cypher
    p_cypher = sub.add_parser("cypher", help="执行 Cypher 查询")
    p_cypher.add_argument("--repo", type=str, required=True, help="仓库名（如 LY-MDSCR__mdscr-fe-admin）")
    p_cypher.add_argument("--query", type=str, required=True, help="Cypher 查询语句")

    # context
    p_ctx = sub.add_parser("context", help="获取符号上下文（可含源码）")
    p_ctx.add_argument("--repo", type=str, required=True, help="仓库名")
    p_ctx.add_argument("--uid", type=str, required=True, help="符号 UID（如 File:src/views/...）")
    p_ctx.add_argument("--content", action="store_true", help="包含源码内容")

    # query
    p_query = sub.add_parser("query", help="搜索执行流和符号")
    p_query.add_argument("--repo", type=str, required=True, help="仓库名")
    p_query.add_argument("--query", type=str, required=True, help="搜索关键词")
    p_query.add_argument("--goal", type=str, help="搜索目标描述（提升相关性排序）")
    p_query.add_argument("--limit", type=str, default="5", help="最多返回几个执行流（默认 5）")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    commands = {
        "list-repos": cmd_list_repos,
        "cypher": cmd_cypher,
        "context": cmd_context,
        "query": cmd_query,
    }

    commands[args.command](args)


if __name__ == "__main__":
    main()
