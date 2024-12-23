import time
import os
from datetime import timedelta
import pickle

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.carousel import Carousel
from kivy.properties import ListProperty, StringProperty, NumericProperty

from kivy.core.window import Window

from kivy.lang.builder import Builder
"""Установить kv файл в директорию совместно в main.py"""
dir_name = os.path.split(os.path.abspath(__file__))
Builder.load_file(os.path.join(dir_name[0], "main_kv.kv"))



month_lst = ('Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
             'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь')

quantity_day = (31,29,31,30,31,30,31,31,30,31,30,31)

time_now = time.time()  # Секунды с начала эпохи
time_day = time.localtime(time_now)  # Текущее число

if time.strftime("%d", time_day)[0] == "0":
    CURRENT_DAY = time.strftime("%d", time_day)[1]
else:
    CURRENT_DAY = time.strftime("%d", time_day)
number_month = int(time.strftime("%m", time_day))-1 # минус месяц из списка

CURRENT_MONTH = month_lst[number_month]
quantity_day_in_current_month = quantity_day[number_month]+1



class TextInpMoney(TextInput):
    def insert_text(self, enter_symbol, from_undo=False):
        print(enter_symbol)
        if enter_symbol.isdigit():
            return super().insert_text(enter_symbol, from_undo=from_undo)

class Pages(Carousel):
    day_spinner = StringProperty(CURRENT_DAY)
    month_spinner = StringProperty(CURRENT_MONTH)
    def __init__(self, **kwargs):
        super(Pages, self).__init__(**kwargs)
        self.loop = True  # Бесконечная прокрутка
        # self.load_slide(self.next_slide)  ##################### следущий Pages








class MyApp(App):
    def build(self):
        Window.clearcolor = ("#40E0D0")
        obj = Pages()
        return obj

    def quit_program(self):
        exit()


if __name__ == '__main__':
    MyApp().run()