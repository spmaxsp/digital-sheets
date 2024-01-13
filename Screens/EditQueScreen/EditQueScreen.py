from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineAvatarIconListItem, OneLineListItem, IRightBodyTouch
from kivymd.uix.button import MDRaisedButton


class EditQueScreen(MDScreen):
    def __init__(self, **kwargs):
        self.que_id = None
        self.que_list = []
        self.que_name = ""
        self.save_que = None
        self.add_item_dialog = None
        super().__init__(**kwargs)

    def apply_que(self):
        self.que_list = []
        for item in self.ids.que_list.children:
            self.que_list.insert(0, {
                'text': item.text,
                'id': item.file_id
            })
        self.save_cue(self.que_list, self.que_name, self.que_id)

    def open_add_item_dialog(self):
        self.add_item_dialog = MDDialog(
            title="Add Item",
            type="custom",
            content_cls=AddToQueDialogContent(on_select=self.add_item),
            buttons=[
                MDRaisedButton(
                    text="CANCEL",
                    on_release=lambda x: self.add_item_dialog.dismiss()
                )
            ]
        )
        self.add_item_dialog.open()
        

    def add_item(self, text, file_id):
        if self.add_item_dialog:
            self.add_item_dialog.dismiss()
        self.ids.que_list.add_widget(EditQueListItem(text=text, 
                                                    file_id=file_id, 
                                                    move_up_func=self.move_up, 
                                                    move_down_func=self.move_down, 
                                                    remove_func=self.remove_item))

    def remove_item(self, item):
        self.ids.que_list.remove_widget(item)

    def swap_elements(self, index1, index2):
        tmp_name = self.ids.que_list.children[index1].text
        self.ids.que_list.children[index1].text = self.ids.que_list.children[index2].text
        self.ids.que_list.children[index2].text = tmp_name

        tmp_file_id = self.ids.que_list.children[index1].file_id
        self.ids.que_list.children[index1].file_id = self.ids.que_list.children[index2].file_id
        self.ids.que_list.children[index2].file_id = tmp_file_id

    def move_up(self, item):
        index = self.ids.que_list.children.index(item)
        if index < len(self.ids.que_list.children) - 1:
            self.swap_elements(index, index + 1)

    def move_down(self, item):
        index = self.ids.que_list.children.index(item)
        if index > 0:
            self.swap_elements(index, index - 1)

    def select_que(self, edit_que_id, que_list, que_name, save_cue_callback):
        self.que_id = edit_que_id
        self.que_name = que_name
        self.que_list = que_list
        self.save_cue = save_cue_callback

        self.ids.top_app_bar.title = "Edit Que: " + self.que_name
        self.ids.que_list.clear_widgets()
        for item in self.que_list:
            self.add_item(item['text'], item['id'])



class EditQueListItem(OneLineAvatarIconListItem):
    def __init__(self, text, file_id, move_up_func, move_down_func, remove_func, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.file_id = file_id
        self.move_up_func = move_up_func
        self.move_down_func = move_down_func
        self.remove_func = remove_func

class UpDownButtons(IRightBodyTouch, MDBoxLayout):
    adaptive_width = True



class AddToQueDialogContent(MDBoxLayout):
    def __init__(self, on_select=None, **kwargs):
        self.app = MDApp.get_running_app()
        super().__init__(**kwargs)
        self.ids.file_list.clear_widgets()
        for file_id in self.app.db['files']:
            self.ids.file_list.add_widget(AddFileItem(text=self.app.db['files'][file_id]['name'],
                                                            file_id=file_id,  
                                                            on_release=lambda x: on_select(x.text, x.file_id)))



class AddFileItem(OneLineListItem):
    def __init__(self, file_id, **kwargs):
        super().__init__(**kwargs)
        self.file_id = file_id