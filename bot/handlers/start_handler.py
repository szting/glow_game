from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from sqlalchemy.orm import Session

from ..services.user_service import UserService
from ..keyboards import get_mode_keyboard, get_language_keyboard
from ..translations import get_text
from ..database.connection import get_db

class StartHandler:
    """Handle /start command and user setup"""
    
    def __init__(self):
        self.command = "start"
    
    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle the /start command"""
        user = update.effective_user
        chat_id = update.effective_chat.id
        
        # Get database session
        db = next(get_db())
        user_service = UserService(db)
        
        try:
            # Check if user already exists
            existing_user = await user_service.get_user(user.id)
            
            if existing_user:
                # User exists, show main menu
                await self._show_main_menu(update, context, existing_user)
            else:
                # New user, start setup process
                await self._start_setup(update, context)
                
        except Exception as e:
            await update.message.reply_text(
                "An error occurred during setup. Please try again."
            )
            print(f"Error in start handler: {e}")
        finally:
            db.close()
    
    async def _start_setup(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Start the user setup process"""
        welcome_text = get_text('en', 'welcome')
        choose_mode_text = get_text('en', 'choose_mode')
        
        # Store user state for setup
        context.user_data['setup_state'] = 'choosing_mode'
        
        await update.message.reply_text(
            f"{welcome_text}\n\n{choose_mode_text}",
            reply_markup=get_mode_keyboard('en')
        )
    
    async def _show_main_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE, user) -> None:
        """Show main menu for existing users"""
        from ..keyboards import get_main_menu_keyboard
        
        welcome_back = f"Welcome back, {user.username or 'Rainbow Friend'}! 🌈"
        await update.message.reply_text(
            welcome_back,
            reply_markup=get_main_menu_keyboard(user.language)
        )
    
    async def handle_mode_selection(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle mode selection callback"""
        query = update.callback_query
        await query.answer()
        
        mode = query.data.split(':')[1]
        context.user_data['selected_mode'] = mode
        
        # Move to language selection
        context.user_data['setup_state'] = 'choosing_language'
        
        choose_lang_text = get_text('en', 'choose_language')
        await query.edit_message_text(
            f"Mode selected: {mode}\n\n{choose_lang_text}",
            reply_markup=get_language_keyboard()
        )
    
    async def handle_language_selection(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle language selection callback"""
        query = update.callback_query
        await query.answer()
        
        language = query.data.split(':')[1]
        mode = context.user_data.get('selected_mode', 'individual')
        
        # Create user in database
        db = next(get_db())
        user_service = UserService(db)
        
        try:
            user = await user_service.create_user(
                telegram_id=update.effective_user.id,
                username=update.effective_user.username or "Unknown",
                language=language,
                mode=mode
            )
            
            # Setup complete
            setup_complete_text = get_text(language, 'setup_complete')
            await query.edit_message_text(setup_complete_text)
            
            # Clear setup state
            context.user_data.clear()
            
        except Exception as e:
            await query.edit_message_text(
                "An error occurred during setup. Please try /start again."
            )
            print(f"Error creating user: {e}")
        finally:
            db.close()
