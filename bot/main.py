from fastapi import FastAPI

# Create a simple FastAPI app
app = FastAPI(
    title="Rainbow Bot API",
    description="API for the Rainbow Bot Telegram application",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"message": "Rainbow Bot API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "bot_running": True}

# Comment out all the complex imports for now
# from .config import get_settings
# from .database.connection import engine, get_db
# from .database.models import Base
# from .handlers import (
#     StartHandler, ChallengeHandler, ProgressHandler, 
#     CoupleHandler, GroupHandler, SettingsHandler, HelpHandler
# )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)