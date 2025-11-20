import logging
import asyncio
import threading
from telegram import Update
from telegram.ext import Application
from config import config
from handlers import register_handlers
from database.db_manager import DatabaseManager

# 自定义AI API服务器
def start_custom_ai_api():
    """启动自定义AI API服务器"""
    if config.ENABLE_CUSTOM_AI_API:
        try:
            import uvicorn
            from services.custom_ai_api import app
            
            def run_server():
                uvicorn.run(
                    app, 
                    host=config.CUSTOM_AI_API_HOST, 
                    port=config.CUSTOM_AI_API_PORT,
                    log_level="info"
                )
            
            # 在单独的线程中运行API服务器
            api_thread = threading.Thread(target=run_server, daemon=True)
            api_thread.start()
            
            logging.info(f"自定义AI API服务器已启动: http://{config.CUSTOM_AI_API_HOST}:{config.CUSTOM_AI_API_PORT}")
            logging.info("API文档地址: http://{}:{}/docs".format(config.CUSTOM_AI_API_HOST, config.CUSTOM_AI_API_PORT))
            
        except ImportError:
            logging.error("未安装FastAPI相关依赖，无法启动自定义AI API服务器")
        except Exception as e:
            logging.error(f"启动自定义AI API服务器失败: {e}")
    else:
        logging.info("自定义AI API服务器已禁用")

async def post_init(app: Application):
    config.BOT_ID = app.bot.id
    config.BOT_USERNAME = app.bot.username
    print(f"Bot ID: {config.BOT_ID} 已设置")
    print(f"Bot Username: {config.BOT_USERNAME} 已设置")

def main():

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    
    # 启动自定义AI API服务器
    start_custom_ai_api()
    
    db_manager = DatabaseManager(config.DATABASE_PATH)
    asyncio.run(db_manager.initialize())
    
    
    app = Application.builder().token(config.BOT_TOKEN).post_init(post_init).build()
    
    
    register_handlers(app)
    
    
    config.validate()
    
    
    logging.info("Bot启动中...")
    app.run_polling()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Bot已停止")
    except Exception as e:
        logging.error(f"启动失败: {e}")
        import traceback
        traceback.print_exc()
