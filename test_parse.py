#!/usr/bin/env python3
"""
测试新的命令解析格式
"""

import re
from typing import Dict, Any

def parse_args(args_str: str) -> Dict[str, Any]:
    """解析命令参数"""
    params = {
        "num": 1,
        "r18": 0,
        "exclude_ai": False,
        "keyword": None,
        "tag": [],
        "uid": None,
        "aspect_ratio": None,
    }

    if not args_str:
        return params

    args = args_str.split()

    # 保留的关键词（不会被识别为搜索关键词）
    reserved_keywords = {
        "r18", "noai", "no_ai", "排除ai",
        "horizontal", "横图", "vertical", "竖图", "square", "方图"
    }

    # 解析参数
    for arg in args:
        arg_lower = arg.lower()

        # 数量
        if arg_lower.isdigit():
            params["num"] = min(max(1, int(arg_lower)), 20)
        # R18
        elif arg_lower == "r18":
            params["r18"] = 1
        # 排除AI
        elif arg_lower in ["noai", "no_ai", "排除ai"]:
            params["exclude_ai"] = True
        # 长宽比快捷方式
        elif arg_lower in ["horizontal", "横图"]:
            params["aspect_ratio"] = "gt1"
        elif arg_lower in ["vertical", "竖图"]:
            params["aspect_ratio"] = "lt1"
        elif arg_lower in ["square", "方图"]:
            params["aspect_ratio"] = "eq1"
        # 标签搜索 - 新格式 #标签
        elif arg.startswith("#"):
            tag_str = arg[1:]  # 去掉#号
            # 支持逗号分隔的OR搜索
            tags = [t.strip() for t in tag_str.split(",")]
            params["tag"].append(tags)
        # 标签搜索 - 旧格式 tag:标签（兼容）
        elif arg.startswith("tag:"):
            tag_str = arg.split(":", 1)[1]
            tags = [t.strip() for t in tag_str.split(",")]
            params["tag"].append(tags)
        # 关键词搜索 - 旧格式 keyword:关键词（兼容）
        elif arg.startswith("keyword:") or arg.startswith("kw:"):
            params["keyword"] = arg.split(":", 1)[1]
        # UID搜索
        elif arg.startswith("uid:"):
            try:
                uid = int(arg.split(":", 1)[1])
                params["uid"] = [uid]
            except ValueError:
                print(f"⚠️ 无效的UID: {arg}")
        # 长宽比表达式
        elif re.match(r"((gt|gte|lt|lte|eq)[\d.]+){1,2}", arg_lower):
            params["aspect_ratio"] = arg_lower
        # 关键词搜索 - 新格式（纯文本）
        elif arg_lower not in reserved_keywords:
            # 如果已有关键词，添加空格连接
            if params["keyword"]:
                params["keyword"] += " " + arg
            else:
                params["keyword"] = arg

    return params


def test_parse():
    """测试命令解析"""
    test_cases = [
        # 基础测试
        ("", "空命令"),
        ("3", "数量3张"),
        ("5 横图", "5张横图"),

        # 新格式 - 标签搜索
        ("#萝莉", "标签搜索：萝莉"),
        ("#白丝,黑丝", "OR搜索：白丝或黑丝"),
        ("#萝莉 #白丝", "AND搜索：萝莉且白丝"),
        ("3 #风景 #唯美", "3张风景且唯美"),

        # 新格式 - 关键词搜索
        ("原神", "关键词：原神"),
        ("初音未来", "关键词：初音未来"),
        ("原神 5", "5张原神"),

        # 组合使用
        ("3 #萝莉,少女 横图", "3张萝莉或少女的横图"),
        ("#白丝 #JK noai", "白丝且JK，排除AI"),
        ("原神 5 竖图", "5张原神竖图"),
        ("#风景 #唯美 gt1.5 noai", "风景且唯美，长宽比>1.5，非AI"),

        # 旧格式兼容
        ("keyword:原神", "旧格式：关键词原神"),
        ("tag:萝莉", "旧格式：标签萝莉"),
        ("kw:风景", "旧格式：关键词风景（缩写）"),

        # UID和其他
        ("uid:12345", "作者UID 12345"),
        ("r18", "R18内容"),
        ("5 noai r18", "5张非AI的R18"),
    ]

    print("=" * 70)
    print("命令解析测试")
    print("=" * 70)

    for args_str, description in test_cases:
        print(f"\n📝 测试: {description}")
        print(f"   命令: /setu {args_str}" if args_str else "   命令: /setu")

        result = parse_args(args_str)

        # 显示解析结果
        output = []
        if result["num"] != 1:
            output.append(f"数量={result['num']}")
        if result["keyword"]:
            output.append(f"关键词=\"{result['keyword']}\"")
        if result["tag"]:
            tag_str = " AND ".join([f"({' OR '.join(t)})" for t in result['tag']])
            output.append(f"标签={tag_str}")
        if result["r18"]:
            output.append("R18=是")
        if result["exclude_ai"]:
            output.append("排除AI=是")
        if result["aspect_ratio"]:
            output.append(f"长宽比={result['aspect_ratio']}")
        if result["uid"]:
            output.append(f"UID={result['uid'][0]}")

        if output:
            print(f"   ✅ 解析: {', '.join(output)}")
        else:
            print(f"   ✅ 解析: 随机获取1张")

    print("\n" + "=" * 70)
    print("✅ 所有测试完成！")
    print("=" * 70)


if __name__ == "__main__":
    test_parse()
