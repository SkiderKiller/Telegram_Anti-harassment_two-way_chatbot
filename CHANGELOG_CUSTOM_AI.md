# 自定义 AI API 集成更新日志

## 版本更新说明

### 新增功能

✨ **支持自定义 AI API (OpenAI API v1 格式)**

项目现已支持使用符合 OpenAI API v1 格式的任何 AI 服务，包括：
- OpenAI 官方 API
- Azure OpenAI
- 各种国产大模型（如讯飞星火、通义千问、文心一言等）
- 本地部署的模型（Ollama、vLLM 等）

### 修改的文件

#### 1. `config.py`
- 新增 `AI_PROVIDER` 配置项，支持 `gemini`、`openai`、`custom` 三种选择
- 新增 `CUSTOM_AI_API_URL` 配置项，用于指定自定义 API 的基础 URL
- 新增 `CUSTOM_AI_API_KEY` 配置项，用于指定自定义 API 的密钥
- 新增 `CUSTOM_AI_MODEL` 配置项，用于指定使用的模型
- 新增 `CUSTOM_AI_VERIFICATION_MODEL` 配置项，用于指定验证问题生成模型（可选）

#### 2. `services/gemini_service.py`
- 修改导入方式，使 Gemini 依赖可选（支持只使用自定义 API）
- 新增 `_create_ai_service()` 工厂函数，根据配置自动选择合适的 AI 服务
- 保持完全向后兼容，现有 Gemini 用户无需修改配置

#### 3. `services/openai_service.py` (新增)
- 实现 `OpenAIService` 类，支持 OpenAI API v1 格式
- 实现 `analyze_message()` 方法，用于内容审查（支持文本和图片）
- 实现 `generate_verification_challenge()` 方法，用于生成人机验证问题
- 实现 `generate_unblock_question()` 方法，用于生成解封验证问题
- 包含本地问题库作为回退方案

#### 4. `requirements.txt`
- 新增 `openai>=1.0.0` 依赖

#### 5. `.env.example`
- 更新配置示例，包含所有新增的环境变量
- 添加详细的配置说明和示例

#### 6. `README.md`
- 更新核心特性说明，说明支持多种 AI 提供商
- 更新获取必要信息部分，添加自定义 AI API 的说明
- 新增 AI 提供商配置章节

### 新增文件

#### 1. `AI_API_SETUP.md`
详细的自定义 AI API 配置指南，包括：
- 各种 AI 提供商的配置示例
- 兼容的第三方服务列表
- 配置说明和注意事项
- 故障排查指南

#### 2. `test_ai_integration.py`
测试脚本，用于验证 AI 服务配置是否正确

#### 3. `CHANGELOG_CUSTOM_AI.md`
本文件，记录此次更新的所有更改

## 使用方式

### 方式 1: 继续使用 Gemini (默认)

无需修改任何配置，保持现有设置即可。

### 方式 2: 使用 OpenAI API

在 `.env` 文件中添加：
```env
AI_PROVIDER=openai
CUSTOM_AI_API_URL=https://api.openai.com/v1
CUSTOM_AI_API_KEY=sk-your-api-key
CUSTOM_AI_MODEL=gpt-4
```

### 方式 3: 使用自定义 AI API

在 `.env` 文件中添加：
```env
AI_PROVIDER=custom
CUSTOM_AI_API_URL=https://your-api-endpoint.com/v1
CUSTOM_AI_API_KEY=your-api-key
CUSTOM_AI_MODEL=your-model-name
```

详细配置请参考 `AI_API_SETUP.md`。

## 兼容性说明

✅ **完全向后兼容**
- 现有使用 Gemini 的用户无需修改任何配置
- 所有现有功能保持不变
- 代码结构保持一致，其他模块无需修改

✅ **可选依赖**
- `google-genai` 库现在是可选的
- 如果只使用自定义 API，可以不安装 Gemini 相关依赖

✅ **优雅降级**
- 如果 AI 服务不可用，自动使用本地问题库
- 确保服务的高可用性

## 测试建议

1. 配置完成后运行测试脚本：
   ```bash
   python test_ai_integration.py
   ```

2. 发送测试消息给机器人，验证：
   - 新用户验证功能是否正常
   - 内容审查功能是否正常
   - 解封验证功能是否正常

3. 检查日志输出，确认 AI 服务调用正常

## 注意事项

⚠️ **API 成本**
使用付费 API 服务时请注意成本控制，可以通过设置 `ENABLE_AI_FILTER=false` 来禁用 AI 功能。

⚠️ **API 限制**
注意 API 服务商的调用频率限制和并发限制，避免超出配额。

⚠️ **模型选择**
建议使用支持视觉理解的模型（如 GPT-4 Vision）以充分利用图片内容审查功能。

## 未来计划

- [ ] 支持更多 AI 提供商的原生 SDK
- [ ] 添加 AI 响应缓存机制
- [ ] 支持自定义审查规则和提示词
- [ ] 添加 AI 使用统计和成本追踪

## 贡献

欢迎提交 Issue 和 Pull Request！

如果您成功集成了新的 AI 服务商，欢迎分享配置方案。
