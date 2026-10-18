import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# Logging configuration
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    await update.message.reply_text(
        f"ሰላም {user_name}! ወደ ኦፊሻላዊው የቢንጎ ጨዋታ ቦት እንኳን ደህና መጡ! 🎯\n\n"
        "ጨዋታውን ለመጀመር ወይም ከርት ለማግኘት /help የሚለውን ይጠቀሙ።"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ምዕራፍ እና የእርዳታ ማዕከል:\n"
        "/start - ጨዋታውን ለመጀመር\n"
        "/help - የቦቱን ህግ እና እርዳታ ለማግኘት\n"
        "/balance - የሂሳብ መጠንዎን ለማየት"
    )

async def balance_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("የእርስዎ የሂሳብ መጠን: 0 ብር 💰")

if __name__ == '__main__':
    # በ Render ላይ Environment Variable ሆኖ የሚሰጠውን Token እዚህ በራስ ሰር እንዲነበብ ይደረጋል
    import os
    TOKEN = os.getenv("BOT_TOKEN")
    
    if not TOKEN:
        raise ValueError("ሰላም! BOT_TOKEN አልተገኘም፤ እባክዎ Render ላይ Environment Variable ያስገቡ።")

    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('balance', balance_command))

    print("ቦቱ በመጀመር ላይ ነው...")
    application.run_polling()
