import re
from datetime import datetime

import requests
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

from configs.variables import ERROR_GROUP, ERROR_BOT
from handlers.conversation_handlers import HOME, CONFIRM
from keyboards import client_keyboards


def format_phone_number(phone: str) -> str:
    """
    Ensures the phone number is in the format +998946104316.
    - If missing '+', it is added.
    - Must be exactly 12 digits after the country code.
    - Must start with '998'.
    """
    phone = phone.strip()
    if not phone.startswith("+"):
        phone = "+" + phone

    pattern = r"^\+998\d{9}$"
    return phone if re.fullmatch(pattern, phone) else None



def is_valid_date(date_str):
    pattern = r"^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[0-2])\.(\d{4})$"
    return bool(re.match(pattern, date_str))



def error_sender(error_message):
    payload = {
        "chat_id": ERROR_GROUP,
        "text": error_message,
        "parse_mode": "HTML"
    }

    # Send the request to send the inline keyboard message
    response = requests.post(
        url=f"https://api.telegram.org/bot{ERROR_BOT}/sendMessage",
        json=payload
    )
    # Check the response status
    if response.status_code == 200:
        return response
    else:
        print("Response text: ", response.text)
        return None



async def pre_confirmation_process(update: Update, context: ContextTypes.DEFAULT_TYPE):
    request = context.user_data["request_details"]
    request_sum = format(int(request['sum']), ',').replace(',', ' ')
    if request.get('exchange_rate', None) is not None:
        requested_currency = format((request['sum'] / request['exchange_rate']), ',').replace(',', ' ')
    else:
        requested_currency = request_sum

    request_text = (
        f"📅 Дата заявки: {datetime.now().date().strftime('%d.%m.%Y')}\n"
        f"📍 Отдел: {request['department_name']}\n"
        f"👤 Заявитель: {context.user_data['client']['fullname']}\n"
        f"📞 Номер заявителя: {context.user_data['client']['phone']}\n"
        f"🛒 Заказчик: {request['buyer_name']}\n"
        f"💰 Тип затраты: {request['expense_type_name']}\n"
        f"🏢 Поставщик: {request['supplier_name']}\n\n"
        f"💎 Стоимость: <b>{request_sum} сум</b>\n"
        f"💎 Запрошенная сумма в валюте: <b>{requested_currency}</b>\n"
        f"💵 Валюта: {request['currency']}\n"
        f"📈 Курс валюты: {request['exchange_rate']}\n"
        f"💳 Тип оплаты: {request['payment_type_name']}\n"
        f"💳 Карта перевода: {request.get('payment_card', '')}\n"
        f"📜 № Заявки в SAP: {request['sap_code']}\n"
        f"🕓 Дата оплаты: {request['payment_time'].strftime('%d.%m.%Y')}\n"
        f"💸 Фирма-плательщик: {request.get('payer_company_name', '')}\n\n"
        f"📝 Комментарии: {request['description']}"
    )
    city_name = context.user_data.get("request_details").get("city")
    trip_days = context.user_data.get("request_details").get("trip_days")
    if city_name and trip_days:
        request_text += (f"\n✈️ Коммандировка по направлению: {city_name}"
                         f"\n⏳ Количество дней: {trip_days}")
    budget_balance = context.user_data["request_details"]["budget_balance"]
    context.user_data["request_details"]["send_ceo"] = False

    if float(context.user_data["request_details"]["sum"]) > budget_balance and context.user_data["request_details"][
        "over_budget"] == False:
        await update.message.reply_text(
            text="К сожалению, на балансе бюджета недостаточно средств для покрытия запрошенной суммы."
        )
        keyboard = (await client_keyboards.home_keyboard())
        await update.message.reply_text(
            text=keyboard['text'],
            reply_markup=keyboard['markup']
        )
        return HOME

    else:
        if float(context.user_data["request_details"]["sum"]) > budget_balance and \
                context.user_data["request_details"]["over_budget"] == True:
            context.user_data["request_details"]["send_ceo"] = True

        await update.message.reply_text(
            text='Проверьте свою заявку ещё раз, если всё правильно, подтвердите её.'
        )
        await update.message.reply_text(
            text=request_text,
            reply_markup=ReplyKeyboardMarkup(keyboard=[["Назад ⬅️"], ["Подтвердить"]], resize_keyboard=True),
            parse_mode='HTML'
        )
        return CONFIRM