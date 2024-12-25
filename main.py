import time
import os

from datetime import timedelta
import pickle


from kivy.app import App
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
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
    comment_comment = ObjectProperty()

    day_spinner_str = StringProperty(CURRENT_DAY)
    quantity_day_property = NumericProperty(quantity_day_in_current_month)
    month_spinner = StringProperty(CURRENT_MONTH)

    all_month_list = ListProperty(month_lst)
    label_save_txt = StringProperty("")
    input_kopeyka = StringProperty("0")
    input_rubel = StringProperty("0")

    input_rubel_for_label = StringProperty("")
    input_kopeyka_for_label = StringProperty("")

    label_month_lst = ListProperty([CURRENT_DAY, CURRENT_MONTH])  # Устан.даты в Label_amount
    label_amount_for_day = StringProperty()

    def __init__(self, **kwargs):
        super(Pages, self).__init__(**kwargs)
        self.loop = True  # Бесконечная прокрутка
        # self.load_slide(self.next_slide)  ##################### следущий Pages
        self.KEY_DICT = ""
        self.VALUE_DICT = ""
        self.COMMENT_DICT = ""
        self.file_dict = {}
        self.main()

    def main(self):
        self.file_dict = self.load_or_create_file_dict()
        self.update_statistic()

    def work_spinner_day_month(self):
        print("work_spinner_day_month")
        self.update_statistic()


    def update_statistic(self):
        print("update_statistic")
        key = self.get_key_for_dict()
        if key in self.file_dict:
            self.install_date_in_label_amount(key)
        else:
            self.install_date_in_label_amount(key_exists=False)








    def install_date_in_label_amount(self,key_exists):
        print("Устан данных в Label")
        self.label_month_lst.clear()
        day = self.day_day_spinner.text
        month = self.month_month_spinner.text
        self.label_month_lst.append(day)
        self.label_month_lst.append(month)
        if key_exists:
            rub = self.get_parser_money(self.file_dict[key_exists], rub=True)
            kopeyka = self.get_parser_money(self.file_dict[key_exists], kop=True)
            comment = self.get_parser_comments(self.file_dict[key_exists])
            self.input_rubel_for_label = rub
            self.input_kopeyka_for_label = kopeyka
            self.comment_comment.text = comment
        else:
            self.input_rubel_for_label = "0"
            self.input_kopeyka_for_label = "0"
            self.comment_comment.text = ""

    def get_parser_money(self, value:tuple, rub=False, kop=False):
        if rub:
            rubel = value[0].split(".")[0]
            return rubel
        if kop:
            kopeyka = value[0].split(".")[1]
            return kopeyka

    def get_parser_comments(self,value):
        comments = value[1]
        return comments.capitalize()


    def save_changes(self):
        key = self.get_key_for_dict()
        print(key)
        if key not in self.file_dict: # проверка ключа на вхождение в словарь
            # Сбор данных для сохранения
            self.VALUE_DICT = self.create_value_for_dict()
            self.file_dict[self.KEY_DICT] = self.VALUE_DICT
            self.write_file_time_work()
        else:
            self.my_popup_rewrite_add()




    def add_amount(self):
        saved_amound_rub = int(self.file_dict[self.KEY_DICT].split(".")[0])*100
        saved_amound_kops = int(self.file_dict[self.KEY_DICT].split(".")[1])
        total_save_amound_in_kop = saved_amound_rub + saved_amound_kops

        current_amount_rub = int(self.rubel_money.text)*100
        current_amount_kops = int(self.kopeyka_money.text)
        total_currents_amound_in_kop = current_amount_rub + current_amount_kops

        total_summ_value_in_dict = (total_save_amound_in_kop + total_currents_amound_in_kop)/100
        self.VALUE_DICT = str(total_summ_value_in_dict)
        self.file_dict[self.KEY_DICT] = self.VALUE_DICT
        self.write_file_time_work()



































    def my_popup_rewrite_add(self):
        def answer_popup(instance):
            if instance.text == "Переписать сумму":
                self.overwriting_values()
                mynepopup.dismiss()
            elif instance.text == "Добавить сумму":
                self.add_amount()
                mynepopup.dismiss()
        mynepopup = Popup(title="Info", size_hint=(.8, .4))
        container = FloatLayout(size_hint=(1, 1))
        lab = Label(text="Рабочий день на эту дату существует.",
                    font_size=30, size_hint=(1, .3), pos_hint={'x': .001, 'top': 1},
                    halign='center')
        container.add_widget(lab)
        btn_ok = Button(text="Переписать сумму", size_hint=(.3, .3),
                        pos_hint={'x': .15, 'y': .1})
        btn_ok.bind(on_press=answer_popup)
        container.add_widget(btn_ok)
        btn_cancel = Button(text="Добавить сумму", size_hint=(.3, .3),
                            pos_hint={'x': .55, 'y': .1})
        btn_cancel.bind(on_press=answer_popup)
        container.add_widget(btn_cancel)
        mynepopup.content = container
        mynepopup.open()  # Запустить Poput

    def get_key_for_dict(self):
        day = self.day_day_spinner.text
        month = self.month_month_spinner.text
        key = day + " " + month
        self.KEY_DICT = key
        return key

    def create_value_for_dict(self):
        if self.rubel_money.text == "":
            self.rubel_money.text = "0"
        elif self.kopeyka_money.text == "":
            self.kopeyka_money.text = "0"
        self.COMMENT_DICT = self.comment_comment.text
        value = self.rubel_money.text + "." + self.kopeyka_money.text, self.COMMENT_DICT
        return value

    def overwriting_values(self):
        self.VALUE_DICT = self.create_value_for_dict()
        self.file_dict[self.KEY_DICT] = self.VALUE_DICT
        self.write_file_time_work()
        print(self.file_dict,"Старый ключ с новым значением")

    @staticmethod
    def load_or_create_file_dict():
        try:
            with open("data_base.dat", 'rb') as file:
                file_dict = pickle.load(file)
                print("Открыт успешно", file_dict)
        except (IOError, EOFError, FileNotFoundError):
            print("Не открылся. Создался пустой")
            with open(os.path.join(dir_name[0], "data_base.dat"), 'wb'):
                pass
            file_dict = {}
        return file_dict

    def my_callback(self, instance):
        self.label_save_txt = ""
        return

    def write_file_time_work(self):
        with open("data_base.dat", 'wb') as obj:
            pickle.dump(self.file_dict, obj)
        Clock.schedule_once(self.my_callback, 2)
        self.label_save_txt = "Сохранено"
        self.update_statistic()
        print(self.file_dict)

    def install_date_spinner_day(self,choice_month:str):
        """Установка кол-ва дней в спиннер в зависимости от месяца"""
        indx_month = month_lst.index(choice_month)
        quan_day = quantity_day[indx_month]
        self.quantity_day_property = quan_day + 1

    def focus_textinput(self, instance, value, text):
        if value and text == "0":
            instance.text = ""
        elif not value and text == "":
            instance.text = "0"

class MyApp(App):
    def build(self):
        Window.clearcolor = ("#40E0D0")
        obj = Pages()
        return obj

    def quit_program(self):
        exit()


if __name__ == '__main__':
    MyApp().run()