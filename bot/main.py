import os
import logging
from fastapi import FastAPI, Request
from telegram import Update

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Rainbow Bot API",
    description="API for the Rainbow Bot Telegram application",
    version="1.0.0"
)

# Get bot token from environment
BOT_TOKEN = os.getenv('BOT_TOKEN')
logger.info(f"BOT_TOKEN loaded: {'Yes' if BOT_TOKEN else 'No'}")

@app.get("/")
async def root():
    return {"message": "Rainbow Bot API", "status": "running"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "bot_running": BOT_TOKEN is not None,
        "bot_token_length": len(BOT_TOKEN) if BOT_TOKEN else 0
    }

@app.post("/webhook")
async def webhook(request: Request):
    logger.info("Webhook received!")
    
    try:
        # Get the update data
        update_data = await request.json()
        logger.info(f"Update data: {update_data}")
        
        # Check if it's a /start command
        if 'message' in update_data and 'text' in update_data['message']:
            text = update_data['message']['text']
            chat_id = update_data['message']['chat']['id']
            logger.info(f"Received message: {text} from chat {chat_id}")
            
            if text == "/start":
                logger.info("Start command received!")
                # For now, just log it
                return {"status": "start_command_received", "chat_id": chat_id}
        
        return {"status": "ok"}
        
    except Exception as e:
        logger.error(f"Error in webhook: {e}")
        return {"error": str(e)}

# Don't run uvicorn here - let Railway handle it