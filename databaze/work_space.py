from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.button import MDFlatButton, MDIconButton, MDRectangleFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import MDList, TwoLineAvatarIconListItem, ImageLeftWidget, IconRightWidget
from kivymd.uix.menu import MDDropdownMenu
from databaze.databaze import Db, Solider


class SoliderContent(BoxLayout):
    def __init__(self, id, *args, **kwargs):
        super().__init__(**kwargs)
        if id:
            solider = vars(app.soliders.database.read_by_id(id))
        else:
            solider = {"id":"", "name": "Petr Novák"}

        self.ids.solider_name.text = solider['name']



class SoliderDialog(MDDialog):
    def __init__(self, id, *args, **kwargs):
        super(SoliderDialog, self).__init__(
            type="custom",
            content_cls=SoliderContent(id=id),
            title='Záznam vojáka',
            size_hint=(.8, 1),
            buttons=[
                MDFlatButton(text='Uložit', on_release=self.save_dialog),
                MDFlatButton(text='Zrušit', on_release=self.cancel_dialog)
            ]
        )
        self.id = id

    def save_dialog(self, *args):
        dialog = {}
        dialog['name'] = self.content_cls.ids.solider_name.text
        if self.id:
            dialog["id"] = self.id
            app.soliders.update(dialog)
        else:
            app.soliders.create(dialog)
        self.dismiss()

    def cancel_dialog(self, *args):
        self.dismiss()


class MyItem(TwoLineAvatarIconListItem):
    def __init__(self, item, *args, **kwargs):
        super(MyItem, self).__init__()
        self.id = item['id']
        self.text = item['name']
        self._no_ripple_effect = True
        self.icon = IconRightWidget(icon="delete", on_release=self.on_delete)
        self.add_widget(self.icon)

    def on_press(self):
        self.dialog = SoliderDialog(id=self.id)
        self.dialog.open()

    def on_delete(self, *args):
        yes_button = MDFlatButton(text='Ano', on_release=self.yes_button_release)
        no_button = MDFlatButton(text='Ne', on_release=self.no_button_release)
        self.dialog_confirm = MDDialog(type="confirmation", title='Smazání záznamu vojáka', text="Chcete smazat záznam tohoto vojáka?", buttons=[yes_button, no_button])
        self.dialog_confirm.open()

    def yes_button_release(self, *args):
        app.soliders.delete(self.id)
        self.dialog_confirm.dismiss()

    def no_button_release(self, *args):
        self.dialog_confirm.dismiss()


class Soliders(BoxLayout):
    def __init__(self, *args, **kwargs):
        super(Soliders, self).__init__(orientation="vertical")
        global app
        app = App.get_running_app()
        scrollview = ScrollView()
        self.list = MDList()
        self.database = Db(dbtype='sqlite', dbname='soliders.db')
        self.rewrite_list()
        scrollview.add_widget(self.list)
        self.add_widget(scrollview)
        button_box = BoxLayout(orientation='horizontal')

        new_solider_btn = MDRectangleFlatButton()
        new_solider_btn.text = "Zapsat vojáka"
        new_solider_btn.icon_color = [0.9, 0.9, 0.9, 1]
        new_solider_btn.md_bg_color = [0, 0.5, 0.8, 1]
        new_solider_btn.pos_hint = {"center_x": .5}
        new_solider_btn.on_release = self.on_create_solider
        button_box.add_widget(new_solider_btn)
        self.add_widget(button_box)


    def rewrite_list(self):
        self.list.clear_widgets()
        soliders = self.database.read_all()
        for x in soliders:
            print(vars(x))
            self.list.add_widget(MyItem(item=vars(x)))

    def on_create_solider(self, *args):
        self.dialog = SoliderDialog(id=None)
        self.dialog.open()


    def create(self, solider):
        create_solider = Solider()
        create_solider.name = solider['name']
        self.database.create(create_solider)
        self.rewrite_list()

    def update(self, solider):
        update_solider = self.database.read_by_id(solider['id'])
        update_solider.name = solider['name']
        self.database.update()
        self.rewrite_list()

    def delete(self, id):
        self.database.delete(id)
        self.rewrite_list()