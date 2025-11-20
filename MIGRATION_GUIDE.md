# 迁移指南：切换到自定义 AI API

本指南帮助您将项目从 Gemini API 迁移到自定义 AI API，或在两者之间切换。

## 无需迁移（继续使用 Gemini）

如果您当前使用 Gemini API 且满意其性能，**无需进行任何更改**。项目默认使用 Gemini，所有现有配置保持有效。

## 从 Gemini 迁移到 OpenAI

### 步骤 1: 获取 OpenAI API 密钥

1. 访问 [OpenAI Platform](https://platform.openai.com/)
2. 注册或登录您的账户
3. 导航到 API Keys 页面
4. 创建新的 API 密钥并保存

### 步骤 2: 更新 .env 配置

在您的 `.env` 文件中修改以下配置：

```env
# 修改 AI 提供商
AI_PROVIDER=openai

# 保留或注释掉 Gemini 配置（可选）
# GEMINI_API_KEY=your_gemini_api_key_here

# 添加 OpenAI 配置
CUSTOM_AI_API_URL=https://api.openai.com/v1
CUSTOM_AI_API_KEY=sk-your-api-key-here
CUSTOM_AI_MODEL=gpt-4
CUSTOM_AI_VERIFICATION_MODEL=gpt-3.5-turbo  # 可选，节省成本
```

### 步骤 3: 重启机器人

如果使用 Docker:
```bash
docker-compose restart
```

如果手动运行:
```bash
# 停止当前运行的机器人
# 然后重新运行
python bot.py
```

## 从 Gemini 迁移到其他自定义 API

### 步骤 1: 准备 API 信息

确保您的 API 服务：
- 完全兼容 OpenAI API v1 格式
- 支持 `/chat/completions` 端点
- （可选）支持视觉模型以使用图片审查功能

### 步骤 2: 更新 .env 配置

```env
# 修改 AI 提供商
AI_PROVIDER=custom

# 添加自定义 API 配置
CUSTOM_AI_API_URL=https://your-api-endpoint.com/v1
CUSTOM_AI_API_KEY=your_api_key_here
CUSTOM_AI_MODEL=your-model-name
```

### 步骤 3: 测试配置

运行测试脚本验证配置：
```bash
python test_ai_integration.py
```

### 步骤 4: 重启机器人

同上述 OpenAI 迁移步骤。

## 在不同 AI 提供商之间切换

您可以随时通过修改 `AI_PROVIDER` 环境变量在不同提供商之间切换：

```env
# 使用 Gemini
AI_PROVIDER=gemini

# 使用 OpenAI
AI_PROVIDER=openai

# 使用自定义 API
AI_PROVIDER=custom
```

切换后重启机器人即可生效。

## 成本对比和建议

### Gemini API
- **优点**: 免费配额较高，响应快
- **缺点**: 可能在某些地区不可用
- **适用**: 个人项目、小型部署

### OpenAI API
- **优点**: 模型能力强，稳定性高
- **缺点**: 需要付费，成本较高
- **适用**: 商业项目、对质量要求高的场景
- **省钱技巧**: 使用 `gpt-3.5-turbo` 作为验证模型

### 自定义 API（国产模型）
- **优点**: 国内访问快，价格便宜
- **缺点**: 需要验证兼容性
- **适用**: 国内部署、成本敏感的项目

## 常见问题

### Q: 切换 AI 提供商会丢失数据吗？
A: 不会。AI 提供商只影响内容审查和问题生成功能，不会影响用户数据、消息记录等。

### Q: 可以同时使用多个 AI 提供商吗？
A: 当前版本一次只能使用一个提供商。未来可能支持多提供商负载均衡。

### Q: 如果 API 调用失败会怎样？
A: 系统会自动使用本地预设的问题库作为后备方案，确保基本功能正常运行。

### Q: 需要重新安装依赖吗？
A: 如果从 Gemini 切换到 OpenAI/自定义 API，需要安装 `openai` 库。如果使用 Docker，重新构建镜像即可。

### Q: 如何控制 API 使用成本？
A: 
1. 使用较便宜的模型作为验证模型
2. 设置 `ENABLE_AI_FILTER=false` 禁用 AI 内容审查
3. 设置适当的速率限制
4. 监控 API 使用量

## 回滚到 Gemini

如果遇到问题需要回滚：

```env
AI_PROVIDER=gemini
```

重启机器人即可。无需卸载 OpenAI 库或删除配置。

## 获取帮助

如遇问题：
1. 查看 `AI_API_SETUP.md` 中的故障排查章节
2. 运行 `test_ai_integration.py` 诊断问题
3. 查看机器人日志输出
4. 在 GitHub 提交 Issue
