from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.carousel import Carousel

from kivy.lang.builder import Builder
Builder.load_file("main_kv.kv")

class Pages(Carousel):
    def __init__(self, **kwargs):
        super(Pages, self).__init__(**kwargs)
        self.loop = True  # Бесконечная прокрутка
        # self.load_slide(self.next_slide)  ##################### следущий Pages


class MyApp(App):
    def build(self):
        obj = Pages()
        return obj

    def quit_program(self):
        exit()


if __name__ == '__main__':
    MyApp().run()