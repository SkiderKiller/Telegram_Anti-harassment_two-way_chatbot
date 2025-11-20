#!/usr/bin/env python3
"""
自定义AI API测试脚本
用于验证OpenAI兼容API的功能

使用方法:
python test_custom_ai_api.py
"""

import asyncio
import aiohttp
import json
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# API配置
API_BASE = "http://localhost:8000/v1"
API_KEY = os.getenv('CUSTOM_AI_API_KEY', '')  # 如果没有设置API密钥，则为空

async def test_health_check():
    """测试健康检查端点"""
    print("🏥 测试健康检查...")
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_BASE.replace('/v1', '')}/health") as response:
            if response.status == 200:
                data = await response.json()
                print(f"✅ 健康检查通过: {data}")
                return True
            else:
                print(f"❌ 健康检查失败: {response.status}")
                return False

async def test_models():
    """测试模型列表端点"""
    print("\n📋 测试模型列表...")
    headers = {"Content-Type": "application/json"}
    if API_KEY:
        headers["Authorization"] = f"Bearer {API_KEY}"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_BASE}/models", headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                models = [model['id'] for model in data['data']]
                print(f"✅ 可用模型: {models}")
                return True
            else:
                print(f"❌ 获取模型列表失败: {response.status}")
                error_text = await response.text()
                print(f"错误信息: {error_text}")
                return False

async def test_chat_completion():
    """测试聊天完成端点"""
    print("\n💬 测试聊天完成...")
    headers = {"Content-Type": "application/json"}
    if API_KEY:
        headers["Authorization"] = f"Bearer {API_KEY}"
    
    request_data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": "你好！请简单介绍一下自己，用一句话回答。"}
        ],
        "temperature": 0.7,
        "max_tokens": 100
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{API_BASE}/chat/completions", 
            headers=headers, 
            json=request_data
        ) as response:
            if response.status == 200:
                data = await response.json()
                message = data['choices'][0]['message']['content']
                usage = data['usage']
                print(f"✅ 聊天响应: {message}")
                print(f"📊 Token使用: {usage}")
                return True
            else:
                print(f"❌ 聊天完成失败: {response.status}")
                error_text = await response.text()
                print(f"错误信息: {error_text}")
                return False

async def test_stream_chat_completion():
    """测试流式聊天完成端点"""
    print("\n🌊 测试流式聊天完成...")
    headers = {"Content-Type": "application/json"}
    if API_KEY:
        headers["Authorization"] = f"Bearer {API_KEY}"
    
    request_data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": "请用3个词形容春天"}
        ],
        "stream": True,
        "temperature": 0.7
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{API_BASE}/chat/completions", 
            headers=headers, 
            json=request_data
        ) as response:
            if response.status == 200:
                content_parts = []
                async for line in response.content:
                    line_str = line.decode('utf-8').strip()
                    if line_str.startswith('data: '):
                        data_str = line_str[6:]  # 移除 'data: ' 前缀
                        if data_str == '[DONE]':
                            break
                        try:
                            data = json.loads(data_str)
                            if 'choices' in data and data['choices']:
                                delta = data['choices'][0].get('delta', {})
                                if 'content' in delta:
                                    content_parts.append(delta['content'])
                                    print(delta['content'], end='', flush=True)
                        except json.JSONDecodeError:
                            continue
                
                full_content = ''.join(content_parts)
                print(f"\n✅ 流式响应完成: {full_content}")
                return True
            else:
                print(f"❌ 流式聊天完成失败: {response.status}")
                error_text = await response.text()
                print(f"错误信息: {error_text}")
                return False

async def test_error_handling():
    """测试错误处理"""
    print("\n⚠️ 测试错误处理...")
    
    # 测试无效模型
    headers = {"Content-Type": "application/json"}
    if API_KEY:
        headers["Authorization"] = f"Bearer {API_KEY}"
    
    request_data = {
        "model": "invalid-model",
        "messages": [
            {"role": "user", "content": "测试"}
        ]
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{API_BASE}/chat/completions", 
            headers=headers, 
            json=request_data
        ) as response:
            if response.status in [400, 500]:
                print("✅ 错误处理正常，无效模型被正确拒绝")
                return True
            else:
                print(f"❌ 错误处理异常: {response.status}")
                return False

async def main():
    """主测试函数"""
    print("🚀 开始测试自定义AI API...")
    print("=" * 50)
    
    # 检查环境变量
    if not os.getenv('GEMINI_API_KEY'):
        print("❌ 错误: GEMINI_API_KEY 环境变量未设置")
        print("请设置您的Gemini API密钥后重试")
        return
    
    # 运行测试
    tests = [
        test_health_check,
        test_models,
        test_chat_completion,
        test_stream_chat_completion,
        test_error_handling
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if await test():
                passed += 1
        except Exception as e:
            print(f"❌ 测试异常: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！自定义AI API工作正常。")
    else:
        print("⚠️ 部分测试失败，请检查配置和服务状态。")
    
    print("\n💡 提示:")
    print("- 如果测试失败，请确保API服务器正在运行")
    print("- 检查环境变量配置是否正确")
    print("- 查看服务器日志获取详细错误信息")

if __name__ == "__main__":
    asyncio.run(main())