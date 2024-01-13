from kivymd.uix.screen import MDScreen

from Screens.MainScreen.FileTab import FileTab
from Screens.MainScreen.QueTab import QueTab

class MainScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def update_data(self):
        self.ids.file_tab.update_data()
        self.ids.que_tab.update_data()


