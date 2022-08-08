import telebot
from config import TOKEN, CURRENCIES
from extensions import CryptoConverter, APIException

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'To get started, enter the command in the following format: \n<currency from> <currency to> <amount>\nTo see the list of available currencies type: /currencies'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def get_values(message: telebot.types.Message):
    text = 'Available currencies:'

    for currency in CURRENCIES.keys():
        text = '\n'.join((text, currency))

    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) > 3:
            raise APIException('Too many parameters given.')

        if len(values) < 3:
            raise APIException('Too few parameters given.')

        base, quote, amount = values

        price = CryptoConverter.convert(base, quote, amount)

        text = f'{amount} {base} in {quote}  - {price}'
        bot.reply_to(message, text)
    except APIException as e:
        bot.reply_to(message, f'User error: {e}')
    except Exception as e:
        bot.reply_to(message, f'System error: {e}')


bot.polling(none_stop=True)