#!/usr/bin/env python3
"""
原型截图脚本
用法: python3 screenshot.py <html文件路径> [输出png路径]

如果未指定输出路径，默认与 HTML 同目录同名（.html → .png）。
"""

import sys
import os
import time
from pathlib import Path


def take_screenshot(html_path: str, png_path: str | None = None) -> str:
    """
    打开 HTML 原型文件，等待渲染完成后截图。

    Args:
        html_path: HTML 文件的绝对路径或相对路径
        png_path: 输出 PNG 路径（可选，默认与 HTML 同目录同名）

    Returns:
        截图文件的绝对路径
    """
    html_path = os.path.abspath(html_path)

    if not os.path.exists(html_path):
        print(f"错误: 文件不存在 - {html_path}", file=sys.stderr)
        sys.exit(1)

    if png_path is None:
        png_path = str(Path(html_path).with_suffix(".png"))
    else:
        png_path = os.path.abspath(png_path)

    # 确保输出目录存在
    os.makedirs(os.path.dirname(png_path), exist_ok=True)

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("错误: playwright 未安装。执行: pip3 install playwright", file=sys.stderr)
        sys.exit(1)

    file_url = f"file://{html_path}"

    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=True)
        except Exception as e:
            error_msg = str(e)
            if "Executable doesn't exist" in error_msg:
                print(
                    "错误: Chromium 浏览器未安装。执行: python3 -m playwright install chromium",
                    file=sys.stderr,
                )
            else:
                print(f"错误: 无法启动浏览器 - {e}", file=sys.stderr)
            sys.exit(1)

        page = browser.new_page(viewport={"width": 1440, "height": 900})

        print(f"打开: {file_url}")
        page.goto(file_url, wait_until="networkidle")

        # 等待 Vue + Element Plus 渲染完成
        # 策略：等待 #app 内出现实际内容（el-descriptions / el-table / el-form）
        try:
            page.wait_for_selector(
                "#app .el-descriptions, #app .el-table, #app .el-form, #app .el-button",
                timeout=15000,
            )
            # 额外等待 500ms，确保动画和样式渲染完毕
            time.sleep(0.5)
            print("渲染完成")
        except Exception:
            # 兜底：如果选择器匹配失败，固定等待 3 秒
            print("等待固定 3 秒后截图...")
            time.sleep(3)

        # 截图（全页面）
        page.screenshot(path=png_path, full_page=True)
        print(f"截图已保存: {png_path}")

        browser.close()

    return png_path


def main():
    if len(sys.argv) < 2:
        print("用法: python3 screenshot.py <html文件路径> [输出png路径]")
        print("示例: python3 screenshot.py prototypes/639911-退款审批详情.html")
        sys.exit(1)

    html_path = sys.argv[1]
    png_path = sys.argv[2] if len(sys.argv) > 2 else None

    result = take_screenshot(html_path, png_path)
    print(f"\n完成: {result}")


if __name__ == "__main__":
    main()
