import asyncio
import logging
from contextlib import asynccontextmanager
from typing import Dict, Any

from fastapi import FastAPI

app = FastAPI(
    title="Rainbow Bot API",
    description="API for the Rainbow Bot Telegram application",
    version="1.0.0"
)

# Your routes should be defined on this 'app' object
@app.get("/health")
async def health_check():
    return {"status": "healthy", "bot_running": True}

from .config import get_settings
from .database.connection import engine, get_db
from .database.models import Base
from .handlers import (
    StartHandler, ChallengeHandler, ProgressHandler, 
    CoupleHandler, GroupHandler, SettingsHandler, HelpHandler
)

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Global bot application
bot_app: Application = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan"""
    # Startup
    global bot_app
    bot_app = await setup_bot()
    
    # Create database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    logger.info("Bot started successfully")
    
    yield
    
    # Shutdown
    if bot_app:
        await bot_app.stop()
        await bot_app.shutdown()
    logger.info("Bot stopped")

# Create FastAPI app
app = FastAPI(
    title="Rainbow Bot API",
    description="API for the Rainbow Bot Telegram application",
    version="1.0.0",
    lifespan=lifespan
)

async def setup_bot() -> Application:
    """Setup and configure the Telegram bot"""
    settings = get_settings()
    
    # Create bot application
    application = Application.builder().token(settings.bot_token).build()
    
    # Add handlers
    start_handler = StartHandler()
    challenge_handler = ChallengeHandler()
    progress_handler = ProgressHandler()
    couple_handler = CoupleHandler()
    group_handler = GroupHandler()
    settings_handler = SettingsHandler()
    help_handler = HelpHandler()
    
    # Command handlers
    application.add_handler(CommandHandler("start", start_handler.handle))
    application.add_handler(CommandHandler("challenge", challenge_handler.handle))
    application.add_handler(CommandHandler("progress", progress_handler.handle))
    application.add_handler(CommandHandler("couple", couple_handler.handle))
    application.add_handler(CommandHandler("group", group_handler.handle))
    application.add_handler(CommandHandler("settings", settings_handler.handle))
    application.add_handler(CommandHandler("help", help_handler.handle))
    
    # Callback query handlers
    application.add_handler(CallbackQueryHandler(start_handler.handle_mode_selection, pattern="^mode:"))
    application.add_handler(CallbackQueryHandler(start_handler.handle_language_selection, pattern="^lang:"))
    
    # Message handlers for responses
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, challenge_handler.handle_text_response))
    application.add_handler(MessageHandler(filters.PHOTO, challenge_handler.handle_photo_response))
    application.add_handler(MessageHandler(filters.VOICE, challenge_handler.handle_voice_response))
    
    return application

@app.post("/webhook")
async def webhook(request: Request):
    """Handle webhook updates from Telegram"""
    if not bot_app:
        return {"error": "Bot not initialized"}
    
    try:
        # Parse update from request body
        update_data = await request.json()
        update = Update.de_json(update_data, bot_app.bot)
        
        # Process update
        await bot_app.process_update(update)
        
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        return {"error": str(e)}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "bot_running": bot_app is not None}

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Rainbow Bot API",
        "version": "1.0.0",
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    settings = get_settings()
    
    uvicorn.run(
        "bot.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )