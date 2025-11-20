#!/bin/bash
# 自定义AI API快速启动示例脚本

echo "🚀 自定义AI API快速启动示例"
echo "=================================="

# 检查是否存在.env文件
if [ ! -f .env ]; then
    echo "❌ 错误: 未找到.env文件"
    echo "请先复制.env.example为.env并配置相关参数"
    exit 1
fi

# 检查GEMINI_API_KEY是否设置
if ! grep -q "GEMINI_API_KEY=" .env || grep -q "GEMINI_API_KEY=$" .env; then
    echo "❌ 错误: GEMINI_API_KEY未设置"
    echo "请在.env文件中设置您的Gemini API密钥"
    exit 1
fi

echo "✅ 环境检查通过"

# 启动选项
echo "请选择启动方式："
echo "1. 独立启动自定义AI API服务器"
echo "2. 启动完整的Telegram Bot（包含自定义AI API）"
echo "3. 使用Docker Compose启动自定义AI API"
echo "4. 测试API功能"

read -p "请输入选项 (1-4): " choice

case $choice in
    1)
        echo "🔧 启动独立API服务器..."
        python custom_ai_api_server.py
        ;;
    2)
        echo "🤖 启动完整Telegram Bot..."
        python bot.py
        ;;
    3)
        echo "🐳 使用Docker Compose启动..."
        docker-compose -f docker-compose.custom-ai-api.yml up --build
        ;;
    4)
        echo "🧪 运行API测试..."
        python test_custom_ai_api.py
        ;;
    *)
        echo "❌ 无效选项"
        exit 1
        ;;
esac