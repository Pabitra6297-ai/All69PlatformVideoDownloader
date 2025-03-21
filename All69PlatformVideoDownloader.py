import os
import yt_dlp
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Your bot token
BOT_TOKEN = "7504514258:AAGAPx-OAw8epM7zr9nWj3WtgTBdt1_ASp0"

# Your Telegram Channel Username (without @)
CHANNEL_USERNAME = "Viral_Meme_Templates"

# Directory to save downloaded videos
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def is_user_member(update: Update, context: CallbackContext) -> bool:
    """Check if the user is a member of the required channel."""
    user_id = update.message.chat.id
    try:
        member_status = context.bot.get_chat_member(f"@{CHANNEL_USERNAME}", user_id).status
        return member_status in ["member", "administrator", "creator"]
    except Exception:
        return False  # If an error occurs, assume they are not a member

def start(update: Update, context: CallbackContext) -> None:
    """Send a welcome message and enforce channel check."""
    if not is_user_member(update, context):
        keyboard = [[InlineKeyboardButton("🔥 Join Our Channel 🔥", url=f"https://t.me/{CHANNEL_USERNAME}")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            f"🚫 *Access Denied!*\n\n"
            f"👋 To use this bot, you must join our channel:\n"
            f"✅ [Click Here to Join](https://t.me/{CHANNEL_USERNAME})\n"
            f"🔄 After joining, send /start again!",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        return

    update.message.reply_text(
        "🎥 *Welcome to Video Downloader Bot!* 📥\n\n"
        "📌 Send me a video link from:\n"
        "  - 🎬 YouTube\n"
        "  - 📘 Facebook\n"
        "  - 📸 Instagram\n"
        "  - 🎵 TikTok\n\n"
        "💡 I will download and send it to you!\n\n"
        "🔄 *To restart, send* /start",
        parse_mode="Markdown"
    )

def download_video(url: str) -> str:
    """Downloads video using yt-dlp and returns the file path."""
    ydl_opts = {
        'outtmpl': f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
        'format': 'best',
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        file_path = ydl.prepare_filename(info)
    
    return file_path

def handle_message(update: Update, context: CallbackContext) -> None:
    """Handle user messages & enforce channel check."""
    if not is_user_member(update, context):
        keyboard = [[InlineKeyboardButton("🔥 Join Our Channel 🔥", url=f"https://t.me/{CHANNEL_USERNAME}")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            f"🚫 *Access Denied!*\n\n"
            f"👋 To use this bot, you must join our channel:\n"
            f"✅ [Click Here to Join](https://t.me/{CHANNEL_USERNAME})\n"
            f"🔄 After joining, send /start again!",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        return
    
    url = update.message.text.strip()
    
    # Check if the message is a valid URL
    if any(x in url for x in ["youtube.com", "youtu.be", "facebook.com", "instagram.com", "tiktok.com"]):
        update.message.reply_text("📥 *Downloading your video... Please wait!*", parse_mode="Markdown")
        
        try:
            file_path = download_video(url)
            
            # File size check (Telegram max 2GB)
            file_size = os.path.getsize(file_path) / (1024 * 1024)  # Convert to MB
            if file_size > 2000:  # 2GB Limit
                update.message.reply_text("🚫 *Video is too large! (Over 2GB)*\nTry a smaller file.", parse_mode="Markdown")
                os.remove(file_path)
                return

            update.message.reply_video(video=open(file_path, 'rb'), caption="✅ *Here is your video!*", parse_mode="Markdown")
            os.remove(file_path)  # Delete after sending
        except Exception as e:
            update.message.reply_text(f"❌ *Failed to download video:*\n{str(e)}", parse_mode="Markdown")
    else:
        update.message.reply_text("⚠️ *Invalid URL! Please send a valid video link.*", parse_mode="Markdown")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()