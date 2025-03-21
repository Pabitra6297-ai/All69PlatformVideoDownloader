import os
import yt_dlp
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Load environment variables
BOT_TOKEN = os.getenv("7504514258:AAGAPx-OAw8epM7zr9nWj3WtgTBdt1_ASp0")  # Add your bot token in Render environment
CHANNEL_ID = os.getenv("Viral_Meme_Templates")  # Set your channel username (e.g., @Viral_Meme_Templates)

async def start(update: Update, context: CallbackContext):
    """Handles /start command and checks if the user joined the channel."""
    user_id = update.message.chat.id

    # Check if the user is a member of the channel
    response = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getChatMember?chat_id={CHANNEL_ID}&user_id={user_id}").json()
    status = response.get("result", {}).get("status", "")

    if status not in ["member", "administrator", "creator"]:
        keyboard = [[InlineKeyboardButton("🔗 Join Channel", url=f"https://t.me/{CHANNEL_ID[1:]}")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("⚠️ *You must join our channel to use this bot!*", reply_markup=reply_markup, parse_mode="Markdown")
        return

    await update.message.reply_text("✅ Welcome! Send me any video link to download.")

async def download_video(update: Update, context: CallbackContext):
    """Handles video downloading"""
    url = update.message.text

    try:
        ydl_opts = {"outtmpl": "downloads/%(title)s.%(ext)s"}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_name = ydl.prepare_filename(info)

        with open(file_name, "rb") as video:
            await update.message.reply_video(video, caption="🎥 Here is your downloaded video!")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

# Initialize bot
app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

# Run bot
if __name__ == "__main__":
    print("🚀 Bot is running...")
    app.run_polling()
