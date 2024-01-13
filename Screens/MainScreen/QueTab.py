from kivymd.app import MDApp
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivymd.uix.list import OneLineAvatarIconListItem
from kivymd.toast import toast


class QueTab(MDBottomNavigationItem):
    def __init__(self, **kwargs):
        self.app = MDApp.get_running_app()
        self.selected_que_id = None
        self.que_count = 0
        super().__init__(**kwargs)

    def update_data(self):
        self.ids.que_list.clear_widgets()
        for que_id in self.app.db['ques']:
            self.ids.que_list.add_widget(QueListItem(text=self.app.db['ques'][que_id]['name'], 
                                                        que_id=que_id, 
                                                        remove_func=self.remove_que, 
                                                        edit_func=self.edit_que, 
                                                        on_release= lambda x: self.show_que(x.que_id)))
            
    def show_que(self, que_id):
        self.selected_que_id = que_id
        self.que_count = 0

        file_id = self.app.db['ques'][que_id]['list'][self.que_count]['id']

        toast(f"Showing que: {self.app.db['ques'][que_id]['name']}: {self.que_count + 1}/{len(self.app.db['ques'][que_id]['list'])}")

        self.app.root.ids.show_file_screen.show_file(file_id=file_id,
                                                        file_info=self.app.db['files'][file_id], 
                                                        show_next_func=self.show_next_file, 
                                                        show_previous_func=self.show_previous_file)
        self.app.root.change_screen('show_file_screen')

    def show_next_file(self, current_file_id):
        if self.que_count < len(self.app.db['ques'][self.selected_que_id]['list']) - 1:
            self.que_count += 1

            toast(f"Showing que: {self.app.db['ques'][self.selected_que_id]['name']}: {self.que_count + 1}/{len(self.app.db['ques'][self.selected_que_id]['list'])}")

            file_id = self.app.db['ques'][self.selected_que_id]['list'][self.que_count]['id']
            self.app.root.ids.show_file_screen.show_file(file_id=file_id,
                                                            file_info=self.app.db['files'][file_id], 
                                                            show_next_func=self.show_next_file, 
                                                            show_previous_func=self.show_previous_file)

    def show_previous_file(self, current_file_id):
        if self.que_count > 0:
            self.que_count -= 1

            toast(f"Showing que: {self.app.db['ques'][self.selected_que_id]['name']}: {self.que_count + 1}/{len(self.app.db['ques'][self.selected_que_id]['list'])}")

            file_id = self.app.db['ques'][self.selected_que_id]['list'][self.que_count]['id']
            self.app.root.ids.show_file_screen.show_file(file_id=file_id,
                                                            file_info=self.app.db['files'][file_id], 
                                                            show_next_func=self.show_next_file, 
                                                            show_previous_func=self.show_previous_file)

    def new_que(self):
        self.app.open_name_entry_dialog(callback=self.new_que_named, 
                                        name="Enter que name",
                                        default_text="New Que")
        
    def new_que_named(self, name):
        self.app.name_entry_dialog.dismiss()
        que_id = self.generate_id()
        print(name, que_id)
        self.app.db['ques'][que_id] ={
            'name': name,
            'list': []
        }
        self.app.write_db()
        self.update_data()

    def generate_id(self):
        que_id = 0
        while que_id in self.app.db['ques']:
            que_id += 1
        return que_id
    
    def save_que(self, que_list, que_name, edit_que_id):
        self.app.db['ques'][edit_que_id] = {
            'name': que_name,
            'list': que_list
        }
        self.app.write_db()
        self.update_data()
        self.app.root.change_screen('main_screen')

    def edit_que(self, que_id):
        self.app.root.ids.edit_que_screen.select_que(edit_que_id=que_id,
                                                    que_list=self.app.db['ques'][que_id]['list'], 
                                                    que_name=self.app.db['ques'][que_id]['name'], 
                                                    save_cue_callback=self.save_que)
        self.app.root.change_screen('edit_que_screen')

    def remove_que(self, que_id):
        self.app.db['ques'].pop(que_id)
        self.app.write_db()
        self.update_data()



class QueListItem(OneLineAvatarIconListItem):
    def __init__(self, text, que_id, remove_func, edit_func, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.que_id = que_id
        self.remove_func = remove_func
        self.edit_func = edit_func
