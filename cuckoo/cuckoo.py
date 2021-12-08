# cuckoo.py
from datetime import datetime

from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dropdownitem import MDDropDownItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.theming import ThemeManager
from kivymd.font_definitions import theme_font_styles



# DARK: 0.09, 0.11, 0.12
# LIGHT: 0.98, 0.88, 0.66
class TimeDisplay(MDLabel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update, 0.25)
        self.text = '12:00:00 am'
        self.halign = 'center'
        self.theme_text_color = 'Custom'
        self.text_color = (0.98, 0.88, 0.66, 1.0)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.7}
        self.font_style = 'H1'
        self.font_size = 144
        self.bold = True
        self.font_name = 'assets/AmaticSC-B.ttf'

    def __del__(self):
        Clock.unschedule(self.update)

    def update(self, dt):
        current_time = datetime.now()
        new_str: str = current_time.strftime('%I:%M:%S %p')
        self.text = new_str


def CuckooDrop(MDDropDownItem):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pos_hint = {'center_x': 0.3, 'center_y': 0.2}
        

class RowLayout(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = 'horizontal'


class CuckooLayout(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [5, 10, 5, 0]

        with self.canvas.before:
            Color(0.09, 0.11, 0.12, 1.0)
            self.rect = Rectangle(size = self.size, pos = self.pos)
        self.bind(size = self._update_rect, pos = self._update_rect)

        self.rone = RowLayout()
        self.rone.spacing = 0
        self.add_widget(self.rone)

        self.rtwo = RowLayout()
        self.rtwo.spacing = 15
        self.add_widget(self.rtwo)

        self.rthree = RowLayout()
        self.rthree.spacing = 15
        self.add_widget(self.rthree)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size



# md_bg_color = (0.98, 0.88, 0.66, 1.0),
# text_color = (0.09, 0.11, 0.12, 1.0),
class CuckooApp(MDApp):
    def build(self):
        layout: CuckooLayout = CuckooLayout()

        self.time_lbl: TimeDisplay = TimeDisplay()
        layout.rone.add_widget(self.time_lbl)

        self.hour_ddi: CuckooDrop = CuckooDrop()
            # md_bg_color = (0.98, 0.88, 0.66, 1.0),
            # size_hint = (0.3, 0.3),
            # font_size = '24sp',
        self.hour_ddi.bind(on_release=self.open_hour_drop_menu)
        layout.rtwo.add_widget(self.hour_ddi)

        self.minute_ddi: CuckooDrop = CuckooDrop(
            # md_bg_color = (0.98, 0.88, 0.66, 1.0),
            pos_hint = {'center_x': 0.6, 'center_y': 0.2},
            # size_hint = (0.3, 0.3),
            # font_size = '24sp',
        )
        self.minute_ddi.bind(on_release=self.open_minute_drop_menu)
        layout.rtwo.add_widget(self.minute_ddi)

        self.meridiem_ddi: CuckooDrop = CuckooDrop(
            # md_bg_color = (0.98, 0.88, 0.66, 1.0),
            pos_hint = {'center_x': 0.85, 'center_y': 0.2},
            # size_hint = (0.2, 0.3),
            # font_size = '24sp',
        )
        self.meridiem_ddi.bind(on_release=self.open_meridiem_drop_menu)
        layout.rtwo.add_widget(self.meridiem_ddi)


        # self.minute_btn: TimeButton = TimeButton(
        #     text = '00',
        #     theme_text_color = 'Custom',
        #     md_bg_color = (0.98, 0.88, 0.66, 1.0),
        #     text_color = (0.09, 0.11, 0.12, 1.0),
        #     pos_hint = {'center_x': 0.6, 'center_y': 0.2},
        #     size_hint = (0.3, 0.3)
        # )
        # self.minute_btn.bind(on_release=self.open_minute_drop_menu)
        # layout.rtwo.add_widget(self.minute_btn)
        # 
        # self.meridiem_btn: TimeButton = TimeButton(
        #     text = 'AM',
        #     theme_text_color = 'Custom',
        #     md_bg_color = (0.98, 0.88, 0.66, 1.0),
        #     text_color = (0.09, 0.11, 0.12, 1.0),
        #     pos_hint = {'center_x': 0.85, 'center_y': 0.2},
        #     size_hint = (0.2, 0.3)
        # )
        # self.meridiem_btn.bind(on_release=self.open_meridiem_drop_menu)
        # layout.rtwo.add_widget(self.meridiem_btn)



        # ---
        self.hour_items: list = [
            {
                'viewclass': 'OneLineListItem',
                'text': f'{i}',
                'height': dp(54),
                'on_release': lambda x = f'{i}': self.set_hour_callback(x),
            } for i in range(1, 13)
        ]

        self.minute_items: list = [
            {
                'viewclass': 'OneLineListItem',
                'text': f'{i}',
                'height': dp(54),
                'on_release': lambda x = f'{i}': self.set_minute_callback(x),
            } for i in range(60)
        ]

        self.meridiem_items: list = [
            {
                'viewclass': 'OneLineListItem',
                'text': 'AM',
                'height': dp(54),
                'on_release': lambda x = 'AM': self.set_meridiem_callback(x),
            }, 
            {
                'viewclass': 'OneLineListItem',
                'text': 'PM',
                'height': dp(54),
                'on_release': lambda x = 'PM': self.set_meridiem_callback(x),
            }, 
        ]

        self.hour_menu: MDDropdownMenu = MDDropdownMenu(
            caller = self.hour_ddi,
            items = self.hour_items,
            width_mult = 2,
            position = 'center',
            background_color = (0.98, 0.88, 0.66, 1.0),
            opening_time = 0,
        )
        self.hour_menu.bind()

        self.minute_menu: MDDropdownMenu = MDDropdownMenu(
            caller = self.minute_ddi,
            items = self.minute_items,
            width_mult = 2,
            position = 'center',
            background_color = (0.98, 0.88, 0.66, 1.0),
            opening_time = 0,
        )
        self.minute_menu.bind()

        self.meridiem_menu: MDDropdownMenu = MDDropdownMenu(
            caller = self.meridiem_ddi,
            items = self.meridiem_items,
            width_mult = 2,
            position = 'center',
            background_color = (0.98, 0.88, 0.66, 1.0),
            opening_time = 0,
        )
        self.meridiem_menu.bind()

        return layout

    def set_hour_callback(self, text_item):
        self.hour_ddi.set_item(text_item)
        self.hour_menu.dismiss()

    def set_minute_callback(self, text_item):
        self.minute_ddi.set_item(text_item)
        self.minute_menu.dismiss()

    def set_meridiem_callback(self, text_item):
        self.meridiem_ddi.set_item(text_item)
        self.meridiem_menu.dismiss()

    def open_hour_drop_menu(self, instance):
        self.hour_menu.open()

    def open_minute_drop_menu(self, instance):
        self.minute_menu.open()

    def open_meridiem_drop_menu(self, instance):
        self.meridiem_menu.open()




if __name__ == '__main__':
    CuckooApp().run()
