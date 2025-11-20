# 自定义 AI API 配置指南

本项目现已支持使用自定义 AI API（符合 OpenAI API v1 格式）。您可以使用 OpenAI 官方 API，或任何兼容 OpenAI API v1 格式的服务。

## 支持的 AI 提供商

### 1. Google Gemini (默认)

```env
AI_PROVIDER=gemini
GEMINI_API_KEY=your_gemini_api_key_here
```

### 2. OpenAI 官方 API

```env
AI_PROVIDER=openai
CUSTOM_AI_API_URL=https://api.openai.com/v1
CUSTOM_AI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
CUSTOM_AI_MODEL=gpt-4
CUSTOM_AI_VERIFICATION_MODEL=gpt-3.5-turbo  # 可选，用于验证问题生成
```

### 3. 自定义 AI API（任何符合 OpenAI API v1 格式的服务）

```env
AI_PROVIDER=custom
CUSTOM_AI_API_URL=https://your-api-endpoint.com/v1
CUSTOM_AI_API_KEY=your_api_key_here
CUSTOM_AI_MODEL=your-model-name
CUSTOM_AI_VERIFICATION_MODEL=your-verification-model  # 可选
```

## 兼容的第三方服务示例

以下第三方服务通常支持 OpenAI API v1 格式：

### Azure OpenAI
```env
AI_PROVIDER=custom
CUSTOM_AI_API_URL=https://your-resource.openai.azure.com/openai/deployments
CUSTOM_AI_API_KEY=your_azure_api_key
CUSTOM_AI_MODEL=your-deployment-name
```

### 国产大模型（如讯飞星火、通义千问、文心一言等）
许多国产大模型提供商提供 OpenAI 兼容的 API 接口，具体配置请参考各服务商文档。

```env
AI_PROVIDER=custom
CUSTOM_AI_API_URL=https://provider-api-endpoint.com/v1
CUSTOM_AI_API_KEY=your_api_key
CUSTOM_AI_MODEL=model-name
```

### 本地部署的模型（如 Ollama、vLLM 等）
如果您有本地部署的大模型服务，且支持 OpenAI API 格式：

```env
AI_PROVIDER=custom
CUSTOM_AI_API_URL=http://localhost:11434/v1  # Ollama 示例
CUSTOM_AI_API_KEY=not-needed  # 本地服务可能不需要密钥
CUSTOM_AI_MODEL=llama3
```

## 配置说明

### 必需配置项

- `AI_PROVIDER`: 选择 AI 提供商（`gemini`、`openai` 或 `custom`）
- `CUSTOM_AI_API_URL`: API 的基础 URL（当使用 openai 或 custom 时）
- `CUSTOM_AI_API_KEY`: API 密钥（当使用 openai 或 custom 时）
- `CUSTOM_AI_MODEL`: 主要模型名称（用于内容审查）

### 可选配置项

- `CUSTOM_AI_VERIFICATION_MODEL`: 用于生成验证问题的模型，如不设置则使用 `CUSTOM_AI_MODEL`
- `ENABLE_AI_FILTER`: 是否启用 AI 过滤（默认 true）
- `AI_CONFIDENCE_THRESHOLD`: AI 置信度阈值（默认 70）

## 功能说明

自定义 AI API 将用于以下功能：

1. **内容审查**: 分析用户发送的文本和图片内容，判断是否为垃圾信息或不当内容
2. **人机验证**: 生成多样化的验证问题，用于新用户验证
3. **解封验证**: 为被封禁用户生成解封验证问题

## 测试配置

配置完成后，您可以使用测试脚本验证配置是否正确：

```bash
python test_ai_integration.py
```

该脚本会：
- 显示当前的 AI 配置
- 测试生成验证问题
- 测试生成解封问题

## 注意事项

1. **API 兼容性**: 确保您的 API 服务完全兼容 OpenAI API v1 格式
2. **模型能力**: 建议使用支持视觉理解的模型（如 GPT-4 Vision）以充分利用图片内容审查功能
3. **成本控制**: 使用付费 API 时请注意成本控制，可以通过 `ENABLE_AI_FILTER` 关闭 AI 功能
4. **回退机制**: 如果 AI 服务不可用，系统会自动使用本地预设的验证问题库
5. **依赖安装**: 使用 OpenAI 兼容 API 时，请确保已安装 `openai` 库（已包含在 requirements.txt 中）

## 故障排查

### 问题：无法连接到 API
- 检查 `CUSTOM_AI_API_URL` 是否正确
- 确认网络连接正常
- 检查防火墙和代理设置

### 问题：认证失败
- 验证 `CUSTOM_AI_API_KEY` 是否正确
- 检查 API 密钥是否有足够的权限

### 问题：模型不存在
- 确认 `CUSTOM_AI_MODEL` 名称与 API 服务提供的模型名称一致
- 检查您的账户是否有权访问该模型

### 问题：API 响应格式错误
- 确保 API 服务完全兼容 OpenAI API v1 格式
- 查看日志输出以获取详细错误信息

## 更多帮助

如有其他问题，请参考：
- [OpenAI API 文档](https://platform.openai.com/docs/api-reference)
- 项目 GitHub Issues
- 联系项目维护者
