import os
import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Rainbow Bot API",
    description="API for the Rainbow Bot Telegram application",
    version="1.0.0"
)

# Add CORS middleware to handle OPTIONS requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get bot token from environment
BOT_TOKEN = os.getenv('BOT_TOKEN')
logger.info(f"BOT_TOKEN loaded: {'Yes' if BOT_TOKEN else 'No'}")

# Create bot instance
bot = Bot(token=BOT_TOKEN) if BOT_TOKEN else None

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

@app.options("/webhook")
async def webhook_options():
    """Handle OPTIONS requests for CORS preflight"""
    return {"status": "ok"}

@app.post("/webhook")
async def webhook_post(request: Request):
    """Handle POST requests from Telegram with update data"""
    logger.info("Webhook POST received!")

    if not bot:
        logger.error("Bot token not configured!")
        raise HTTPException(status_code=500, detail="Bot token not configured")

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
                await bot.send_message(
                    chat_id=chat_id,
                    text="🌈 **Welcome to Rainbow Bot!**\n\nThis bot helps you strengthen relationships through daily rainbow-themed challenges.\n\nUse /help to see all commands."
                )
                return {"status": "start_command_handled", "chat_id": chat_id}

        return {"status": "ok"}

    except Exception as e:
        logger.error(f"Error in webhook: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.api_route("/webhook", methods=["GET", "POST", "OPTIONS", "PUT", "DELETE", "PATCH", "HEAD"])
async def webhook_all(request: Request):
    """Catch-all webhook handler for all HTTP methods"""
    method = request.method
    
    if method == "GET":
        return await webhook_test()
    elif method == "POST":
        return await webhook_post(request)
    elif method == "OPTIONS":
        return await webhook_options()
    else:
        return {
            "message": f"Method {method} not supported for webhook",
            "supported_methods": ["GET", "POST", "OPTIONS"],
            "status": "method_not_allowed"
        }

@app.get("/webhook")
async def webhook_test():
    """Test endpoint for webhook - allows GET requests for testing"""
    return {
        "message": "Webhook endpoint is working!",
        "status": "ready",
        "note": "This endpoint expects POST requests from Telegram with update data",
        "test_with": "Use POST method with Telegram update JSON to test actual functionality"
    }

# Test endpoint to verify bot works
@app.get("/test-bot")
async def test_bot():
    if not bot:
        return {"error": "Bot token not configured"}

    try:
        bot_info = await bot.get_me()
        return {
            "bot_username": bot_info.username,
            "bot_name": bot_info.first_name,
            "status": "working"
        }
    except Exception as e:
        return {"error": f"Bot test failed: {e}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)