import telebot
import requests
from xml.etree import ElementTree as Etree
import re

TOKEN = '7697672080:AAGjag1CuzfyFffw2pGMcBSfrhwhrtkTh10'
bot = telebot.TeleBot(TOKEN)


# Получаем курсы доллара и евро с сайта ЦБ РФ
def get_rates():
    url = 'https://www.cbr.ru/scripts/XML_daily.asp'
    result = requests.get(url)
    response = result.content
    tree = Etree.fromstring(response)

    usd, eur = None, None

    for cur in tree.findall('Valute'):
        code = cur.find('CharCode').text
        if code == 'USD':
            usd = cur.find('Value').text
        elif code == 'EUR':
            eur = cur.find('Value').text

        if usd and eur:
            break

    return usd, eur


def valid_name_check(n):
    if len(n) > 20:
        return False
    if not re.match(r"^[А-Яа-яA-Za-z]+$", n):
        return False
    return True


@bot.message_handler(commands=['start'])
def welcome(msg):
    bot.reply_to(msg, "Добрый день. Как вас зовут? ")


@bot.message_handler(func=lambda message: True)
def askname(m):
    user_name = m.text.strip()
    if valid_name_check(user_name):
        usd, eur = get_rates()
        if usd and eur:
            reply = (f"Рад знакомству, {user_name} ! Курс валют:\n"  
                     f"- Доллар США: {usd} руб.\n"
                     f"- Евро: {eur} руб.")
        else:
            reply = "Не удалось получить курс валют. Попробуйте позже."
    else:
        reply = "Пожалуйста, введите корректное имя (до 20 символов, только буквы)."

    bot.reply_to(m, reply)


bot.polling()
