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
from kivy.properties import ListProperty, StringProperty, NumericProperty,ObjectProperty

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


class TextInpMoneyRub(TextInput):
    def insert_text(self, enter_symbol, from_undo=False):
        if enter_symbol.isdigit() and len(self.text) < 4:
            return super().insert_text(enter_symbol, from_undo=from_undo)


class TextInpMoneyKop(TextInput):
    def insert_text(self, enter_symbol, from_undo=False):
        if enter_symbol.isdigit() and len(self.text) < 2:
            return super().insert_text(enter_symbol, from_undo=from_undo)







class Pages(Carousel):
    day_day_spinner = ObjectProperty()
    month_month_spinner = ObjectProperty()
    rubel_money = ObjectProperty()
    kopeyka_money = ObjectProperty()




    day_spinner_str = StringProperty(CURRENT_DAY)
    quantity_day_property = NumericProperty(quantity_day_in_current_month)
    month_spinner = StringProperty(CURRENT_MONTH)
    all_month_list = ListProperty(month_lst)
    input_rubel = StringProperty("0")
    input_kopeyka = StringProperty("0")
    label_month_lst = ListProperty([CURRENT_DAY, CURRENT_MONTH])  # Устан.даты в Label
    label_amount_for_day = StringProperty()

    def __init__(self, **kwargs):
        super(Pages, self).__init__(**kwargs)
        self.loop = True  # Бесконечная прокрутка
        # self.load_slide(self.next_slide)  ##################### следущий Pages
        self.file_dict = {}

        print(self.file_dict)





    def focus_textinput(self, instance, value, text):
        if value and text == "0":
            instance.text = ""








    def install_date_spinner_day(self,choice_month:str):
        """Установка кол-ва дней в спиннер в зависимости от месяца"""
        indx_month = month_lst.index(choice_month)
        quan_day = quantity_day[indx_month]
        self.quantity_day_property = quan_day + 1


    def create_key_for_dict(self):
        day = self.day_day_spinner.text
        month = self.month_month_spinner.text
        self.file_dict[day + " " + month] = self.rubel_money.text + " " + self.kopeyka_money.text
        print(self.file_dict)

    def create_date_in_label_amount(self,text):
        self.label_month_lst.clear()
        day = self.day_day_spinner.text
        month = self.month_month_spinner.text
        self.label_month_lst.append(day)
        self.label_month_lst.append(month)

        self.input_rubel = self.rubel_money.text
        self.input_kopeyka = self.kopeyka_money.text


















class MyApp(App):
    def build(self):
        Window.clearcolor = ("#40E0D0")
        obj = Pages()
        return obj

    def quit_program(self):
        exit()


if __name__ == '__main__':
    MyApp().run()