# 自定义AI API服务

基于Google Gemini API的OpenAI兼容接口服务，提供标准的OpenAI API调用格式。

## 🚀 功能特性

- ✅ **OpenAI API兼容**: 完全兼容OpenAI API v1格式
- ✅ **多模型支持**: 支持gpt-3.5-turbo、gpt-4、gpt-4o等模型映射
- ✅ **流式响应**: 支持Server-Sent Events流式输出
- ✅ **API密钥验证**: 可选的API密钥认证
- ✅ **自动文档**: 提供Swagger UI交互式文档
- ✅ **错误处理**: 完善的错误响应机制

## 📋 环境要求

- Python 3.8+
- Google Gemini API密钥
- 依赖包：fastapi, uvicorn, google-genai, pydantic

## ⚙️ 配置说明

在`.env`文件中添加以下配置：

```env
# Gemini API配置（必需）
GEMINI_API_KEY=your_gemini_api_key_here

# 自定义AI API配置
ENABLE_CUSTOM_AI_API=true              # 启用自定义AI API
CUSTOM_AI_API_PORT=8000                # API服务器端口
CUSTOM_AI_API_HOST=0.0.0.0             # API服务器主机
CUSTOM_AI_API_KEY=your_api_key_here    # 可选的API密钥验证
```

## 🛠️ 安装和启动

### 方法1: 随Telegram Bot一起启动

1. 确保已安装所有依赖：
```bash
pip install -r requirements.txt
```

2. 在`.env`文件中设置`ENABLE_CUSTOM_AI_API=true`

3. 启动Telegram Bot，自定义AI API会自动启动：
```bash
python bot.py
```

### 方法2: 独立启动API服务器

1. 确保已安装所有依赖：
```bash
pip install -r requirements.txt
```

2. 设置环境变量：
```bash
export GEMINI_API_KEY=your_gemini_api_key_here
export CUSTOM_AI_API_PORT=8000
```

3. 运行启动脚本：
```bash
python custom_ai_api_server.py
```

或使用uvicorn直接启动：
```bash
uvicorn services.custom_ai_api:app --host 0.0.0.0 --port 8000
```

## 📚 API文档

启动服务后，访问以下地址：

- **API交互文档**: http://localhost:8000/docs
- **API原始文档**: http://localhost:8000/redoc
- **健康检查**: http://localhost:8000/health

## 🔌 API使用示例

### 1. 聊天完成（非流式）

```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -d '{
    "model": "gpt-3.5-turbo",
    "messages": [
      {"role": "user", "content": "你好！请介绍一下自己。"}
    ],
    "temperature": 0.7,
    "max_tokens": 1000
  }'
```

### 2. 聊天完成（流式）

```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -d '{
    "model": "gpt-4",
    "messages": [
      {"role": "user", "content": "请写一首关于春天的诗"}
    ],
    "stream": true
  }'
```

### 3. 获取可用模型

```bash
curl -X GET http://localhost:8000/v1/models \
  -H 'Authorization: Bearer YOUR_API_KEY'
```

### 4. Python客户端示例

```python
import requests

# API配置
API_BASE = "http://localhost:8000/v1"
API_KEY = "your_api_key_here"  # 如果启用了API密钥验证

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

# 发送聊天请求
response = requests.post(
    f"{API_BASE}/chat/completions",
    headers=headers,
    json={
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": "你好！"}
        ]
    }
)

result = response.json()
print(result["choices"][0]["message"]["content"])
```

### 5. OpenAI Python SDK兼容

```python
from openai import OpenAI

# 配置客户端
client = OpenAI(
    api_key="your_api_key_here",  # 如果启用了API密钥验证
    base_url="http://localhost:8000/v1"
)

# 使用标准OpenAI API
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "你好！请介绍一下自己。"}
    ]
)

print(response.choices[0].message.content)
```

## 🎯 模型映射

| OpenAI模型名称 | Gemini后端模型 | 说明 |
|---------------|---------------|------|
| gpt-3.5-turbo | gemini-2.0-flash-exp | 标准聊天模型 |
| gpt-4 | gemini-2.0-flash-exp | 高级聊天模型 |
| gpt-4-turbo | gemini-2.0-flash-exp | 快速高级模型 |
| gpt-4o | gemini-2.0-flash-exp | 最新的多模态模型 |
| text-davinci-003 | gemini-2.0-flash-exp | 文本生成模型 |
| gemini-pro | gemini-2.0-flash-exp | Gemini原生模型 |

## 📝 支持的参数

### 请求参数

- `model`: 模型名称（必填）
- `messages`: 消息列表（必填）
- `temperature`: 温度参数（0-2，默认0.7）
- `max_tokens`: 最大token数（可选）
- `stream`: 是否流式响应（默认false）
- `top_p`: 核采样参数（默认1.0）
- `frequency_penalty`: 频率惩罚（默认0.0）
- `presence_penalty`: 存在惩罚（默认0.0）

### 响应格式

完全兼容OpenAI API响应格式，包括：
- `id`: 响应ID
- `object`: 对象类型
- `created`: 创建时间戳
- `model`: 使用的模型
- `choices`: 选择列表
- `usage`: Token使用统计

## 🔒 安全配置

### API密钥验证

1. 在`.env`文件中设置`CUSTOM_AI_API_KEY=your_secure_api_key`
2. 客户端请求时需要在Header中包含：
   ```
   Authorization: Bearer your_secure_api_key
   ```

### 网络安全

- 默认监听`0.0.0.0`，生产环境建议配置防火墙
- 支持反向代理（Nginx、Caddy等）
- 建议在生产环境中使用HTTPS

## 🐛 故障排除

### 常见问题

1. **API密钥错误**
   - 检查`GEMINI_API_KEY`是否正确设置
   - 确认Gemini API配额充足

2. **端口占用**
   - 修改`CUSTOM_AI_API_PORT`为其他端口
   - 检查防火墙设置

3. **依赖缺失**
   ```bash
   pip install -r requirements.txt
   ```

4. **模型不可用**
   - 检查Gemini API服务状态
   - 确认模型名称映射正确

### 日志查看

服务器启动后会显示详细日志，包括：
- 请求信息
- 响应状态
- 错误详情
- 性能指标

## 🚀 部署建议

### Docker部署

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "custom_ai_api_server.py"]
```

### 反向代理配置（Nginx）

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 📄 许可证

本项目遵循MIT许可证。详见[LICENSE](LICENSE)文件。

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个项目！

## 📞 支持

如有问题或建议，请通过以下方式联系：
- 创建GitHub Issue
- 发送邮件至项目维护者
- 加入项目讨论群组