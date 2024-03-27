import telebot
import requests
import json


bot = telebot.TeleBot('YOUR_BOT_TOKEN')
API_KEY = 'YOUR_API_KEY'   # API ключ для OpenWeatherMap


@bot.message_handler(commands=['start']) # отслеживаем команду /start  и отправляем приветственное сообщение
def start(message):
    bot.send_message(message.chat.id,
                     f'Привет, {message.from_user.first_name} {message.from_user.last_name}! Напиши название города 😇')


@bot.message_handler(content_types=['text'])  # отслеживаем текстовые сообщения
def get_weather(message):
    city = message.text.strip().lower()    # сохраняем введеный текст в переменую , убираем пробелы в начале и в конце и преобразуем в нижний регистр
    try: # проверяем, есть ли введенное название города
        res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric') # создаём запрос к OpenWeatherMap
        if res.status_code == 200:
            data = res.json()
            temp = data["main"]["temp"]
            weather = data["weather"][0]["description"]

            response_message = f"""В городе {city.title()} сейчас {temp} градусов, 
            скорость ветра: {data["wind"]["speed"]} м/с,
            относительная влажность: {data["main"]["humidity"]}%, 
            атмосферное давление: {data["main"]["pressure"]} мм"""

            bot.reply_to(message, response_message) # отправляем сообщение в чат пользователю с указанным текстом

            if weather == 'clear sky':
                image = 'photo1.jpg'
            elif weather in ['few clouds', 'broken clouds', 'overcast clouds', 'fog','scattered clouds']:
                image = 'photo2.png'
            elif weather in ['light rain', 'moderate rain', 'heavy rain']:
                image = 'photo3.png'
            else:
                image = 'photo3.png'
            file = open(image, 'rb')
            bot.send_photo(message.chat.id, file) # отправляем фото в чат пользователю с указанным текстом



        else:
            bot.send_message(message.chat.id, 'К сожалению, город не найден 😢 Попробуйте ввести другое название.')
    except Exception as e:
        bot.send_message(message.chat.id, 'Произошла ошибка при обработке вашего запроса.')


bot.polling(none_stop=True)