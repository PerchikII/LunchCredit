import time
import os

from datetime import timedelta
import pickle


from kivy.app import App
from kivy.clock import Clock
from kivy.tools.pep8checker.pep8 import get_parser
from kivy.uix.label import Label
from kivy.uix.popup import Popup
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
    two_pages = ObjectProperty()
    scroll_two_pages = ObjectProperty()

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
    # label_amount_for_day = StringProperty()

    def __init__(self, **kwargs):
        super(Pages, self).__init__(**kwargs)
        self.loop = True  # Бесконечная прокрутка

        # self.load_slide(self.next_slide)  ##################### следущий Pages

        # self.KEY_DICT = ""
        # self.VALUE_DICT = ""
        # self.COMMENT_DICT = ""
        self.file_dict = {}
        self.main()

    def main(self):
        self.file_dict = self.load_or_create_file_dict()
        key = self.get_key_for_dict()
        self.update_statistic(key)











    def create_label_statistic_two_page(self):
        self.two_pages.bind(minimum_height=self.two_pages.setter('height'))

        for i in range(1,3):
            box_data = BoxLayout()
            lab_data = Label(padding=5,text=f"{i+1} Декабря",size_hint_y=None, height=40,
                         size_hint_x= .5)

            lab_money = Label(padding=5,text=f"{i}руб {i+100}коп",size_hint_y=None, height=40,
                         size_hint_x= .5)

            lab_comment = Label(padding=5,text=f"Чай,вода,булочка,пивас,ганджубас",size_hint_y=None, height=40,
                         size_hint_x= .5)
            box_data.add_widget(lab_data)
            box_data.add_widget(lab_money)
            box_data.add_widget(lab_comment)

        self.two_pages.add_widget(box_data)
























    def update_statistic(self,key:str):
        print(key,"95 Мартобря")
        if key in self.file_dict:
            day = self.day_day_spinner.text
            month = self.month_month_spinner.text
            rubli = self.get_parser_money(key,rub=True)
            kopeyki = self.get_parser_money(key,kop=True)
            comment = self.get_parser_comments(key)
            data = day,month,rubli,kopeyki,comment
            self.install_date_in_label_amount(data)
        else:
            print("ключа нет")
            self.install_date_in_label_amount(data=False)


    def install_date_in_label_amount(self, data):
        if data:
            self.label_month_lst.clear()
            day = data[0]
            month = data[1]
            self.label_month_lst.append(day)
            self.label_month_lst.append(month)
            rub = data[2]
            kopeyka = data[3]
            comment = data[4]
            self.input_rubel_for_label = rub
            self.input_kopeyka_for_label = kopeyka
            self.comment_comment.text = comment
        else:
            self.label_month_lst.clear()
            self.label_month_lst.append('0')
            self.label_month_lst.append('0')
            self.input_rubel_for_label = "0"
            self.input_kopeyka_for_label = "0"
            self.comment_comment.text = ""

    def get_parser_money(self, key_dict, rub=False, kop=False) ->str:
        val_for_parsing = self.file_dict[key_dict]
        if rub:
            rubel = val_for_parsing[0].split(".")[0]
            return rubel
        if kop:
            kopeyka = val_for_parsing[0].split(".")[1]
            return kopeyka
    def get_parser_comments(self,key):
        comments = self.file_dict[key][1]
        return comments.capitalize()

    def work_spinner_day_month(self):
        key = self.get_key_for_dict()
        self.rubel_money.text = "0"
        self.kopeyka_money.text = "0"
        self.update_statistic(key)



    def save_changes(self):
        key = self.get_key_for_dict()
        if key not in self.file_dict: # проверка ключа на вхождение в словарь
            # Сбор данных для сохранения
            if self.rubel_money.text == "":
                self.rubel_money.text = "0"
            elif self.kopeyka_money.text == "":
                self.kopeyka_money.text = "0"
            comment = self.comment_comment.text
            value = self.create_value_for_dict(self.rubel_money.text,self.kopeyka_money.text,comment)
            self.file_dict[key] = value
            self.write_file()
        else:
            self.my_popup_rewrite_add()

    def create_value_for_dict(self,rub,kop,comm):
        value = rub + "." + kop, comm
        return value




    def add_amount(self):
        key = self.get_key_for_dict()
        old_amount_rub = int(self.get_parser_money(key,rub=True))*100
        old_amount_kops = int(self.get_parser_money(key,kop=True))
        total_save_amount_in_kop = old_amount_rub + old_amount_kops

        current_amount_rub = int(self.rubel_money.text)*100
        current_amount_kops = int(self.kopeyka_money.text)
        total_currents_amount_in_kop = current_amount_rub + current_amount_kops

        total_summ_value_in_dict = str((total_save_amount_in_kop + total_currents_amount_in_kop)/100)
        # сформировать новое значение
        rub = total_summ_value_in_dict.split(".")[0]
        kop = total_summ_value_in_dict.split(".")[1]
        comment = self.comment_comment.text
        new_value = self.create_value_for_dict(rub,kop,comment)
        self.file_dict[key] = new_value
        self.write_file()
        self.rubel_money.text = "0"
        self.kopeyka_money.text = "0"
        print("New summ value",total_summ_value_in_dict)

    def del_amount(self):
        key = self.get_key_for_dict()
        if key in self.file_dict:
            del self.file_dict[key]
            Clock.schedule_once(self.my_callback, 2)
            self.label_save_txt = "Дата удалена"
        else:
            Clock.schedule_once(self.my_callback, 2)
            self.label_save_txt = "Такой даты не существует"



    def my_popup_rewrite_add(self):
        def answer_popup(instance):

            if instance.text == "Переписать сумму":
                self.overwriting_values()
                mynepopup.dismiss()
            elif instance.text == "Добавить данные":
                self.add_amount()
                mynepopup.dismiss()
            elif instance.text == "Удалить сумму":
                self.del_amount()
                mynepopup.dismiss()


        mynepopup = Popup(title="Изменение суммы")
        root_container = BoxLayout(size_hint=(1, 1), orientation="vertical")
        label_container = BoxLayout(size_hint=(1, .3))
        lab = Label(text="Сумма на эту дату существует.",
                    font_size=40, size_hint=(1, .3), pos_hint={'x': .001, 'top': 1},
                    halign='center')
        label_container.add_widget(lab)

        button_container = BoxLayout(size_hint=(1, .3), padding=10, spacing=10)
        btn_rewrite = Button(text="Переписать сумму", size_hint=(.3, 1), font_size=20)
        btn_rewrite.bind(on_press=answer_popup)
        btn_add_amount = Button(text="Добавить данные", size_hint=(.3, 1), font_size=23)
        btn_add_amount.bind(on_press=answer_popup)
        btn_cancel = Button(text="Удалить сумму", size_hint=(.3, 1), font_size=25)
        btn_cancel.bind(on_press=answer_popup)

        empty_container = BoxLayout(size_hint=(1, .3), padding=10, spacing=10)
        btn_close_popup = Button(text="Закрыть", size_hint=(1, .5), font_size=23)
        btn_close_popup.bind(on_press=mynepopup.dismiss)
        empty_container.add_widget(btn_close_popup)

        button_container.add_widget(btn_rewrite)
        button_container.add_widget(btn_add_amount)
        button_container.add_widget(btn_cancel)

        root_container.add_widget(label_container)
        root_container.add_widget(button_container)
        root_container.add_widget(empty_container)

        mynepopup.content = root_container
        mynepopup.open()  # Запустить Poput

    def get_key_for_dict(self):
        day = self.day_day_spinner.text
        month = self.month_month_spinner.text
        key = day + " " + month
        #self.KEY_DICT = key
        return key



    def overwriting_values(self):
        rub = self.rubel_money.text
        kop = self.kopeyka_money.text
        comment = self.comment_comment.text

        key = self.get_key_for_dict()
        value = self.create_value_for_dict(rub,kop,comment)

        self.file_dict[key] = value
        self.write_file()
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

    def my_callback(self, time):
        self.label_save_txt = ""


    def write_file(self):
        try:
            with open("data_base.dat", 'wb') as obj:
                pickle.dump(self.file_dict, obj)
            Clock.schedule_once(self.my_callback, 2)
            self.label_save_txt = "Данные успешно сохранены"
            key = self.get_key_for_dict()
            self.update_statistic(key)
            print(self.file_dict)
        except Exception as err:
            self.label_save_txt = "Ошибка: ",err

    def focus_textinput(self, instance, value, text):
        if value and text == "0":
            instance.text = ""
        elif not value and text == "":
            instance.text = "0"



    def install_date_spinner_day(self,choice_month:str):
        """Установка кол-ва дней в спиннер в зависимости от месяца"""
        indx_month = month_lst.index(choice_month)
        quan_day = quantity_day[indx_month]
        self.quantity_day_property = quan_day + 1


class MyApp(App):
    def build(self):
        Window.clearcolor = "#40E0D0"
        obj = Pages()
        return obj

    def quit_program(self):
        exit()


if __name__ == '__main__':
    MyApp().run()