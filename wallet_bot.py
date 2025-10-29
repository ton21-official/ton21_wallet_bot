import telebot
import requests
from config import *

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    text = (
        "💎 <b>Ton21 Wallet</b> — управление вашим $T21.\n\n"
        "💰 Купить $T21\n"
        "💎 Проверить баланс\n"
        "🔄 Обменять\n"
        "🏠 Домой — в Ton21 Portal"
    )
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("💰 Buy $T21", callback_data="buy"))
    markup.add(telebot.types.InlineKeyboardButton("💎 Wallet", callback_data="balance"))
    markup.add(telebot.types.InlineKeyboardButton("🔄 Swap / Exchange", callback_data="swap"))
    markup.add(telebot.types.InlineKeyboardButton("🏠 Home", url=PORTAL_URL))
    bot.send_message(message.chat.id, text, parse_mode="HTML", reply_markup=markup)

@bot.callback_query_handler(func=lambda c: True)
def callback(c):
    if c.data == "buy":
        bot.send_message(c.message.chat.id,
            f"💰 Отправь TON на кошелёк:\n<code>{TON_WALLET}</code>\n\n⚙️ 1 TON = 10 T21",
            parse_mode="HTML")
    elif c.data == "balance":
        bot.send_message(c.message.chat.id, "⏳ Проверяем баланс кошелька…")
        try:
            r = requests.get(
                f"https://toncenter.com/api/v2/getTransactions?address={TON_WALLET}&limit=1&api_key={TONCENTER_API_KEY}"
            )
            tx = r.json()['result'][0]
            amount = int(tx['in_msg']['value']) / 1e9
            bot.send_message(c.message.chat.id, f"💎 Баланс: {amount:.3f} TON")
        except Exception:
            bot.send_message(c.message.chat.id, "⚠️ Ошибка при получении данных.")
    elif c.data == "swap":
        bot.send_message(c.message.chat.id, "🔄 DeDust.io или STON.fi — для обмена TON/T21")

bot.polling(none_stop=True)
