#!/usr/bin/env python3
"""
Mermaid 图表渲染器——将 Mermaid 代码渲染为 PNG 图片。

使用 Playwright（无头浏览器）渲染 Mermaid 图表，不依赖外部 API 或 npm 包。

用法：
  # 渲染单个图表
  python3 scripts/render_mermaid.py --code "graph TD\n    A-->B" --output diagrams/flow.png

  # 从文件读取 Mermaid 代码
  python3 scripts/render_mermaid.py --input diagrams/flow.mmd --output diagrams/flow.png

  # 指定图表类型（默认自动检测）
  python3 scripts/render_mermaid.py --input diagrams/seq.mmd --output diagrams/seq.png --type sequence

  # 指定宽度和背景色
  python3 scripts/render_mermaid.py --input flow.mmd --output flow.png --width 1200 --bg white

支持的图表类型：
  flowchart / graph — 流程图
  sequenceDiagram — 时序图
  erDiagram — ER 实体关系图
  classDiagram — 类图
  stateDiagram — 状态图
  gantt — 甘特图
  mindmap — 思维导图
  pie — 饼图
  gitGraph — Git 分支图
"""

import argparse
import os
import sys
import tempfile
import time

# Mermaid JS 本地文件（优先）和 CDN（回退）
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MERMAID_LOCAL = os.path.join(SCRIPT_DIR, "mermaid.min.js")
MERMAID_CDN = "https://unpkg.com/mermaid@11/dist/mermaid.min.js"


def build_html(mermaid_code: str, bg_color: str = "white", width: int = 1200) -> str:
    """构建包含 Mermaid 图表的 HTML 页面。"""
    # 优先用本地 Mermaid JS，不存在则用 CDN
    if os.path.exists(MERMAID_LOCAL):
        mermaid_src = f"file://{MERMAID_LOCAL}"
    else:
        mermaid_src = MERMAID_CDN
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {{
    margin: 0;
    padding: 20px;
    background: {bg_color};
    display: flex;
    justify-content: center;
  }}
  #mermaid-container {{
    max-width: {width}px;
  }}
  #mermaid-container svg {{
    max-width: 100%;
    height: auto;
  }}
</style>
</head>
<body>
<div id="mermaid-container">
<pre class="mermaid">
{mermaid_code}
</pre>
</div>
<script src="{mermaid_src}"></script>
<script>
  mermaid.initialize({{
    startOnLoad: true,
    theme: 'default',
    securityLevel: 'loose',
    flowchart: {{ useMaxWidth: true, htmlLabels: true }},
    sequence: {{ useMaxWidth: true }},
    er: {{ useMaxWidth: true }},
  }});
</script>
</body>
</html>"""


def render(mermaid_code: str, output_path: str, bg_color: str = "white",
           width: int = 1200, timeout: int = 30) -> bool:
    """用 Playwright 渲染 Mermaid 图表并保存为 PNG。"""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("错误：需要安装 playwright。运行：pip install playwright && playwright install chromium",
              file=sys.stderr)
        return False

    html_content = build_html(mermaid_code, bg_color, width)

    # 写入临时 HTML 文件
    with tempfile.NamedTemporaryFile(suffix=".html", mode="w", encoding="utf-8",
                                      delete=False) as f:
        f.write(html_content)
        html_path = f.name

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": width + 40, "height": 800})

            # 加载 HTML
            page.goto(f"file://{html_path}")

            # 等待 Mermaid 渲染完成（检测 SVG 元素出现）
            try:
                page.wait_for_selector("#mermaid-container svg", timeout=timeout * 1000)
            except Exception:
                print("警告：等待 SVG 渲染超时，尝试截图当前状态", file=sys.stderr)

            # 额外等待确保渲染稳定
            time.sleep(0.5)

            # 获取 SVG 元素的边界框
            bbox = page.evaluate("""
                () => {
                    const svg = document.querySelector('#mermaid-container svg');
                    if (!svg) return null;
                    const rect = svg.getBoundingClientRect();
                    return { x: rect.x, y: rect.y, width: rect.width, height: rect.height };
                }
            """)

            if bbox:
                # 只截取 SVG 区域（加 padding）
                padding = 20
                page.screenshot(
                    path=output_path,
                    clip={
                        "x": max(0, bbox["x"] - padding),
                        "y": max(0, bbox["y"] - padding),
                        "width": bbox["width"] + padding * 2,
                        "height": bbox["height"] + padding * 2,
                    },
                )
            else:
                # 回退：截取整个页面
                page.screenshot(path=output_path, full_page=True)

            browser.close()

        # 验证输出文件
        if os.path.exists(output_path) and os.path.getsize(output_path) > 100:
            return True
        else:
            print(f"错误：输出文件过小或不存在：{output_path}", file=sys.stderr)
            return False

    finally:
        # 清理临时文件
        os.unlink(html_path)


def main():
    parser = argparse.ArgumentParser(description="Mermaid 图表渲染器（Playwright）")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--code", type=str, help="Mermaid 代码（直接传入）")
    group.add_argument("--input", type=str, help="Mermaid 代码文件路径")
    parser.add_argument("--output", type=str, required=True, help="输出 PNG 文件路径")
    parser.add_argument("--bg", type=str, default="white", help="背景色（默认 white）")
    parser.add_argument("--width", type=int, default=1200, help="渲染宽度（默认 1200）")
    parser.add_argument("--timeout", type=int, default=30, help="渲染超时秒数（默认 30）")
    parser.add_argument("--type", type=str, help="图表类型提示（目前仅用于日志）")

    args = parser.parse_args()

    # 获取 Mermaid 代码
    if args.code:
        mermaid_code = args.code.replace("\\n", "\n")
    else:
        with open(args.input, "r", encoding="utf-8") as f:
            mermaid_code = f.read()

    if not mermaid_code.strip():
        print("错误：Mermaid 代码为空", file=sys.stderr)
        sys.exit(1)

    # 确保输出目录存在
    output_dir = os.path.dirname(args.output)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    # 渲染
    print(f"渲染 Mermaid 图表 → {args.output}")
    if args.type:
        print(f"  类型：{args.type}")
    print(f"  宽度：{args.width}px")

    success = render(mermaid_code, args.output, args.bg, args.width, args.timeout)

    if success:
        size = os.path.getsize(args.output)
        print(f"  ✅ 完成（{size} bytes）")
    else:
        print(f"  ❌ 渲染失败", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
