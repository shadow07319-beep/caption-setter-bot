import os
import json
import asyncio
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# --- WEB SERVER FOR RENDER ---
flask_app = Flask('')

@flask_app.route('/')
def home():
    return "Bot is running!"

def run_web():
    # Render provides a PORT environment variable automatically
    port = int(os.environ.get("PORT", 8080))
    flask_app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_web)
    t.daemon = True
    t.start()

# --- CONFIGURATION ---
# Use Environment Variables on Render Dashboard for BOT_TOKEN
BOT_TOKEN = os.environ.get("BOT_TOKEN") 
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

# --- CAPTION ENGINE (ALL 30 STYLES PRESERVED) ---
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

# --- HANDLERS (ALL COMMANDS PRESERVED) ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("<b>🤖 Welcome! Bot is Live.</b>\n/usage to start.", parse_mode="HTML")

async def usage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    guide = "<b>📖 How to use:</b>\n1. Send videos.\n2. Send /done.\n3. Send details: <code>Anime | Sn | Qual | Audio | @ch | StartEp</code>"
    await update.message.reply_text(guide, parse_mode="HTML")

async def setstyle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: return await update.message.reply_text("❌ Use: /setstyle 1-30")
    user_styles[str(update.effective_user.id)] = int(context.args[0])
    save_styles(user_styles)
    await update.message.reply_text(f"✅ Style {context.args[0]} set!")

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("waiting_thumb"):
        if update.message.photo:
            file = await update.message.photo[-1].get_file()
            await file.download_to_drive(f"{THUMB_DIR}/{update.effective_user.id}.jpg")
            context.user_data["waiting_thumb"] = False
            return await update.message.reply_text("✅ Thumbnail saved!")
    file = update.message.video or update.message.document
    if file:
        context.user_data.setdefault("videos", []).append(file.file_id)
        await update.message.reply_text(f"📥 Saved ({len(context.user_data['videos'])})")

async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("videos"): return await update.message.reply_text("❌ No videos!")
    context.user_data["ask_details"] = True
    await update.message.reply_text("✅ Send details in format:\n<code>Anime | Sn | Qual | Audio | @ch | StartEp</code>", parse_mode="HTML")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("ask_details"): return
    try:
        data = [x.strip() for x in update.message.text.split("|")]
        anime, sn, qual, audio, power, start_ep = data
        videos = context.user_data.get("videos", [])
        choice = user_styles.get(str(update.effective_user.id), 1)
        
        await update.message.reply_text(f"🚀 Uploading {len(videos)} videos...")
        for i, vid in enumerate(videos):
            cap = get_caption(anime, sn, int(start_ep)+i, qual, audio, power, choice)
            await update.message.reply_video(video=vid, caption=cap, parse_mode="HTML")
            await asyncio.sleep(1)
        await update.message.reply_text("✅ All Done!")
        context.user_data.clear()
    except:
        await update.message.reply_text("❌ Error! Check format.")

# --- RUN BOT ---
if __name__ == '__main__':
    keep_alive()
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("usage", usage))
    app.add_handler(CommandHandler("setstyle", setstyle))
    app.add_handler(CommandHandler("done", done))
    app.add_handler(MessageHandler(filters.VIDEO | filters.Document.ALL | filters.PHOTO, handle_video))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    print("⚡ Bot is Running...")
    app.run_polling()
