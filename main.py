import os

from kivy.lang import Builder

from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.button import MDRaisedButton

import json


from Screens.MainScreen.MainScreen import MainScreen
from Screens.EditQueScreen.EditQueScreen import EditQueScreen
from Screens.ShowFileScreen.ShowFileScreen import ShowFileScreen

class MainScreenManager(ScreenManager):
    def change_screen(self, new_screen):
        print('main screen manager')
        if new_screen == 'main_screen':
            self.transition.direction = 'right'
        else:
            self.transition.direction = 'left'
        self.current = new_screen


class NameDialogContent(BoxLayout):
    pass


class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Digital-Sheets"
        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.material_style = "M3"
        self.theme_cls.theme_style = "Dark"

        self.current_db_path = "./db/db.json"
        self.db_loaded = False

        self.db = None

        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager, 
            select_path=self.exit_manager,
            selector="file"
        )

        self.name_entry_dialog = None

    #
    #    File manager functions
    #
    def file_manager_open(self, callback, name, file_type="file", *args, **kwargs):
        self.file_manager.selector = file_type
        self.file_manager.name = name
        self.file_manager.select_path = lambda path: callback(path, *args, **kwargs)
        user_folder = os.path.expanduser('~')
        self.file_manager.show(user_folder)
        self.manager_open = True

    def exit_manager(self, *args):
        self.manager_open = False
        self.file_manager.close()

    #
    #    DB functions
    #
    def read_db(self):
        if os.path.exists(self.current_db_path):
            try:
                with open(self.current_db_path, 'r') as f:
                    self.db = json.load(f)
                    self.db_loaded = True
            except Exception as e:
                print("Error loading db: ", e)
                self.db_loaded = False
                self.db = None
        else:
            print("Error loading db: file does not exist")
            self.db_loaded = False
            self.db = None

        if self.db_loaded:
            self.root.ids.main_screen.update_data()

    def write_db(self):
        if self.db_loaded:
            try:
                with open(self.current_db_path, 'w') as f:
                    json.dump(self.db, f)
            except Exception as e:
                print("Error writing db: ", e)
        else:
            print("Error writing db: no db loaded")
    

    #
    #    Dialogs
    #
    def open_name_entry_dialog(self, callback, name, default_text="", *args, **kwargs):
        self.name_entry_dialog = MDDialog(
            title=name,
            type="custom",
            text=default_text,
            content_cls=NameDialogContent(),
            buttons=[
                MDRaisedButton(
                    text="CANCEL",
                    on_release=lambda x: self.name_entry_dialog.dismiss()
                ),
                MDRaisedButton(
                    text="OK",
                    on_release=lambda x: callback(self.name_entry_dialog.content_cls.ids.name_textfield.text, *args, **kwargs)
                )
            ]
        )
        self.name_entry_dialog.open()

    def return_to_main_screen(self):
        self.root.change_screen('main_screen')

    #
    #    Kivy MD events
    #  
    def on_start(self):
        self.read_db()
        return super().on_start()

    def events(self, instance, keyboard, keycode, text, modifiers):
        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True


if __name__ == '__main__':
    MainApp().run()