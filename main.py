
import requests
import time
import telebot
from config import BOT_TOKEN, CHAT_ID, OPENSEA_API_KEY

bot = telebot.TeleBot(BOT_TOKEN)

OPENSEA_URL = "https://api.opensea.io/api/v2/orders/eth/seaport/listings"

def get_live_mints():
    headers = {
        "accept": "application/json",
        "X-API-KEY": OPENSEA_API_KEY
    }

    params = {
        "limit": 5
    }

    response = requests.get(OPENSEA_URL, headers=headers, params=params)
    data = response.json()

    mints = []
    if "orders" in data:
        for order in data["orders"]:
            name = order.get("maker", {}).get("address", "Unknown")
            price = order.get("current_price", "N/A")
            link = order.get("order_hash", "")

            mints.append({
                "name": name,
                "price": price,
                "link": f"https://opensea.io/assets/{link}"
            })

    return mints


def send_updates():
    mints = get_live_mints()
    if not mints:
        bot.send_message(CHAT_ID, "لا يوجد Mint شغال حالياً على Opensea ⌛️")
        return

    for mint in mints:
        text = f"🚀 **Mint Live Detected!**\n\n👤 Name: {mint['name']}\n💰 Price: {mint['price']}\n🔗 Link: {mint['link']}"
        bot.send_message(CHAT_ID, text, parse_mode="Markdown")


@bot.message_handler(commands=["check"])
def check_command(message):
    send_updates()


bot.send_message(CHAT_ID, "✅ Bot Started and Monitoring Opensea Drops...")
bot.infinity_polling()
