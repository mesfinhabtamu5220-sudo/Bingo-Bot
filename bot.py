import os
import random
import logging
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# Logging configuration
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def generate_bingo_card():
    """የ 5x5 ቢንጎ ካርቴላ ምስል በ Pillow ይፈጥራል"""
    # 1. ቁጥሮችን በዘፈቀደ ማዘጋጀት
    b = random.sample(range(1, 16), 5)
    i = random.sample(range(16, 31), 5)
    n = random.sample(range(31, 46), 5)
    g = random.sample(range(46, 61), 5)
    o = random.sample(range(61, 76), 5)

    card_data = [b, i, n, g, o]

    # 2. የምስል መጠን እና ቀለሞች ማዋቀር
    width, height = 500, 600
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)

    # ርዕስ (B I N G O)
    headers = ["B", "I", "N", "G", "O"]
    cell_size = 80
    start_x = 50
    start_y = 100

    # B I N G O ርዕስ መጻፍ
    for col_idx, text in enumerate(headers):
        x = start_x + col_idx * cell_size
        draw.rectangle([x, 40, x + cell_size, 90], fill="#4CAF50", outline="black")
        draw.text((x + 32, 55), text, fill="white")

    # ሰንጠረዥ እና ቁጥሮችን መሳል
    for col_idx in range(5):
        for row_idx in range(5):
            x = start_x + col_idx * cell_size
            y = start_y + row_idx * cell_size
            
            # መካከለኛው ቦታ (FREE) ከሆነ
            if col_idx == 2 and row_idx == 2:
                val = "FREE"
                fill_color = "#FFD700"
            else:
                val = str(card_data[col_idx][row_idx])
                fill_color = "#F0F0F0"

            # ሳጥን መሳል
            draw.rectangle([x, y, x + cell_size, y + cell_size], fill=fill_color, outline="black")
            
            # ቁጥር መጻፍ
            text_x = x + 28 if len(val) == 1 else (x + 22 if len(val) == 2 else x + 18)
            if val == "FREE":
                text_x = x + 18

            draw.text((text_x, y + 32), val, fill="black")

    # ምስሉን ወደ Memory መጨመር
    bio = BytesIO()
    bio.name = 'bingo_card.png'
    image.save(bio, 'PNG')
    bio.seek(0)
    return bio

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    await update.message.reply_text(
        f"ሰላም {user_name}! ወደ ኦፊሻላዊው የቢንጎ ጨዋታ ቦት እንኳን ደህና መጡ! 🎯\n\n"
        "ካርቴላ ለማዘጋጀት /card የሚለውን ይጫኑ!"
    )

async def card_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ለተጠቃሚው የካርቴላ ምስል ይልካል"""
    await update.message.reply_text("የእርስዎን የቢንጎ ካርቴላ በማዘጋጀት ላይ ነው... ⏳")
    card_image = generate_bingo_card()
    await update.message.reply_photo(photo=card_image, caption="🎲 የእርስዎ የቢንጎ ካርቴላ ይኸውልዎት! መልካም ዕድል!")

if __name__ == '__main__':
    # 🔴 የእርስዎን የቴሌግራም ቦት ቶከን በቀጥታ ከዚህ በታች ባለው Quotation ውስጥ ያስገቡ
    TOKEN = "የእርስዎን_ቦት_ቶከን_እዚህ_ውስጥ_ያድርጉ"
    
    if not TOKEN or TOKEN == "የእርስዎን_ቦት_ቶከን_እዚህ_ውስጥ_ያድርጉ":
8875481705:AAGg09K0SL80r9yTS31rZ09KY0TZM_ASA7k
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('card', card_command))

    print("ቦቱ በስራ ላይ ነው...")
    application.run_polling()
