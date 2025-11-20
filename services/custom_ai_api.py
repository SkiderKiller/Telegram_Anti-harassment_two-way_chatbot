from fastapi import FastAPI, HTTPException, Header
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any, Union, AsyncGenerator
import json
import asyncio
import os
from google.genai import Client
from config import config
import re
import time

app = FastAPI(title="Custom AI API", description="OpenAI-compatible API using Gemini backend")

class Message(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: str = "gpt-3.5-turbo"
    messages: List[Message]
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = None
    stream: Optional[bool] = False
    top_p: Optional[float] = 1.0
    frequency_penalty: Optional[float] = 0.0
    presence_penalty: Optional[float] = 0.0

class ChatCompletionChoice(BaseModel):
    index: int
    message: Message
    finish_reason: str

class ChatCompletionUsage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

class ChatCompletionResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: List[ChatCompletionChoice]
    usage: ChatCompletionUsage

class ChatCompletionStreamChoice(BaseModel):
    index: int
    delta: Dict[str, Any]
    finish_reason: Optional[str] = None

class ChatCompletionStreamResponse(BaseModel):
    id: str
    object: str = "chat.completion.chunk"
    created: int
    model: str
    choices: List[ChatCompletionStreamChoice]

class ModelInfo(BaseModel):
    id: str
    object: str = "model"
    created: int = int(time.time())
    owned_by: str = "gemini-openai-adapter"

class ModelsResponse(BaseModel):
    object: str = "list"
    data: List[ModelInfo]

# 初始化Gemini客户端
gemini_client = None
if config.GEMINI_API_KEY:
    gemini_client = Client(api_key=config.GEMINI_API_KEY)

# 模型映射
MODEL_MAPPING = {
    "gpt-3.5-turbo": "gemini-2.0-flash-exp",
    "gpt-4": "gemini-2.0-flash-exp",
    "gpt-4-turbo": "gemini-2.0-flash-exp",
    "gpt-4o": "gemini-2.0-flash-exp",
    "text-davinci-003": "gemini-2.0-flash-exp",
    "gemini-pro": "gemini-2.0-flash-exp",
    "gemini-pro-vision": "gemini-2.0-flash-exp",
}

def get_gemini_model(openai_model: str) -> str:
    """将OpenAI模型名称映射到Gemini模型"""
    return MODEL_MAPPING.get(openai_model, "gemini-2.0-flash-exp")

def convert_messages_to_gemini_format(messages: List[Message]) -> List[str]:
    """将OpenAI消息格式转换为Gemini格式"""
    gemini_messages = []
    
    for message in messages:
        if message.role == "system":
            gemini_messages.append(f"System: {message.content}")
        elif message.role == "user":
            gemini_messages.append(f"Human: {message.content}")
        elif message.role == "assistant":
            gemini_messages.append(f"Assistant: {message.content}")
    
    return gemini_messages

def estimate_tokens(text: str) -> int:
    """简单估算token数量（大约1个token=4个字符）"""
    return len(text) // 4

async def verify_api_key(authorization: str = Header(None)) -> bool:
    """验证API密钥"""
    # 如果没有配置API密钥，则跳过验证
    if not config.CUSTOM_AI_API_KEY:
        return True
    
    if not authorization:
        raise HTTPException(status_code=401, detail="API key required")
    
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization format")
    
    api_key = authorization.replace("Bearer ", "")
    
    # 验证API密钥
    if api_key != config.CUSTOM_AI_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    return True

@app.get("/v1/models")
async def list_models():
    """列出可用模型"""
    models = [
        ModelInfo(id=model_id) 
        for model_id in MODEL_MAPPING.keys()
    ]
    
    return ModelsResponse(data=models)

@app.get("/v1/models/{model_id}")
async def get_model(model_id: str):
    """获取特定模型信息"""
    if model_id not in MODEL_MAPPING:
        raise HTTPException(status_code=404, detail="Model not found")
    
    return ModelInfo(id=model_id)

@app.post("/v1/chat/completions")
async def create_chat_completion(
    request: ChatCompletionRequest,
    authorization: str = Header(None)
):
    """创建聊天完成"""
    await verify_api_key(authorization)
    
    if request.stream:
        # 如果是流式请求，返回流式响应
        return StreamingResponse(
            generate_stream_response(request),
            media_type="text/plain",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Content-Type": "text/event-stream"
            }
        )
    else:
        # 非流式请求
        return await create_non_stream_completion(request)

async def create_non_stream_completion(request: ChatCompletionRequest) -> ChatCompletionResponse:
    """创建非流式聊天完成"""
    if not gemini_client:
        raise HTTPException(status_code=500, detail="Gemini client not initialized")
    
    try:
        # 转换消息格式
        gemini_messages = convert_messages_to_gemini_format(request.messages)
        
        # 构建完整的对话内容
        conversation = "\n".join(gemini_messages)
        
        # 添加系统提示
        system_prompt = "你是一个有用的AI助手。请用自然、友好的语调回答用户的问题。"
        full_prompt = f"{system_prompt}\n\n{conversation}\n\nAssistant: "
        
        # 获取对应的Gemini模型
        gemini_model = get_gemini_model(request.model)
        
        # 调用Gemini API
        response = await gemini_client.aio.models.generate_content(
            model=gemini_model,
            contents=full_prompt
        )
        
        if not response.candidates or not response.candidates[0].content.parts:
            raise HTTPException(status_code=500, detail="No response from Gemini")
        
        response_text = response.candidates[0].content.parts[0].text
        
        # 估算token使用量
        prompt_tokens = estimate_tokens(full_prompt)
        completion_tokens = estimate_tokens(response_text)
        total_tokens = prompt_tokens + completion_tokens
        
        # 构建OpenAI格式的响应
        choice = ChatCompletionChoice(
            index=0,
            message=Message(
                role="assistant",
                content=response_text
            ),
            finish_reason="stop"
        )
        
        usage = ChatCompletionUsage(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens
        )
        
        response_data = ChatCompletionResponse(
            id=f"chatcmpl-{int(time.time())}",
            created=int(time.time()),
            model=request.model,
            choices=[choice],
            usage=usage
        )
        
        return response_data
        
    except Exception as e:
        print(f"Error in chat completion: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def generate_stream_response(request: ChatCompletionRequest) -> AsyncGenerator[str, None]:
    """生成流式响应"""
    if not gemini_client:
        raise HTTPException(status_code=500, detail="Gemini client not initialized")
    
    try:
        # 转换消息格式
        gemini_messages = convert_messages_to_gemini_format(request.messages)
        
        # 构建完整的对话内容
        conversation = "\n".join(gemini_messages)
        
        # 添加系统提示
        system_prompt = "你是一个有用的AI助手。请用自然、友好的语调回答用户的问题。"
        full_prompt = f"{system_prompt}\n\n{conversation}\n\nAssistant: "
        
        # 获取对应的Gemini模型
        gemini_model = get_gemini_model(request.model)
        
        # 调用Gemini API（流式）
        response = await gemini_client.aio.models.generate_content(
            model=gemini_model,
            contents=full_prompt,
            stream=True
        )
        
        chunk_id = f"chatcmpl-{int(time.time())}"
        created = int(time.time())
        
        # 发送开始chunk
        start_chunk = ChatCompletionStreamResponse(
            id=chunk_id,
            created=created,
            model=request.model,
            choices=[ChatCompletionStreamChoice(
                index=0,
                delta={"role": "assistant"},
                finish_reason=None
            )]
        )
        yield f"data: {start_chunk.model_dump_json()}\n\n"
        
        # 流式发送内容
        accumulated_content = ""
        async for chunk in response:
            if chunk.candidates and chunk.candidates[0].content.parts:
                chunk_text = chunk.candidates[0].content.parts[0].text
                accumulated_content += chunk_text
                
                content_chunk = ChatCompletionStreamResponse(
                    id=chunk_id,
                    created=created,
                    model=request.model,
                    choices=[ChatCompletionStreamChoice(
                        index=0,
                        delta={"content": chunk_text},
                        finish_reason=None
                    )]
                )
                yield f"data: {content_chunk.model_dump_json()}\n\n"
        
        # 发送结束chunk
        end_chunk = ChatCompletionStreamResponse(
            id=chunk_id,
            created=created,
            model=request.model,
            choices=[ChatCompletionStreamChoice(
                index=0,
                delta={},
                finish_reason="stop"
            )]
        )
        yield f"data: {end_chunk.model_dump_json()}\n\n"
        yield "data: [DONE]\n\n"
        
    except Exception as e:
        print(f"Error in stream: {e}")
        error_chunk = {
            "error": {
                "message": str(e),
                "type": "internal_error"
            }
        }
        yield f"data: {json.dumps(error_chunk)}\n\n"

@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {
        "status": "healthy",
        "gemini_initialized": gemini_client is not None,
        "timestamp": int(time.time())
    }

@app.get("/")
async def root():
    """根端点"""
    return {
        "message": "Custom AI API - OpenAI Compatible API using Gemini Backend",
        "version": "1.0.0",
        "endpoints": {
            "models": "/v1/models",
            "chat": "/v1/chat/completions",
            "health": "/health"
        }
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("CUSTOM_AI_API_PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)