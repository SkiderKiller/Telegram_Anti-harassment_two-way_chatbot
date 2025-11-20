#!/usr/bin/env python3
"""
测试AI集成的简单脚本
用于验证自定义AI API集成是否正常工作
"""

import asyncio
from dotenv import load_dotenv

load_dotenv()


async def test_ai_service():
    print("=" * 50)
    print("测试 AI 服务集成")
    print("=" * 50)

    from config import config

    print(f"\n当前 AI 提供商: {config.AI_PROVIDER}")

    if config.AI_PROVIDER in ["openai", "custom"]:
        print(f"API URL: {config.CUSTOM_AI_API_URL}")
        print(f"API Key: {'已设置' if config.CUSTOM_AI_API_KEY else '未设置'}")
        print(f"模型: {config.CUSTOM_AI_MODEL}")
    elif config.AI_PROVIDER == "gemini":
        print(f"Gemini API Key: {'已设置' if config.GEMINI_API_KEY else '未设置'}")

    print("\n正在导入 AI 服务...")
    from services.gemini_service import gemini_service

    print(f"服务类型: {type(gemini_service).__name__}")

    if not config.ENABLE_AI_FILTER:
        print("\n注意: AI 过滤功能已禁用")
        return

    print("\n测试 1: 生成验证问题")
    try:
        question_data = await gemini_service.generate_verification_challenge()
        print(f"问题: {question_data['question']}")
        print(f"正确答案: {question_data['correct_answer']}")
        print(f"选项: {question_data['options']}")
        print("✓ 验证问题生成成功")
    except Exception as e:
        print(f"✗ 生成验证问题失败: {e}")

    print("\n测试 2: 生成解封问题")
    try:
        unblock_data = await gemini_service.generate_unblock_question()
        print(f"问题: {unblock_data['question']}")
        print(f"正确答案: {unblock_data['correct_answer']}")
        print(f"选项: {unblock_data['options']}")
        print("✓ 解封问题生成成功")
    except Exception as e:
        print(f"✗ 生成解封问题失败: {e}")

    print("\n" + "=" * 50)
    print("测试完成")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(test_ai_service())
