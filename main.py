from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Your API Credentials
API_ID = 37197223
API_HASH = "3a43ae287a696ee9a6a82fb79f605b75"
BOT_TOKEN = "8336671886:AAGrAv4g0CEc4X8kO1CFv7R8hucIMck60ac"

app = Client("tempest_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    # Check if user came from a file link (e.g., /start 123)
    if len(message.command) > 1:
        file_id = int(message.command[1])
        try:
            # This sends the stored file to the user
            await client.copy_message(
                chat_id=message.chat.id,
                from_chat_id=message.chat.id, 
                message_id=file_id
            )
        except Exception as e:
            await message.reply_text("❌ Error: This file is no longer available.")
    else:
        # Standard welcome message
        await message.reply_text(
            f"Hello {message.from_user.mention}!\n\n"
            "Welcome to the **Tempest Network** File Store Bot.\n"
            "Send me any file and I will provide a permanent sharing link.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Join Tempest Network", url="https://t.me/your_channel_link")]
            ])
        )

@app.on_message(filters.document | filters.video | filters.audio | filters.photo)
async def handle_files(client, message):
    status_msg = await message.reply_text("⏳ Processing your file...")
    
    # Generate the sharing link
    msg_id = message.id
    bot_username = (await client.get_me()).username
    share_link = f"https://t.me/{bot_username}?start={msg_id}"
    
    await status_msg.edit_text(
        f"✅ **File Stored Successfully!**\n\n"
        f"🔗 **Your Share Link:**\n`{share_link}`",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Share Link", url=f"https://t.me/share/url?url={share_link}")]
        ])
    )

print("Tempest Network Bot is Running...")
app.run()
