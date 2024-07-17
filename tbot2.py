import telebot
import requests

# Замените этот токен на ваш реальный токен бота
BOT_TOKEN = "7390852453:AAGGfnJ_YQgklQHOI8N-vXk_5t9odWL6bhU" 

# API-ключ для CoinMarketCap
COINMARKETCAP_API_KEY = "1d6d60cd-9e3c-4df9-9a07-65a4e254f95c"

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
  bot.reply_to(message, "Привет! 👋 Я могу показать тебе текущую цену криптовалют. \n Введите название криптовалюты (например, 'BTC' или 'ETH') для получения информации.")

@bot.message_handler(func=lambda message: True)
def get_crypto_price(message):
  crypto_symbol = message.text.upper()

  try:
    url = f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol={crypto_symbol}&CMC_PRO_API_KEY={COINMARKETCAP_API_KEY}"
    response = requests.get(url)
    response.raise_for_status()

    data = response.json()
    price = data["data"][crypto_symbol]["quote"]["USD"]["price"]

    bot.reply_to(message, f"Текущая цена {crypto_symbol}: ${price:.2f}")
  except requests.exceptions.RequestException as e:
    bot.reply_to(message, f"Ошибка: {e}")
  except KeyError:
    bot.reply_to(message, f"Не удалось найти криптовалюту с символом '{crypto_symbol}'. Пожалуйста, попробуйте другое название.")

# Запускаем бота
bot.polling()