#!/usr/bin/env python3
"""
Lolicon色图插件测试脚本
测试API调用和基本功能
"""

import asyncio
import sys
from pathlib import Path

# 添加MaiBot路径到系统路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# 导入插件模块
from plugins.lolicon_setu_plugin.plugin import LoliconAPI


async def test_api_connection():
    """测试API连接"""
    print("=" * 60)
    print("测试1: API连接测试")
    print("=" * 60)

    api = LoliconAPI(timeout=30)

    # 测试基础API
    print("\n📡 测试基础API...")
    try:
        result = await api.fetch_setu(num=1)

        if not result.get("error"):
            print("✅ API 连接成功！")
            data = result.get("data", [])
            if data:
                item = data[0]
                print(f"\n📊 获取到的图片信息：")
                print(f"   标题: {item.get('title', 'N/A')}")
                print(f"   作者: {item.get('author', 'N/A')}")
                print(f"   PID: {item.get('pid', 'N/A')}")
                print(f"   尺寸: {item.get('width', 0)}x{item.get('height', 0)}")
                print(f"   AI类型: {item.get('aiType', 0)}")

                tags = item.get('tags', [])
                if tags:
                    print(f"   标签: {', '.join(tags[:3])}")
            else:
                print("⚠️  API响应成功但无数据")
        else:
            print(f"❌ API 调用失败: {result.get('error', '未知错误')}")

    except Exception as e:
        print(f"❌ API 测试异常: {str(e)}")
        import traceback
        traceback.print_exc()


async def test_tag_search():
    """测试标签搜索"""
    print("\n" + "=" * 60)
    print("测试2: 标签搜索测试")
    print("=" * 60)

    api = LoliconAPI(timeout=30)

    # 测试简单标签搜索
    print("\n🏷️ 测试简单标签搜索...")
    try:
        result = await api.fetch_setu(num=1, tag=[["萝莉"]])
        if not result.get("error") and result.get("data"):
            print("✅ 标签搜索成功")
            item = result["data"][0]
            print(f"   标题: {item['title']}")
            print(f"   标签: {', '.join(item['tags'][:5])}")
        else:
            print("⚠️  标签搜索返回空结果（可能是正常的）")
    except Exception as e:
        print(f"❌ 标签搜索测试失败: {str(e)}")

    # 测试AND搜索
    print("\n🔗 测试AND搜索...")
    try:
        result = await api.fetch_setu(num=1, tag=[["白丝"], ["JK"]])
        if not result.get("error") and result.get("data"):
            print("✅ AND搜索成功")
        else:
            print("⚠️  AND搜索返回空结果")
    except Exception as e:
        print(f"❌ AND搜索测试失败: {str(e)}")


async def test_keyword_search():
    """测试关键词搜索"""
    print("\n" + "=" * 60)
    print("测试3: 关键词搜索测试")
    print("=" * 60)

    api = LoliconAPI(timeout=30)

    print("\n🔍 测试关键词搜索...")
    try:
        result = await api.fetch_setu(num=1, keyword="原神")
        if not result.get("error") and result.get("data"):
            print("✅ 关键词搜索成功")
            item = result["data"][0]
            print(f"   标题: {item['title']}")
            print(f"   作者: {item['author']}")
        else:
            print("⚠️  关键词搜索返回空结果")
    except Exception as e:
        print(f"❌ 关键词搜索测试失败: {str(e)}")


async def test_filters():
    """测试筛选功能"""
    print("\n" + "=" * 60)
    print("测试4: 筛选功能测试")
    print("=" * 60)

    api = LoliconAPI(timeout=30)

    # 测试排除AI
    print("\n🚫 测试排除AI...")
    try:
        result = await api.fetch_setu(num=1, exclude_ai=True)
        if not result.get("error") and result.get("data"):
            print("✅ 排除AI筛选成功")
            item = result["data"][0]
            print(f"   AI类型: {item['aiType']}")
        else:
            print("⚠️  排除AI筛选返回空结果")
    except Exception as e:
        print(f"❌ 排除AI测试失败: {str(e)}")

    # 测试长宽比
    print("\n📐 测试长宽比筛选...")
    try:
        result = await api.fetch_setu(num=1, aspect_ratio="gt1")  # 横图
        if not result.get("error") and result.get("data"):
            print("✅ 长宽比筛选成功")
            item = result["data"][0]
            ratio = item['width'] / item['height']
            print(f"   尺寸: {item['width']}x{item['height']}")
            print(f"   长宽比: {ratio:.3f}")
        else:
            print("⚠️  长宽比筛选返回空结果")
    except Exception as e:
        print(f"❌ 长宽比测试失败: {str(e)}")


async def run_all_tests():
    """运行所有测试"""
    print("\n" + "🧪" * 30)
    print("🚀 开始测试Lolicon色图插件")
    print("🧪" * 30 + "\n")

    try:
        # 测试1: API连接
        await test_api_connection()

        # 测试2: 标签搜索
        await test_tag_search()

        # 测试3: 关键词搜索
        await test_keyword_search()

        # 测试4: 筛选功能
        await test_filters()

        print("\n" + "=" * 60)
        print("✅ 所有测试完成！")
        print("=" * 60)

        print("\n📝 测试总结:")
        print("   - 如果所有测试都通过，插件可以正常使用")
        print("   - 如果API调用失败，请检查网络连接")
        print("   - 如果返回空数据，可能是API暂时无可用图片")
        print("\n💡 下一步:")
        print("   1. 在MaiBot中使用 /setu 命令测试")
        print("   2. 尝试不同的搜索条件")
        print("   3. 检查日志文件查看详细信息")

    except Exception as e:
        print(f"\n❌ 测试过程中发生错误: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # 运行测试
    asyncio.run(run_all_tests())
