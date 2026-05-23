#@cantarellabots
import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.environ.get("API_ID", 39407537))
API_HASH = os.environ.get("API_HASH", "5bd2e83dd1227da3f38c966d1d46d9ae")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8604957606:AAHUao26G25NjgDgEsoiYNWPDvtl6daAn9s")

SET_INTERVAL = int(os.environ.get("SET_INTERVAL", 60))  # in seconds, default 1 hour
TARGET_CHAT_ID = os.environ.get("TARGET_CHAT_ID", "")
MAIN_CHANNEL = os.environ.get("MAIN_CHANNEL", "-1003864140941") # Change as needed
LOG_CHANNEL = os.environ.get("LOG_CHANNEL", "-1003751522913")
MONGO_URL = os.environ.get("MONGO_URL", "mongodb+srv://ADMIN98:Irfan987065@cluster0.eqcgcaq.mongodb.net/?appName=Cluster0")
MONGO_NAME = os.environ.get("MONGO_NAME", "Sasuke")
OWNER_ID = int(os.environ.get("OWNER_ID", "8180269769"))
ADMIN_URL = os.environ.get("ADMIN_URL", "@SubaruXnatsuki")
BOT_USERNAME = os.environ.get("BOT_USERNAME", "@Sasuke_Rage_Bot")
FSUB_PIC = os.environ.get("FSUB_PIC", "https://files.catbox.moe/bli70r.jpg")
FSUB_LINK_EXPIRY = int(os.environ.get("FSUB_LINK_EXPIRY", 600))
START_PIC =os.environ.get("START_PIC", "https://ibb.co/mCDb1CxR")

# ─── Filename & Caption Formats ───
FORMAT = os.environ.get("FORMAT", "S{season}-{episode}] {title} [{quality}] [{audio}] @Anime_Rage_official.mkv")
CAPTION = os.environ.get("CAPTION", "[{FORMAT}]")

# ─── Progress Bar Settings ───
PROGRESS_BAR = os.environ.get("PROGRESS_BAR", """
<blockquote> {bar} </blockquote>
<blockquote>📁 <b>{title}</b>
⚡ Speed: {speed}
📦 {current} / {total}</blockquote>
""")

# ─── Response Images ───
# Rotating anime images sent with every bot reply. Add as many as you like.
RESPONSE_IMAGES = [
    "https://files.catbox.moe/5oonsm.jpg",
    "https://files.catbox.moe/9ufgme.jpg",
    "https://files.catbox.moe/4b8jvw.jpg",
    "https://files.catbox.moe/bli70r.jpg",
    "https://files.catbox.moe/uce0lw.jpg",
    "https://files.catbox.moe/is7q4q.jpg"
]
