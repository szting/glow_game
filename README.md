# Rainbow Bot 🌈

A Telegram bot that helps strengthen relationships through daily rainbow-themed challenges, built with Python, FastAPI, and SQLAlchemy.

## 🏗️ Architecture

- **Bot Framework**: python-telegram-bot (most mature Python Telegram library)
- **Backend**: FastAPI (lightweight, auto-docs, easy async handling)
- **Database**: SQLite → PostgreSQL (smooth migration path)
- **ORM**: SQLAlchemy (smooth migration path between databases)
- **Deployment**: Railway.app

## 📁 Project Structure

```
rainbow-bot/
├── bot/
│   ├── handlers/          # Command handlers by feature
│   ├── models/           # SQLAlchemy models
│   ├── services/         # Business logic
│   ├── database/         # Database connection & migrations
│   └── utils/            # Helpers, translations
├── crowdsource/          # Community submission system
├── migrations/           # Database migrations (Alembic)
├── deploy/              # Railway deployment config
├── requirements.txt      # Python dependencies
├── alembic.ini          # Alembic configuration
├── railway.toml         # Railway deployment config
└── README.md            # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Telegram Bot Token (from [@BotFather](https://t.me/botfather))
- OpenAI API Key (optional, for image generation)
- Giphy API Key (optional, for GIFs)

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd rainbow-bot
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your actual values
   ```

5. **Initialize database**
   ```bash
   # Create initial migration
   alembic revision --autogenerate -m "Initial migration"
   
   # Apply migration
   alembic upgrade head
   ```

6. **Run the bot**
   ```bash
   python -m bot.main
   ```

### Environment Variables

Create a `.env` file with the following variables:

```env
# Bot Configuration
BOT_TOKEN=your_telegram_bot_token_here
WEBHOOK_URL=https://your-domain.com/webhook  # Optional for webhook mode
WEBHOOK_SECRET=your_webhook_secret_here      # Optional for webhook mode

# Database Configuration
DATABASE_URL=sqlite:///./rainbow_bot.db      # SQLite for development
# DATABASE_URL=postgresql://user:pass@host:port/db  # PostgreSQL for production

# API Keys
OPENAI_API_KEY=your_openai_api_key_here     # Optional
GIPHY_API_KEY=your_giphy_api_key_here       # Optional

# Application Settings
DEBUG=true                                   # Set to false in production
ENVIRONMENT=development                      # development/production
HOST=0.0.0.0
PORT=8000
```

## 🗄️ Database

### Development (SQLite)
The bot starts with SQLite for easy development. No additional setup required.

### Production (PostgreSQL)
When ready to scale, migrate to PostgreSQL:

1. **Update DATABASE_URL in .env**
   ```env
   DATABASE_URL=postgresql://user:pass@host:port/db
   ```

2. **Install PostgreSQL adapter**
   ```bash
   pip install psycopg2-binary
   ```

3. **Run migrations**
   ```bash
   alembic upgrade head
   ```

### Database Migrations

The project uses Alembic for database migrations:

```bash
# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback migrations
alembic downgrade -1

# View migration history
alembic history
```

## 🚀 Deployment on Railway

### 1. Connect GitHub Repository
- Push your code to GitHub
- Connect your repository to Railway.app

### 2. Set Environment Variables
In Railway dashboard, set the following environment variables:
- `BOT_TOKEN`
- `DATABASE_URL` (Railway provides PostgreSQL)
- `OPENAI_API_KEY` (optional)
- `GIPHY_API_KEY` (optional)
- `ENVIRONMENT=production`

### 3. Deploy
Railway will automatically deploy your application and provide:
- A public URL for your API
- PostgreSQL database
- Automatic HTTPS
- Auto-scaling capabilities

### 4. Set Webhook (Optional)
If using webhook mode instead of polling:

```bash
# Set webhook URL
curl -X POST "https://api.telegram.org/bot<BOT_TOKEN>/setWebhook" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://your-railway-app.railway.app/webhook"}'
```

## 🌐 API Documentation

Once deployed, visit `/docs` for interactive API documentation (Swagger UI).

### Available Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `POST /webhook` - Telegram webhook
- `GET /crowdsource/suggestions` - Get challenge suggestions
- `POST /crowdsource/submit` - Submit new challenge
- `PUT /crowdsource/suggestions/{id}/status` - Update suggestion status

## 🤖 Bot Commands

- `/start` - Begin your rainbow journey
- `/challenge` - Get today's challenge
- `/progress` - View your rainbow progress
- `/streak` - Check your current streak
- `/badges` - See your earned badges
- `/suggest` - Suggest a new challenge
- `/settings` - Change language or mode
- `/couple` - Couple mode options
- `/help` - Show help message

## 🎨 Features

### Individual Mode
- Personal growth and self-reflection
- Daily rainbow challenges
- Progress tracking and streaks
- Achievement badges

### Couple Mode
- Connect with your partner
- Shared challenges and progress
- Joint rainbow completion
- Real-time partner updates

### Group Mode
- Build collective rainbow with friends
- Group challenges and progress
- Member participation tracking

### Crowdsource System
- Submit new challenge ideas
- Community voting and feedback
- Admin approval workflow
- Web interface for submissions

## 🧪 Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=bot

# Run specific test file
pytest tests/test_user_service.py
```

## 📝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- Create an issue for bugs or feature requests
- Check the [Telegram Bot API documentation](https://core.telegram.org/bots/api)
- Review [FastAPI documentation](https://fastapi.tiangolo.com/)
- Check [SQLAlchemy documentation](https://docs.sqlalchemy.org/)

## 🔄 Migration from Old Version

If migrating from the previous aiogram-based version:

1. **Backup your data** (if using Supabase)
2. **Install new dependencies** from requirements.txt
3. **Set up new environment variables**
4. **Run database migrations**
5. **Test thoroughly before deploying**

## 🎯 Roadmap

- [ ] User analytics dashboard
- [ ] Advanced challenge algorithms
- [ ] Multi-language support expansion
- [ ] Mobile app companion
- [ ] Integration with calendar apps
- [ ] Social sharing features
- [ ] Advanced gamification elements