# 自定义 AI API 功能总结

## 功能概述

本次更新为 Telegram 双向聊天机器人项目添加了对自定义 AI API 的支持，允许用户使用任何符合 OpenAI API v1 格式的 AI 服务。

## 主要特性

### ✨ 多 AI 提供商支持

- **Google Gemini** (默认)
- **OpenAI** (GPT-3.5, GPT-4 等)
- **自定义 AI API** (任何 OpenAI v1 兼容服务)

### 🔧 灵活配置

通过环境变量轻松切换不同的 AI 服务：

```env
# 三选一
AI_PROVIDER=gemini    # 使用 Gemini
AI_PROVIDER=openai    # 使用 OpenAI
AI_PROVIDER=custom    # 使用自定义 API
```

### 🛡️ 向后兼容

- 现有 Gemini 用户无需任何更改
- 自动回退机制确保服务稳定性
- 可选依赖，不强制安装 OpenAI 库

### 🌐 广泛兼容

支持多种第三方服务：
- Azure OpenAI
- 国产大模型（讯飞星火、通义千问、文心一言等）
- 本地部署模型（Ollama、vLLM 等）
- 任何提供 OpenAI v1 兼容接口的服务

## 使用场景

### 场景 1: 成本优化

使用更便宜的 AI 服务替代 Gemini：

```env
AI_PROVIDER=custom
CUSTOM_AI_API_URL=https://cheap-api.com/v1
CUSTOM_AI_MODEL=low-cost-model
```

### 场景 2: 本地部署

使用本地模型确保数据隐私：

```env
AI_PROVIDER=custom
CUSTOM_AI_API_URL=http://localhost:11434/v1
CUSTOM_AI_MODEL=llama3
```

### 场景 3: 企业级应用

使用 Azure OpenAI 获得企业级 SLA：

```env
AI_PROVIDER=custom
CUSTOM_AI_API_URL=https://your-resource.openai.azure.com/openai/deployments
CUSTOM_AI_MODEL=your-deployment-name
```

### 场景 4: 地区限制

在 Gemini 不可用的地区使用其他服务：

```env
AI_PROVIDER=custom
CUSTOM_AI_API_URL=https://domestic-ai-service.com/v1
CUSTOM_AI_MODEL=chinese-model
```

## 功能影响范围

自定义 AI API 将用于：

1. **内容审查** - 分析用户消息，识别垃圾信息和不当内容
2. **人机验证** - 为新用户生成验证问题
3. **解封验证** - 为被封禁用户生成解封问题

## 技术实现

### 核心组件

1. **config.py**
   - 添加 AI 提供商相关配置项
   - 支持灵活的环境变量配置

2. **services/openai_service.py**
   - 实现 OpenAI API v1 兼容客户端
   - 支持文本和图片内容分析
   - 集成本地问题库作为后备

3. **services/gemini_service.py**
   - 添加服务工厂函数
   - 实现自动服务选择和回退
   - 保持 Gemini 服务完整性

### 依赖更新

```txt
# 新增依赖
openai>=1.0.0
```

## 配置示例

### 最小配置（OpenAI）

```env
BOT_TOKEN=your_bot_token
FORUM_GROUP_ID=-1001234567890
ADMIN_IDS=123456789

AI_PROVIDER=openai
CUSTOM_AI_API_URL=https://api.openai.com/v1
CUSTOM_AI_API_KEY=sk-your-key
CUSTOM_AI_MODEL=gpt-3.5-turbo
```

### 完整配置（自定义 API）

```env
BOT_TOKEN=your_bot_token
FORUM_GROUP_ID=-1001234567890
ADMIN_IDS=123456789

AI_PROVIDER=custom
CUSTOM_AI_API_URL=https://your-api.com/v1
CUSTOM_AI_API_KEY=your_api_key
CUSTOM_AI_MODEL=your-main-model
CUSTOM_AI_VERIFICATION_MODEL=your-cheap-model

ENABLE_AI_FILTER=true
AI_CONFIDENCE_THRESHOLD=70
```

## 文档资源

项目包含完整的文档支持：

- **AI_API_SETUP.md** - 详细的 API 配置指南
- **MIGRATION_GUIDE.md** - 从 Gemini 迁移的步骤
- **CHANGELOG_CUSTOM_AI.md** - 完整的更改记录
- **test_ai_integration.py** - 配置测试脚本

## 测试验证

使用提供的测试脚本验证配置：

```bash
python test_ai_integration.py
```

测试内容：
- 配置加载验证
- AI 服务初始化
- 验证问题生成
- 解封问题生成

## 性能和成本

### Gemini API
- 免费配额：60 请求/分钟
- 响应时间：~1-2 秒
- 成本：免费（有配额限制）

### OpenAI API
- 限制：根据账户级别
- 响应时间：~1-3 秒
- 成本：
  - GPT-3.5-turbo: $0.0015/1K tokens
  - GPT-4: $0.03/1K tokens
  - GPT-4 Vision: $0.01/image + token cost

### 自定义 API
- 根据具体服务商而定
- 国产模型通常更便宜
- 本地部署几乎无成本

## 安全考虑

1. **API 密钥保护**
   - 使用 .env 文件存储
   - 不要提交到版本控制
   - 定期轮换密钥

2. **数据隐私**
   - 了解 API 服务商的数据政策
   - 本地部署可确保完全隐私
   - 避免发送敏感信息到第三方

3. **成本控制**
   - 设置 API 使用配额
   - 监控调用量
   - 使用 ENABLE_AI_FILTER 控制开关

## 未来计划

- [ ] 支持多提供商负载均衡
- [ ] 添加响应缓存机制
- [ ] 自定义审查规则和提示词
- [ ] AI 使用统计和成本追踪
- [ ] 支持更多 AI 提供商的原生 SDK

## 贡献

欢迎贡献代码和文档！特别欢迎：
- 新的 AI 提供商集成
- 配置示例和最佳实践
- 性能优化建议
- Bug 报告和修复

## 许可证

本项目采用 MIT 许可协议。

---

**版本**: v2.0  
**更新日期**: 2024  
**维护者**: 项目团队
