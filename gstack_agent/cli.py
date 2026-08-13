#!/usr/bin/env python3
"""gstack-agent CLI 入口"""
import argparse
import sys

from .office_hours import run_office_hours
from .ceo_review import run_ceo_review
from .investigate import run_investigate


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="gstack-agent",
        description="YC CEO 思考方法 AI 助手 - Garry Tan gstack 框架落地",
    )
    sub = parser.add_subparsers(dest="command", help="可用命令")

    # analyze - 通用分析
    p_analyze = sub.add_parser("analyze", help="全面分析（追问 + 审核 + 调查）")
    p_analyze.add_argument("task", help="任务描述")

    # office-hours
    p_oh = sub.add_parser("office-hours", help="Office-Hours 6 问法")
    p_oh.add_argument("idea", help="产品想法/方案描述")
    p_oh.add_argument("--auto", action="store_true", help="自动模式，跳过追问直接输出分析")

    # ceo-review
    p_cr = sub.add_parser("ceo-review", help="CEO Review 9 条指令审核")
    p_cr.add_argument("plan", help="方案文档或描述")
    p_cr.add_argument("--strict", action="store_true", help="严格模式，必须 100% 符合")

    # investigate
    p_inv = sub.add_parser("investigate", help="Investigate 4 阶段故障排查")
    p_inv.add_argument("symptom", help="症状描述")
    p_inv.add_argument("--interactive", action="store_true", help="交互式排查")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    if args.command == "analyze":
        run_office_hours(args.task, auto=True)
        print("\n" + "=" * 60)
        run_ceo_review(args.task)
        print("\n" + "=" * 60)
        run_investigate(args.task)
        return 0

    if args.command == "office-hours":
        run_office_hours(args.idea, auto=args.auto)
        return 0

    if args.command == "ceo-review":
        run_ceo_review(args.plan, strict=args.strict)
        return 0

    if args.command == "investigate":
        run_investigate(args.symptom, interactive=args.interactive)
        return 0

    return 1