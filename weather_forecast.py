#импорт необходимых библиотек
import time
import Adafruit_SSD1306
import requests

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

#конфигурация портов Raspberry Pi
RST = 24

#128x64 дисплей с поддержкой I2C
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

#вставьте ваш уникальный OpenWeatherMap.org URL  
open_weather_map_url = 'http://api.openweathermap.org/data/2.5/weather?q=Porto,PT&APPID=88982278ea0a426562a08fce9bb1bb3d'

#инициализация дисплея
disp.begin()

while True:
    #очистка дисплея
    disp.clear()
    disp.display()

    #создание пустого изображения для вывода
    #проверьте, что создаете изображение в режиме «1» для 1-битного цвета
    width = disp.width
    height = disp.height
    image = Image.new('1', (width, height))

    #получение объекта рисунка для рисования на изображении
    draw = ImageDraw.Draw(image)

    #нарисуйте черный прямоугольник, чтобы очистить изображение
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    #задание констант для определения области рисования
    padding = 2
    top = padding
    #перемещение слева направо, отслеживание текущей позиции x для рисования текста
    x = padding

    #загрузка шрифта по умолчанию
    font = ImageFont.load_default()

    #запрос данных погоды с openWeatherMap.org
    weather_data = requests.get(open_weather_map_url)

    #отображение местоположения
    location = weather_data.json().get('name') + ' - ' + weather_data.json().get('sys').get('country')
    draw.text((x, top), location,  font=font, fill=255)

    #отображение описания
    description = 'Desc ' + weather_data.json().get('weather')[0].get('main')
    draw.text((x, top+10), description,  font=font, fill=255)

    #температура
    raw_temperature = weather_data.json().get('main').get('temp')-273.15

    #температура по Цельсию
    temperature = 'Temp ' + str(raw_temperature) + '*C'
    draw.text((x, top+20), temperature, font=font, fill=255)

    #отображение давления
    pressure = 'Pres ' + str(weather_data.json().get('main').get('pressure')) + 'hPa'
    draw.text((x, top+30), pressure, font=font, fill=255)

    #отображение влажности
    humidity = 'Humi ' + str(weather_data.json().get('main').get('humidity')) + '%'
    draw.text((x, top+40), humidity, font=font, fill=255)

    #отображение ветра
    wind = 'Wind ' + str(weather_data.json().get('wind').get('speed')) + 'mps ' + str(weather_data.json().get('wind').get('deg')) + '*'
    draw.text((x, top+50), wind, font=font, fill=255)

    #вывод изображения на дисплей
    disp.image(image)
    disp.display()
    time.sleep(10)
