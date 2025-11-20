#!/usr/bin/env python3
"""
独立的自定义AI API服务器启动脚本
基于Gemini提供OpenAI兼容的API接口

使用方法:
1. 直接运行: python custom_ai_api_server.py
2. 或通过uvicorn: uvicorn services.custom_ai_api:app --host 0.0.0.0 --port 8000

环境变量配置:
- GEMINI_API_KEY: Gemini API密钥（必需）
- CUSTOM_AI_API_PORT: API服务器端口（默认8000）
- CUSTOM_AI_API_HOST: API服务器主机（默认0.0.0.0）
- CUSTOM_AI_API_KEY: 可选的API密钥验证
"""

import os
import sys
import uvicorn
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def main():
    # 检查必需的环境变量
    gemini_api_key = os.getenv('GEMINI_API_KEY')
    if not gemini_api_key:
        print("错误: GEMINI_API_KEY 环境变量未设置")
        print("请设置您的Gemini API密钥:")
        print("export GEMINI_API_KEY=your_gemini_api_key_here")
        sys.exit(1)
    
    # 获取配置
    host = os.getenv('CUSTOM_AI_API_HOST', '0.0.0.0')
    port = int(os.getenv('CUSTOM_AI_API_PORT', '8000'))
    api_key = os.getenv('CUSTOM_AI_API_KEY')
    
    print("=" * 60)
    print("🤖 自定义AI API服务器启动中...")
    print("=" * 60)
    print(f"📍 服务地址: http://{host}:{port}")
    print(f"📚 API文档: http://{host}:{port}/docs")
    print(f"🔑 API密钥验证: {'已启用' if api_key else '已禁用'}")
    print(f"🧠 后端模型: Google Gemini")
    print("=" * 60)
    
    if api_key:
        print(f"⚠️  使用API密钥: {api_key[:8]}...{api_key[-8:]}")
        print("   请求时请在Header中添加: Authorization: Bearer YOUR_API_KEY")
        print()
    
    print("🚀 启动FastAPI服务器...")
    print("📝 可用端点:")
    print("   GET  /v1/models              - 列出可用模型")
    print("   GET  /v1/models/{{model}}     - 获取模型信息")
    print("   POST /v1/chat/completions    - 聊天完成（支持流式）")
    print("   GET  /health                  - 健康检查")
    print("   GET  /                        - 根信息")
    print()
    print("💡 使用示例:")
    print("curl -X POST http://localhost:8000/v1/chat/completions \\")
    print("  -H 'Content-Type: application/json' \\")
    if api_key:
        print("  -H 'Authorization: Bearer YOUR_API_KEY' \\")
    print("  -d '{")
    print('    "model": "gpt-3.5-turbo",')
    print('    "messages": [{"role": "user", "content": "你好！"}]')
    print("  }'")
    print()
    print("按 Ctrl+C 停止服务器")
    print("=" * 60)
    
    try:
        # 启动服务器
        uvicorn.run(
            "services.custom_ai_api:app",
            host=host,
            port=port,
            reload=False,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()