from telegram import ReplyKeyboardMarkup, KeyboardButton
from utils.api_requests import api_routes
from datetime import datetime, date
import calendar


async def home_keyboard():
    reply_keyboard = [
        [
            KeyboardButton(text="Подать заявку"),
            KeyboardButton(text="Мои заявки")
        ],
        [
            KeyboardButton(text="Регламент подачи")
        ]
    ]
    text = "Главная страница"
    reply_markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    data_dict = {'text': text, 'markup': reply_markup}
    return data_dict


async def departments_keyboard():
    departments = api_routes.get_departments()["items"]
    departments = [department["name"] for department in departments]
    reply_keyboard = [["Назад ⬅️"]]
    for i in range(0, len(departments), 3):
        reply_keyboard.append(departments[i: i+3])

    text = "Укажите отдел, откуда подаёте заявку"
    reply_markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=True)
    data_dict = {'text': text, 'markup': reply_markup}
    return data_dict


async def expense_types_keyboard(department_id):
    # Get today's date
    today = date.today()

    # First day of current month
    first_day = today.replace(day=1)
    # first_day = datetime(year=2025, month=5, day=1).date()

    # Last day of current month
    last_day = today.replace(day=calendar.monthrange(today.year, today.month)[1])
    # last_day = datetime(year=2025, month=5, day=31).date()

    objs = api_routes.get_expense_types(department_id=department_id, start_date=first_day, finish_date=last_day)
    # objs = api_routes.get_expense_types()
    # print(objs)
    # objs = [obj["name"] for obj in objs]
    objs = [obj["expense_type"]["name"] for obj in objs]
    reply_keyboard = [["Назад ⬅️"]]
    for i in range(0, len(objs), 3):
        reply_keyboard.append(objs[i: i+3])

    if objs:
        text = "Укажите тип затраты"
    else:
        text = "Бюджет вашего отдела пустой !\nСвяжитесь с финансовым отделом."
    reply_markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=True)
    data_dict = {'text': text, 'markup': reply_markup}
    return data_dict


async def buyers_keyboard():
    objs = api_routes.get_buyers()
    objs = [obj["name"] for obj in objs]
    reply_keyboard = [["Назад ⬅️"]]
    for i in range(0, len(objs), 3):
        reply_keyboard.append(objs[i: i+3])

    text = "Укажите Закупщика"
    reply_markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    data_dict = {'text': text, 'markup': reply_markup}
    return data_dict


async def suppliers_keyboard():
    objs = api_routes.get_suppliers()
    objs = [obj["name"] for obj in objs]
    reply_keyboard = [["Назад ⬅️"]]
    for i in range(0, len(objs), 3):
        reply_keyboard.append(objs[i: i+3])

    text = "Укажите поставщика"
    reply_markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    data_dict = {'text': text, 'markup': reply_markup}
    return data_dict


async def payment_types_keyboard():
    objs = api_routes.get_payment_types()
    objs = [obj["name"] for obj in objs]
    reply_keyboard = [["Назад ⬅️"]]
    for i in range(0, len(objs), 3):
        reply_keyboard.append(objs[i: i+3])

    text = "Выберите тип оплаты"
    reply_markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=True)
    data_dict = {'text': text, 'markup': reply_markup}
    return data_dict


async def currency_keyboard():
    currencies = ["Сум", "Доллар", "Евро", "Тенге", "Фунт", "Рубль", "Другое"]
    reply_keyboard = [["Назад ⬅️"]]
    for i in range(0, len(currencies), 3):
        reply_keyboard.append(currencies[i: i+3])

    text = "Выберите валюту"
    reply_markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=True)
    data_dict = {'text': text, 'markup': reply_markup}
    return data_dict


async def payer_companies_keyboard():
    response = api_routes.get_payer_companies()
    objs = response.json()['items']
    objs = [obj["name"] for obj in objs]
    reply_keyboard = [["Назад ⬅️"]]
    for i in range(0, len(objs), 3):
        reply_keyboard.append(objs[i: i + 3])

    text = 'Выбрите плательщика (фирму)'
    reply_markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=True)
    data_dict = {'text': text, 'markup': reply_markup}
    return data_dict
