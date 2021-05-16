from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivy.lang import Builder
from databaze.work_space import Soliders


class DatabaseScreen(Screen):
    pass


class Test(MDApp):

    def build(self):
        self.theme_cls.primary_palette = "BlueGray"
        builder = Builder.load_file('main.kv')
        self.soliders = Soliders()
        builder.ids.navigation.ids.tab_manager.screens[0].add_widget(self.soliders)
        return builder


Test().run()