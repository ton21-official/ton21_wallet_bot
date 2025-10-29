# main.py — Ton21 Wallet Bot (Replit-ready)
import os
import logging
import threading
from typing import Optional

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ── (1) .env support for local runs ─────────────────────────────────────────────
try:
    # load .env only if file exists (local dev); on Replit use Secrets
    if os.path.isfile(".env"):
        from dotenv import load_dotenv  # type: ignore
        load_dotenv()
except Exception:
    pass

def env(name: str, default: Optional[str] = None) -> Optional[str]:
    v = os.environ.get(name)
    return v if (v is not None and v.strip() != "") else default

# ── (2) Required/optional settings ─────────────────────────────────────────────
BOT_TOKEN = env("BOT_TOKEN")  # set in Replit → Tools → Secrets
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is missing. Add it in Replit → Tools → Secrets.")

# Optional links (set in Secrets if хочешь другие адреса)
PORTAL_URL = env("PORTAL_URL", "https://t.me/Ton21PortalBot")
BUY_URL    = env("BUY_URL",    PORTAL_URL)          # куда вести кнопку Buy
WALLET_URL = env("WALLET_URL", PORTAL_URL)          # открыть кошелёк/мини-приложение
SWAP_URL   = env("SWAP_URL",   PORTAL_URL)          # обмен/биржа

# (необязательные, для будущих фич)
TON_WALLET = env("TON_WALLET")            # адрес Tonkeeper
TONCENTER_API_KEY = env("TONCENTER_API_KEY")

# ── (3) Logging ────────────────────────────────────────────────────────────────
logging.basicConfig(
    format="%(asctime)s — %(levelname)s — %(name)s — %(message)s",
    level=logging.INFO,
)
log = logging.getLogger("t21_wallet_bot")

# ── (4) UI ─────────────────────────────────────────────────────────────────────
def main_menu() -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton("💰 Buy $T21", url=BUY_URL)],
        [InlineKeyboardButton("💎 Wallet", url=WALLET_URL)],
        [InlineKeyboardButton("🔁 Swap / Exchange", url=SWAP_URL)],
        [InlineKeyboardButton("🏠 Home", url=PORTAL_URL)],
    ]
    return InlineKeyboardMarkup(rows)

WELCOME_TEXT = (
    "💎 <b>Ton21 Wallet</b> — your decentralized wallet for $T21.\n\n"
    "• Buy $T21 directly with TON\n"
    "• Open your wallet\n"
    "• Swap or exchange your tokens\n\n"
    "🚀 Power up your journey with Ton21!"
)

# ── (5) Handlers ───────────────────────────────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_html(WELCOME_TEXT, reply_markup=main_menu())

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Use /start to open the menu. For more: " + PORTAL_URL)

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("I only understand /start and /help 😉")

# ── (6) Keep-alive web server for Replit (optional but useful) ────────────────
def run_keepalive():
    try:
        from flask import Flask
        app = Flask(__name__)

        @app.get("/")
        def index():
            return "Ton21 Wallet Bot is alive and running 24/7!"

        port = int(env("PORT", "8080"))
        app.run(host="0.0.0.0", port=port)
    except Exception as e:
        log.warning("Keep-alive server not started: %s", e)

# ── (7) Bootstrap ──────────────────────────────────────────────────────────────
def run():
    # Start tiny web server in a side thread (so Replit keeps the repl awake)
    threading.Thread(target=run_keepalive, daemon=True).start()

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CallbackQueryHandler(lambda *_: None))  # placeholder
    app.add_handler(CommandHandler(None, unknown))          # fallback

    log.info("Starting Ton21 Wallet Bot…")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    run()
