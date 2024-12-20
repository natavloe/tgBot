import logging  # Импортируем модуль для ведения логов
import requests  # Импортируем модуль для отправки HTTP-запросов
from aiogram import Bot, Dispatcher, executor, types  # Импортируем необходимые компоненты из библиотеки aiogram

API_TOKEN = '7631759260:AAHlSvtDKVLSFN713e-3uPKSbYx0Lei081s'  # Токен вашего бота Telegram
WEATHER_API_KEY = '53adf836e50f19b6cab51be4dd465294'  # Ваш ключ API для OpenWeatherMap

logging.basicConfig(level=logging.INFO)  # Настраиваем уровень логгирования

bot = Bot(token=API_TOKEN)  # Создаём объект бота
dp = Dispatcher(bot)  # Создаём диспетчер для обработки сообщений


def get_weather(city: str) -> str:  # Функция для получения погоды по названию города
    base_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru'  # Формируем URL для запроса к API OpenWeatherMap
    response = requests.get(base_url)  # Отправляем запрос
    data = response.json()  # Преобразуем ответ в формат JSON
    if data['cod'] != 200:  # Проверяем код ответа (200 означает успех)
        return "Не удалось получить данные о погоде."  # Если код не 200, возвращаем сообщение об ошибке

    weather_description = data['weather'][0]['description']  # Извлекаем описание погоды
    temperature = int(data['main']['temp'])  # Извлекаем температуру
    feels_like = int(data['main']['feels_like'])  # Извлекаем ощущение температуры
    humidity = int(data['main']['humidity'])  # Извлекаем влажность

    return (f"Погода в {city}:\n"  # Формируем строку с информацией о погоде
            f"Температура: {temperature}°C\n"
            f"Ощущается как: {feels_like}°C\n"
            f"Описание: {weather_description}\n"
            f"Влажность: {humidity}%")


@dp.message_handler(commands=['start'])  # Декоратор для обработки команд '/start'
async def send_welcome(message: types.Message):  # Функция-обработчик для команды '/start'
    await message.reply("Нажмите на вторую команду чтобы узнать погоду в Самаре")  # Ответ на команду '/start'


@dp.message_handler(commands=['weather'])  # Декоратор для обработки команд '/weather'
async def send_weather(message: types.Message):  # Функция-обработчик для команды '/weather'
    await message.reply(get_weather('Samara'))  # Отправляем пользователю информацию о погоде в Самаре


@dp.message_handler()  # Декоратор для обработки всех остальных сообщений
async def echo(message: types.Message):  # Функция-обработчик для всех других сообщений
    await message.answer("я не знаю такой команды")  # Ответ на неизвестные команды


if __name__ == '__main__':  # Основной блок программы
    executor.start_polling(dp, skip_updates=True)  # Запускаем бот и начинаем обработку сообщений