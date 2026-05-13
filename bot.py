import os
import json
import asyncio
from flask import Flask
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# --- RENDER WEB SERVER ---
flask_app = Flask('')

@flask_app.route('/')
def home():
    return "Bot is alive!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    flask_app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_web)
    t.daemon = True
    t.start()

# --- CONFIGURATION ---
BOT_TOKEN = os.environ.get("BOT_TOKEN") # Render Dashboard se uthayega
ADMIN_HANDLE = "@Shadow_atomic_21"
STYLE_FILE = "user_styles.json"
THUMB_DIR = "thumbnails"

if not os.path.exists(THUMB_DIR):
    os.makedirs(THUMB_DIR)

# --- DATA PERSISTENCE ---
def load_styles():
    if os.path.exists(STYLE_FILE):
        try:
            with open(STYLE_FILE, "r") as f: return json.load(f)
        except: return {}
    return {}

def save_styles(data):
    with open(STYLE_FILE, "w") as f: json.dump(data, f)

user_styles = load_styles()

# --- CAPTION ENGINE (POORE 30 STYLES) ---
def get_caption(anime, season, ep, quality, audio, power, style_choice):
    ep_str = f"{ep:02d}"
    sn_str = f"{int(season):02d}"
    
    styles = [
        f"<b>{anime} ━━━━━━━━━━━━━━━━━━━━━━━━\n° Season : {sn_str} ° Episode : {ep_str}\n° Quality : {quality}\n° Audio : {audio}\n━━━━━━━━━━━━━━━━━━━━━━━━\n<blockquote>➳ᴘᴏᴡᴇʀᴇᴅ ʙʏ:- {power}</blockquote></b>",
        f"<b>❖  ᴇᴘɪsᴏᴅᴇ: {ep_str}\n✧  ʟᴀɴɢᴜᴀɢᴇ: {audio}\n➠  ǫᴜᴀʟɪᴛʏ: {quality} \n━━━━━━━━━━━━━━\n<blockquote>➳ᴘᴏᴡᴇʀᴇᴅ ʙʏ:- \n{power}</blockquote></b>",
        f"<b>╔═══════════════════╗\n  {anime} [S{sn_str}]\n╚═══════════════════╝\n◈ Episode: {ep_str}\n◈ Audio: {audio}\n◈ Quality: {quality}\n<blockquote>🚀 {power}</blockquote></b>",
        f"<b>『 {anime} 』\n────────────────\nSeason: {sn_str} ⚡️ Episode: {ep_str}\nQuality: {quality}\nAudio: {audio}\n<blockquote>🔗 Join: {power}</blockquote></b>",
        f"<b>🔥 {anime} 🔥\n━━━━━━━━━━━━━━━\n💥 Season: {sn_str}\n💥 Episode: {ep_str}\n💥 Audio: {audio}\n💥 Quality: {quality}\n<blockquote>✨ Credits: {power}</blockquote></b>",
        f"<b>[ ʟᴏᴀᴅɪɴɢ {anime}... ]\n\n■ ᴇᴘɪsᴏᴅᴇ : {ep_str}\n■ ǫᴜᴀʟɪᴛʏ : {quality}\n■ ᴀᴜᴅɪᴏ : {audio}\n<blockquote>⚡️ sʏsᴛᴇᴍ: {power}</blockquote></b>",
        f"<b>💠 {anime} 💠\n\n🔹 Episode : {ep_str}\n🔹 Quality : {quality}\n🔹 Language: {audio}\n<blockquote>💎 {power}</blockquote></b>",
        f"<b>🌸 {anime} 🌸\n━━━━━━━━━━━━━━━\n✿ Episode: {ep_str}\n✿ Quality: {quality}\n✿ Audio  : {audio}\n<blockquote>💌 {power}</blockquote></b>",
        f"<b>╭┈─────── ೄྀ࿐ ˊˎ-\n╰┈➤ ❝ {anime} ❞\n\n📍 Ep: {ep_str} | Sn: {sn_str}\n📍 Quality: {quality}\n📍 Audio: {audio}\n<blockquote>🕊️ {power}</blockquote></b>",
        f"<b>⛩️ {anime} ⛩️\n🏮 Season: {sn_str}\n🏮 Episode: {ep_str}\n🏮 Audio: {audio}\n<blockquote>🎴 {power}</blockquote></b>",
        f"<b>➠ {anime} S{sn_str}\n\n➠ Episode : {ep_str}\n➠ Resolution: {quality}\n➠ Language : {audio}\n<blockquote>➠ Join: {power}</blockquote></b>",
        f"<b>┎┈┈┈┈┈┈┈┈┈┈┈┈┈┒\n  {anime}\n┖┈┈┈┈┈┈┈┈┈┈┈┈┈┚\n◈ Ep: {ep_str} | Q: {quality}\n◈ Audio: {audio}\n<blockquote>🛡️ {power}</blockquote></b>",
        f"<b>🌟 {anime} 🌟\n\n⭐ Episode: {ep_str}\n⭐ Quality: {quality}\n⭐ Audio: {audio}\n<blockquote>🌟 Uploaded By: {power}</blockquote></b>",
        f"<b>● {anime} S{sn_str} ●\n\n◦ Ep: {ep_str}\n◦ Res: {quality}\n◦ Lang: {audio}\n<blockquote>🔗 {power}</blockquote></b>",
        f"<b>⚡️ {anime} ⚡️\n────────────────\n⚡️ Ep: {ep_str}\n⚡️ Qual: {quality}\n⚡️ Audio: {audio}\n<blockquote>⚡️ Link: {power}</blockquote></b>",
        f"<b>💀 {anime} [S{sn_str}]\n────────────────\n👻 Episode: {ep_str}\n👻 Quality: {quality}\n👻 Audio: {audio}\n<blockquote>🌑 {power}</blockquote></b>",
        f"<b>👑 {anime} 👑\n━━━━━━━━━━━━━━━\n🔱 Ep: {ep_str}\n🔱 Res: {quality}\n🔱 Audio: {audio}\n<blockquote>🏰 {power}</blockquote></b>",
        f"<b>🫧 {anime} 🫧\n◌ Ep: {ep_str}\n◌ Res: {quality}\n◌ Lang: {audio}\n<blockquote>🫧 Credit: {power}</blockquote></b>",
        f"<b>🍃 {anime} 🍃\n━━━━━━━━━━━━━━━\n🌿 Episode: {ep_str}\n🌿 Quality: {quality}\n🌿 Audio: {audio}\n<blockquote>🍀 {power}</blockquote></b>",
        f"<b>网 {anime} 网\n\n格 Ep: {ep_str}\n格 Res: {quality}\n格 Lang: {audio}\n<blockquote>🌐 {power}</blockquote></b>",
        f"<b>◤ {anime} ◢\n\n➤ Ep: {ep_str}\n➤ Qual: {quality}\n➤ Lang: {audio}\n<blockquote>◢ {power} ◣</blockquote></b>",
        f"<b>═ {anime} ═\n\n║ Season: {sn_str}\n║ Episode: {ep_str}\n║ Audio: {audio}\n<blockquote>═ {power} ═</blockquote></b>",
        f"<b>🛡️ {anime} 🛡️\n\n⚔️ Episode: {ep_str}\n⚔️ Quality: {quality}\n⚔️ Language: {audio}\n<blockquote>🛡️ Powered by: {power}</blockquote></b>",
        f"<b>▣ {anime} S{sn_str}\n\n▣ Ep: {ep_str}\n▣ Res: {quality}\n▣ Lang: {audio}\n<blockquote>▣ Link: {power}</blockquote></b>",
        f"<b>✨ {anime} ✨\n━━━━━━━━━━━━━━━\n💎 Ep: {ep_str}\n💎 Q: {quality}\n💎 A: {audio}\n<blockquote>💠 {power}</blockquote></b>",
        f"<b>🎶 {anime} 🎶\n\n🎵 Ep: {ep_str}\n🎵 Qual: {quality}\n🎵 Audio: {audio}\n<blockquote>🎧 {power}</blockquote></b>",
        f"<b>☩ {anime} ☩\n\n☩ Ep: {ep_str}\n☩ Qual: {quality}\n☩ Audio: {audio}\n<blockquote>☩ {power} ☩</blockquote></b>",
        f"<b>// {anime} //\n\n// Ep: {ep_str}\n// Res: {quality}\n// Lang: {audio}\n<blockquote>// {power} //</blockquote></b>",
        f"<b>🌌 {anime} 🌌\n━━━━━━━━━━━━━━━\n🌠 Ep: {ep_str}\n🌠 Quality: {quality}\n🌠 Audio: {audio}\n<blockquote>🪐 {power}</blockquote></b>",
        f"<b>🤖 {anime} 🤖\n\n⚙️ Episode: {ep_str}\n⚙️ Quality: {quality}\n⚙️ Audio: {audio}\n<blockquote>⚙️ Powered by {power}</blockquote></b>"
    ]
    
    try:
        idx = int(style_choice) - 1
        return styles[idx] if 0 <= idx < 30 else styles[0]
    except:
        return styles[0]

# --- COMMAND HANDLERS ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = "<b>🤖 Welcome to Anime Uploader Bot!</b>\n\n/usage - How to use\n/setstyle [1-30] - Set style\n/see_all - See all styles"
    await update.message.reply_text(welcome_text, parse_mode="HTML")

async def usage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    guide = "<b>📖 How to use:</b>\n\n1. Send videos\n2. Type /done\n3. Send: <code>Anime | Season | Quality | Audio | @Channel | StartEP</code>"
    await update.message.reply_text(guide, parse_mode="HTML")

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🆘 Admin: {ADMIN_HANDLE}")

async def setstyle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("❌ Use: /setstyle 1-30")
    val = context.args[0]
    user_styles[str(update.effective_user.id)] = int(val)
    save_styles(user_styles)
    await update.message.reply_text(f"✅ Style {val} set!")

async def mystyle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    style = user_styles.get(str(update.effective_user.id), 1)
    await update.message.reply_text(f"🎨 Current style: {style}")

async def preview(update: Update, context: ContextTypes.DEFAULT_TYPE):
    choice = user_styles.get(str(update.effective_user.id), 1)
    cap = get_caption("Solo Leveling", "01", 5, "1080p", "Hindi", "@MyChannel", choice)
    await update.message.reply_text(f"<b>Preview Style {choice}:</b>\n\n{cap}", parse_mode="HTML")

async def see_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔄 Sending styles...")
    for i in range(1, 31):
        cap = get_caption("Anime Name", "01", i, "720p", "Jap/Eng", "@Channel", i)
        await update.message.reply_text(f"<b>Style {i}:</b>\n\n{cap}", parse_mode="HTML")
        await asyncio.sleep(0.5)

async def thumb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["waiting_thumb"] = True
    await update.message.reply_text("📸 Send the photo now.")

async def show_thumb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    path = f"{THUMB_DIR}/{update.effective_user.id}.jpg"
    if os.path.exists(path):
        await update.message.reply_photo(photo=open(path, "rb"), caption="🖼️ Current thumbnail")
    else:
        await update.message.reply_text("❌ No thumbnail!")

async def del_thumb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    path = f"{THUMB_DIR}/{update.effective_user.id}.jpg"
    if os.path.exists(path):
        os.remove(path)
        await update.message.reply_text("🗑️ Deleted.")
    else:
        await update.message.reply_text("❌ Nothing to delete.")

# --- PROCESSING HANDLERS ---

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("waiting_thumb") and update.message.photo:
        file = await update.message.photo[-1].get_file()
        await file.download_to_drive(f"{THUMB_DIR}/{update.effective_user.id}.jpg")
        context.user_data["waiting_thumb"] = False
        return await update.message.reply_text("✅ Thumbnail Saved!")

    file = update.message.video or update.message.document
    if file:
        context.user_data.setdefault("videos", []).append(file.file_id)
        await update.message.reply_text(f"📥 Video {len(context.user_data['videos'])} Saved")

async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("videos"):
        return await update.message.reply_text("❌ Send videos first!")
    context.user_data["ask_details"] = True
    await update.message.reply_text("✅ Send details: <code>Anime | Season | Quality | Audio | @channel | StartEP</code>", parse_mode="HTML")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("ask_details"): return
    try:
        data = [x.strip() for x in update.message.text.split("|")]
        anime, season, quality, audio, power, start_ep = data
        videos = context.user_data.get("videos", [])
        user_id = str(update.effective_user.id)
        choice = user_styles.get(user_id, 1)
        
        await update.message.reply_text(f"🚀 Uploading {len(videos)} videos...")
        for i, vid in enumerate(videos):
            caption = get_caption(anime, season, int(start_ep) + i, quality, audio, power, choice)
            # Thumbnail check
            thumb_path = f"{THUMB_DIR}/{user_id}.jpg"
            if os.path.exists(thumb_path):
                await update.message.reply_video(video=vid, caption=caption, thumbnail=open(thumb_path, "rb"), parse_mode="HTML")
            else:
                await update.message.reply_video(video=vid, caption=caption, parse_mode="HTML")
            await asyncio.sleep(2)
        
        await update.message.reply_text("✅ Completed!")
        context.user_data.clear()
    except:
        await update.message.reply_text("❌ Error! Use: Anime | Sn | Qual | Audio | @ch | StartEP")

# --- MAIN ---
if __name__ == '__main__':
    keep_alive() # Render ke liye
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # Registering all your original commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("usage", usage))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("setstyle", setstyle))
    app.add_handler(CommandHandler("mystyle", mystyle))
    app.add_handler(CommandHandler("preview", preview))
    app.add_handler(CommandHandler("see_all", see_all))
    app.add_handler(CommandHandler("thumb", thumb))
    app.add_handler(CommandHandler("show_thumb", show_thumb))
    app.add_handler(CommandHandler("del_thumb", del_thumb))
    app.add_handler(CommandHandler("done", done))
    
    app.add_handler(MessageHandler(filters.VIDEO | filters.Document.ALL | filters.PHOTO, handle_video))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    print("⚡ Bot is Running...")
    app.run_polling()
