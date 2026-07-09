#!/usr/bin/env python3
"""
HTML 原型 vs Vue 源码一致性验证脚本。

从 HTML 原型和 Vue 源码中提取 Element Plus 组件字段（el-form-item / el-descriptions-item /
el-table-column / el-col），比对一致性，报告差异。

用法：
  python3 scripts/validate_prototype.py \
    --html prototypes/639911-退款审批详情.html \
    --vue .tmp/DetailInfo_index.vue \
    --changes "新增还车时间,退款时间,退款后订单实收,租期,车型"

  # 从文件读取变更清单
  python3 scripts/validate_prototype.py \
    --html prototypes/xxx.html \
    --vue .tmp/xxx.vue \
    --changes-file .tmp/change_analysis.md

输出：
  - 字段完整性（缺失/多余/顺序）
  - 已删除字段残留检查
  - 自定义 CSS 检查
  - 总结（error / warning 数量）

退出码：
  - 0: 无 error（可能有 warning）
  - 1: 有 error，需要修复
"""

import argparse
import re
import sys
from html.parser import HTMLParser


class FieldExtractor(HTMLParser):
    """从 HTML 中提取 Element Plus 组件的字段标签。"""

    def __init__(self):
        super().__init__()
        self.fields = []  # [(标签, 组件类型, 行号), ...]
        self._current_tag = None
        self._current_attrs = {}
        self._tag_stack = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        self._tag_stack.append((tag, attrs_dict))

        # Element Plus 字段组件
        if tag in ("el-form-item", "el-descriptions-item", "el-table-column"):
            label = attrs_dict.get("label", "")
            prop = attrs_dict.get("prop", "")
            self.fields.append((label or prop, tag, self.getpos()[0]))

    def handle_endtag(self, tag):
        if self._tag_stack:
            self._tag_stack.pop()


def extract_fields_from_html(html_content: str) -> list:
    """从 HTML 中提取所有 Element Plus 字段。"""
    parser = FieldExtractor()
    parser.feed(html_content)
    return [(label, comp, line) for label, comp, line in parser.fields if label]


def extract_fields_from_vue(vue_content: str) -> list:
    """从 Vue SFC 的 <template> 部分提取字段。"""
    template_match = re.search(
        r"<template>(.*?)</template>", vue_content, re.DOTALL
    )
    if not template_match:
        return []

    template = template_match.group(1)
    return extract_fields_from_html(template)


def extract_css_classes(html_content: str) -> set:
    """从 <style> 标签中提取自定义 CSS 类名（排除 Tailwind 工具类）。"""
    classes = set()
    for match in re.finditer(r"<style[^>]*>(.*?)</style>", html_content, re.DOTALL):
        style_content = match.group(1)
        for cls_match in re.finditer(r"\.([a-zA-Z_-][\w-]*)", style_content):
            cls = cls_match.group(1)
            # 排除 Tailwind 生成的类和常见工具类前缀
            if not cls.startswith(("tw-", "el-")):
                classes.add(cls)
    return classes


def extract_css_classes_from_vue(vue_content: str) -> set:
    """从 Vue SFC 的 <style> 部分提取 CSS 类名。"""
    classes = set()
    for match in re.finditer(r"<style[^>]*>(.*?)</style>", vue_content, re.DOTALL):
        style_content = match.group(1)
        for cls_match in re.finditer(r"\.([a-zA-Z_-][\w-]*)", style_content):
            cls = cls_match.group(1)
            if not cls.startswith(("tw-", "el-")):
                classes.add(cls)
    return classes


def compare_fields(html_fields, vue_fields, deleted_fields=None):
    """
    比对 HTML 和 Vue 的字段列表。
    返回 (errors, warnings) 元组。
    """
    html_labels = [f[0] for f in html_fields]
    vue_labels = [f[0] for f in vue_fields]

    errors = []
    warnings = []

    # 1. 字段完整性：Vue 有但 HTML 没有
    html_label_set = set(html_labels)
    vue_label_set = set(vue_labels)

    for label in vue_labels:
        if label not in html_label_set:
            if deleted_fields and label in deleted_fields:
                continue  # PRD 要求删除的字段
            errors.append(f"[字段缺失] Vue 源码有字段「{label}」，但 HTML 原型中没有")

    # 2. 多余字段：HTML 有但 Vue 没有
    for label, comp, line in html_fields:
        if label not in vue_label_set:
            warnings.append(
                f"[新增字段] HTML 第 {line} 行有「{label}」（{comp}），Vue 源码中没有"
            )

    # 3. 已删除字段残留
    if deleted_fields:
        for df in deleted_fields:
            if df in html_label_set:
                errors.append(f"[残留字段] PRD 要求删除「{df}」，但 HTML 中仍然存在")

    # 4. 字段顺序检查（只检查共有字段）
    common_fields = [l for l in vue_labels if l in html_label_set]
    html_order = [l for l in html_labels if l in set(common_fields)]
    vue_order = [l for l in vue_labels if l in set(common_fields)]

    if html_order != vue_order:
        # 找出第一个不一致的位置
        for i, (h, v) in enumerate(zip(html_order, vue_order)):
            if h != v:
                warnings.append(
                    f"[顺序差异] 第 {i+1} 个共有字段不一致：Vue「{v}」vs HTML「{h}」"
                )
                break

    return errors, warnings


def compare_css(html_content: str, vue_content: str):
    """比对 CSS 类名。"""
    html_classes = extract_css_classes(html_content)
    vue_classes = extract_css_classes_from_vue(vue_content)

    warnings = []
    custom_classes = html_classes - vue_classes
    if custom_classes:
        for cls in sorted(custom_classes):
            warnings.append(f"[自定义CSS] HTML 有自定义类 .{cls}，Vue 源码中不存在")

    return warnings


def validate(html_path: str, vue_path: str, changes: list = None) -> dict:
    """
    执行完整验证。
    返回 {"errors": [...], "warnings": [...]}
    """
    # 读取文件
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    with open(vue_path, "r", encoding="utf-8") as f:
        vue_content = f.read()

    # 提取字段
    html_fields = extract_fields_from_html(html_content)
    vue_fields = extract_fields_from_vue(vue_content)

    # 解析删除字段（从 changes 列表中识别 "删除XXX" 格式的变更）
    deleted_fields = []
    if changes:
        for c in changes:
            if c.startswith("删除") or c.startswith("移除"):
                deleted_fields.append(c[2:].strip())

    # 比对
    field_errors, field_warnings = compare_fields(
        html_fields, vue_fields, deleted_fields
    )
    css_warnings = compare_css(html_content, vue_content)

    all_errors = field_errors
    all_warnings = field_warnings + css_warnings

    return {
        "errors": all_errors,
        "warnings": all_warnings,
        "html_field_count": len(html_fields),
        "vue_field_count": len(vue_fields),
    }


def main():
    parser = argparse.ArgumentParser(
        description="HTML 原型 vs Vue 源码一致性验证",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--html", type=str, required=True, help="HTML 原型文件路径"
    )
    parser.add_argument(
        "--vue", type=str, required=True, help="Vue 源码文件路径"
    )
    parser.add_argument(
        "--changes",
        type=str,
        help="PRD 变更点列表（逗号分隔，如：新增还车时间,删除车型ID）",
    )
    parser.add_argument(
        "--changes-file",
        type=str,
        help="PRD 变更清单文件路径（每行一个变更点）",
    )

    args = parser.parse_args()

    # 解析变更清单
    changes = []
    if args.changes:
        changes = [c.strip() for c in args.changes.split(",") if c.strip()]
    elif args.changes_file:
        with open(args.changes_file, "r", encoding="utf-8") as f:
            changes = [
                line.strip() for line in f.readlines() if line.strip()
            ]

    # 验证
    print(f"验证 HTML 原型: {args.html}")
    print(f"对照 Vue 源码:  {args.vue}")
    if changes:
        print(f"PRD 变更点:   {len(changes)} 个")
    print("-" * 60)

    result = validate(args.html, args.vue, changes)

    # 输出结果
    if result["errors"]:
        print(f"\n❌ 错误（{len(result['errors'])} 个）：")
        for e in result["errors"]:
            print(f"  {e}")

    if result["warnings"]:
        print(f"\n⚠️  警告（{len(result['warnings'])} 个）：")
        for w in result["warnings"]:
            print(f"  {w}")

    # 汇总
    print("\n" + "=" * 60)
    error_count = len(result["errors"])
    warning_count = len(result["warnings"])
    print(
        f"验证完成：{error_count} 个错误，{warning_count} 个警告"
    )
    print(
        f"  HTML 字段数：{result['html_field_count']}  |  Vue 字段数：{result['vue_field_count']}"
    )

    if error_count > 0:
        print("需要修复后重新验证")
        sys.exit(1)
    else:
        print("✅ 验证通过")
        sys.exit(0)


if __name__ == "__main__":
    main()
