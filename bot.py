import os
import logging
import yt_dlp
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, filters
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext

# Enable Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get API Token from Environment Variable
TOKEN = os.getenv("7504514258:AAGAPx-OAw8epM7zr9nWj3WtgTBdt1_ASp0")
CHANNEL_ID = "@Viral_Meme_Templates"  # Your Telegram channel username

# Function to Check if User is Subscribed
async def is_subscribed(user_id: int) -> bool:
    url = f"https://api.telegram.org/bot{TOKEN}/getChatMember?chat_id={CHANNEL_ID}&user_id={user_id}"
    response = requests.get(url).json()
    status = response.get("result", {}).get("status", "")
    return status in ["member", "administrator", "creator"]

# Start Command
async def start(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    if not await is_subscribed(user_id):
        keyboard = [[InlineKeyboardButton("🔗 Join Channel", url=f"https://t.me/{CHANNEL_ID}")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "🚀 To use this bot, you must join our channel first!", reply_markup=reply_markup
        )
        return
    
    await update.message.reply_text("🎬 Send me any video link (YouTube, TikTok, Instagram, Facebook) and I'll download it for you!")

# Download Video Function
async def download_video(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    if not await is_subscribed(user_id):
        keyboard = [[InlineKeyboardButton("🔗 Join Channel", url=f"https://t.me/{CHANNEL_ID}")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "🚀 To use this bot, you must join our channel first!", reply_markup=reply_markup
        )
        return

    url = update.message.text
    await update.message.reply_text("⏳ Downloading video, please wait...")

    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.mp4',
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        with open("video.mp4", "rb") as video:
            await update.message.reply_video(video, caption="✅ Here is your downloaded video!")

        os.remove("video.mp4")
    
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {str(e)}")

# Main Function
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

    logger.info("🚀 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
