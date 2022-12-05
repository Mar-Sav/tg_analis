import requests
import datetime
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)

kb = InlineKeyboardMarkup(row_width=1)
Button = InlineKeyboardButton(text='Температура', callback_data='temp')
Button2 = InlineKeyboardButton(text='Влажность', callback_data='hum')
Button3 = InlineKeyboardButton(text='Давление', callback_data='press')
Button4 = InlineKeyboardButton(text='Ветер', callback_data='wind')
Button5 = InlineKeyboardButton(text='Световой день', callback_data='sun')
Button6 = InlineKeyboardButton(text='Назад', callback_data='back2')
kb.add(Button, Button2, Button3,Button4, Button5, Button6)

kb_back = InlineKeyboardMarkup(row_width=1)
back = InlineKeyboardButton(text='Назад', callback_data='back')
kb_back.add(back)

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply('Привет, напиши мне название города, и я пришлю погоду')

@dp.message_handler()
async def get_weather(message: types.Message):
    code_to_smile = {
        'Clear': "Ясно \U00002600",
        'Clouds': 'Облачно \U00002601',
        'Rain': 'Дождь \U00002614',
        'Drizzle': 'Дождь \U00002614',
        'Thunderstorm': 'Гроза \U000026A1',
        'Snow': 'Снег \U0001F328',
        'Mist': 'Туман \U0001F32B'
    }

    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric")
        data = r.json()
        global city
        global cur_weather
        global wd
        global humidity
        global pressure
        global wind
        global sunrise_timestamp
        global sunset_timestamp
        city = data['name']
        cur_weather = data['main']['temp']

        weather_description = data['weather'][0]['main']
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = 'Посмотри в окно'

        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind = data['wind']['speed']
        sunrise_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunset'])

        await bot.send_message(message.chat.id, "Город введен верно, что хотите посмотреть:", reply_markup=kb)

    except:
        await message.reply("Проверьте название города")


@dp.callback_query_handler(text="temp")
async def temp(message: types.Message):
    await bot.send_message(message.from_user.id, f"Погода в городе: {city}\n Температура равна: {cur_weather}C \n {wd}\n ", reply_markup=kb_back)


@dp.callback_query_handler(text="hum")
async def temp(message: types.Message):
    await bot.send_message(message.from_user.id, f"Погода в городе: {city}\n Влажность равна: {humidity}%\n", reply_markup=kb_back)


@dp.callback_query_handler(text="press")
async def temp(message: types.Message):
    await bot.send_message(message.from_user.id, f"Погода в городе: {city}\n Давление равно: {pressure}мм.рт.ст.\n", reply_markup=kb_back)


@dp.callback_query_handler(text="wind")
async def temp(message: types.Message):
    await bot.send_message(message.from_user.id, f"Погода в городе: {city}\n Ветер равен: {wind} м/c\n", reply_markup=kb_back)


@dp.callback_query_handler(text="sun")
async def temp(message: types.Message):
    await bot.send_message(message.from_user.id, f"Погода в городе: {city}\n Восход солнца : {sunrise_timestamp}\n "
                                f"Заход солнца: {sunset_timestamp}\n", reply_markup=kb_back)

@dp.callback_query_handler(text="back")
async def temp(message: types.Message):
    await bot.send_message(message.from_user.id, f"Что хотите узнать:", reply_markup=kb)


@dp.callback_query_handler(text="back2")
async def temp(message: types.Message):
    await bot.send_message(message.from_user.id, 'Напиши мне название города, и я пришлю погоду')


if __name__ == '__main__':
    executor.start_polling(dp)