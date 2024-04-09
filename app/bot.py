import datetime

import telebot
from telebot import types
import requests

from config_bot import TELEGRAM_TOKEN, API_URL

bot = telebot.TeleBot(TELEGRAM_TOKEN)


@bot.message_handler(content_types=['text'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    button_sales_get_report = types.InlineKeyboardButton(
        'Получить отчет',
        callback_data='get_report')
    button_sale_append = types.InlineKeyboardButton(
        'Внести данные',
        callback_data='sale_append')
    markup.add(button_sales_get_report, button_sale_append)
    bot.send_message(
        message.chat.id,
        "Выберите действие:",
        reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'get_report':
        msg = bot.send_message(
            call.message.chat.id,
            "Введите период в формате:\n"
            "DD.MM.YYYY-DD.MM.YYYY\n\n"
            "Пример:\n"
            "01.04.2024-02.04.2024")
        bot.register_next_step_handler(msg, process_sales_get_report)
    elif call.data == 'sale_append':
        msg = bot.send_message(
            call.message.chat.id,
            "Введите данные в формате:\n"
            "Дата, Название продукта, Количество, Цена\n\n"
            "Пример:\n"
            "01.04.2024, Пицца, 1.5, 150.99")
        bot.register_next_step_handler(msg, process_sale_append)


def process_sales_get_report(message):
    dates = message.text
    if len(dates) == 21:  # длина строки формата 01.01.1990-01.01.1990
        start_date = datetime.datetime.strptime(
            dates.split("-")[0], "%d.%m.%Y")
        end_date = datetime.datetime.strptime(dates.split("-")[1], "%d.%m.%Y")
        response = requests.get(
            f"{API_URL}/sales/?start_date={start_date}&end_date={end_date}")
        data = response.json()
        if len(data) == 0:
            bot.reply_to(
                message,
                "Данных за указанный период не найдено. Попробуйте увеличить диапазон.")
            start(message)
            return
        text =  " Дата      | Продукт                        | Кол-во   | Цена\n"
        text += "-----------|--------------------------------|----------|----------\n"
        for item in data:
            sale_date = datetime.datetime.strptime(
                item['sale_date'], '%Y-%m-%d').strftime('%d.%m.%Y')
            product_name = item['product_name']
            if len(product_name) > 30:
                # обрезаем слишком длинные названия
                product_name = product_name[:27] + "..."
            quantity = item['quantity']
            price = item['price']
            text += f"{sale_date} | {product_name:<30} | {quantity:<8} | {price:<8}\n"
        bot.reply_to(
            message,
            "Отчет о продажах:\n"
            f"```\n{text}\n```",
            parse_mode='MarkdownV2')
    else:
        bot.reply_to(message, "Неверный формат данных. Попробуйте еще раз.")
    start(message)


def process_sale_append(message):
    data = message.text.split(',')
    if len(data) == 4:
        sale_date, product_name, quantity, price = data
        sale_date = str(datetime.datetime.strptime(sale_date, "%d.%m.%Y"))
        product_name = product_name.strip()
        quantity = round(float(quantity), 3)
        price = round(float(price), 2)
        response = requests.post(
            f"{API_URL}/sales/create",
            json={
                "sale_date": sale_date,
                "product_name": product_name,
                "quantity": quantity,
                "price": price})
        # bot.reply_to(message, f"{response.status_code}")  # debug
        bot.reply_to(message, "Данные о продаже успешно добавлены.")
    else:
        bot.reply_to(message, "Неверный формат данных. Попробуйте еще раз.")
    start(message)
