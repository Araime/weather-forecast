import os
import sys
import time
from tkinter import ttk
from tkinter import messagebox

import requests
from ttkthemes import ThemedTk

OW_TOKEN = 'your_token'
API_URL = 'https://api.openweathermap.org/data/2.5/weather'
WORK_PATH = getattr(sys, "_MEIPASS", os.path.abspath(os.path.dirname(__file__)))


def print_weather(weather):
    try:
        city = weather['name']
        country = weather['sys']['country']
        temp = weather['main']['temp']
        press = weather['main']['pressure']
        humidity = weather['main']['humidity']
        wind = weather['wind']['speed']
        desc = weather['weather'][0]['description']
        sunrise_ts = weather['sys']['sunrise']
        sunset_ts = weather['sys']['sunset']
        sunrise_struct_time = time.localtime(sunrise_ts)
        sunset_struct_time = time.localtime(sunset_ts)
        sunrise = time.strftime('%H:%M:%S', sunrise_struct_time)
        sunset = time.strftime('%H:%M:%S', sunset_struct_time)
        return f'Местоположение: {city}, {country} \n' \
               f'Температура: {temp} °C \nАтм. давление: {press} гПа \n' \
               f'Влажность: {humidity}% \nСкорость ветра: {wind} м/с \n' \
               f'Погодные условия: {desc} \nВосход: {sunrise} \nЗакат: {sunset}'
    except requests.exceptions.ConnectionError:
        return 'Ошибка получения данных...'


def get_weather(event=''):
    if not entry.get():
        messagebox.showwarning('Warning', 'Введите запрос в формате city, country_code')
    else:
        params = {
            'appid': OW_TOKEN,
            'q': entry.get(),
            'units': 'metric',
            'lang': 'ru'
        }
    response = requests.get(API_URL, params=params)
    weather = response.json()
    label['text'] = print_weather(weather)


if __name__ == '__main__':
    root = ThemedTk(theme='arc', themebg='arc')
    root.title('Weather forecast')
    root.geometry('450x250+1000+300')
    root.resizable(0, 0)
    iconbit = os.path.join(WORK_PATH, "cloud.ico")
    root.iconbitmap(iconbit)

    style = ttk.Style()
    style.configure('TFrame', background='#AFEEEE')

    top_frame = ttk.Frame(root)
    top_frame.place(relx=0.5, rely=0.1, relwidth=0.9, relheight=0.1, anchor='n')

    entry = ttk.Entry(top_frame, font='Arial 12 bold')
    entry.place(relwidth=1, relheight=1)
    entry.bind('<Return>', get_weather)
    entry.focus()

    lower_frame = ttk.Frame(root)
    lower_frame.place(relx=0.5, rely=0.25, relwidth=0.9, relheight=0.7, anchor='n')

    label = ttk.Label(lower_frame, anchor='nw', font="Arial 12 bold")
    label.place(relwidth=1, relheight=1)

    root.mainloop()
