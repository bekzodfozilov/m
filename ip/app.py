from telegram import Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import requests

# Функция для получения геопозиции по IP-адресу
def get_location_by_ip(ip):
    try:
        response = requests.get(f'http://ip-api.com/json/{ip}')
        data = response.json()
        if data['status'] == 'success':
            return {
                'city': data['city'],
                'region': data['regionName'],
                'country': data['country'],
                'latitude': data['lat'],
                'longitude': data['lon'],
            }
        else:
            return None
    except Exception as e:
        print(f'Error getting location by IP: {e}')
        return None

# Обработчик команды /ip
def ip_command(update, context):
    if len(context.args) == 0:
        update.message.reply_text("Please provide an IP address.")
        return

    ip = context.args[0]
    location = get_location_by_ip(ip)
    if location:
        message = f"Location for IP {ip}:\nCity: {location['city']}\nRegion: {location['region']}\nCountry: {location['country']}\nLatitude: {location['latitude']}\nLongitude: {location['longitude']}"
        update.message.reply_text(message)
    else:
        update.message.reply_text("Failed to retrieve location for the provided IP address.")

# Обработчик текстовых сообщений
def text_message(update, context):
    update.message.reply_text("To use this bot, send an IP address.")

def main():
    # Замените 'YOUR_BOT_TOKEN' на токен вашего бота
    bot_token = '6968895449:AAHWOFy13ul5omGZ6ejCMZS3EeANu3D8OsU'
    bot = Bot(token=bot_token)
    updater = Updater(bot=bot, use_context=True)

    # Получаем диспетчер для регистрации обработчиков
    dispatcher = updater.dispatcher

    # Регистрация обработчиков команд
    dispatcher.add_handler(CommandHandler("ip", ip_command))

    # Регистрация обработчика текстовых сообщений
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, text_message))

    # Запуск бота
    updater.start_polling()

    # Бот работает до принудительной остановки
    updater.idle()

if __name__ == '__main__':
    main()
