import os

from kivymd.app import MDApp
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivymd.uix.list import OneLineAvatarIconListItem
from kivymd.toast import toast

import fitz


class FileTab(MDBottomNavigationItem):  
    def __init__(self, **kwargs):
        self.app = MDApp.get_running_app()
        super().__init__(**kwargs)

    def update_data(self):
        self.ids.file_list.clear_widgets()
        for file_id in self.app.db['files']:
            self.ids.file_list.add_widget(FileListItem(text=self.app.db['files'][file_id]['name'], 
                                                        file_id=file_id, 
                                                        remove_func=self.remove_file, 
                                                        remap_func=self.remap_file, 
                                                        on_release= lambda x: self.show_file(x.file_id)))
        
    def new_file(self):
        self.app.file_manager_open(callback=self.new_file_selection, 
                                    name="Select PDF file")
        
    def show_file(self, file_id):
        self.app.root.ids.show_file_screen.show_file(file_id=file_id,
                                                        file_info=self.app.db['files'][file_id], 
                                                        show_next_func=self.show_next_file, 
                                                        show_previous_func=self.show_previous_file)
        self.app.root.change_screen('show_file_screen')

    def show_next_file(self, current_file_id):
        if current_file_id in self.app.db['files']:
            file_ids = list(self.app.db['files'].keys())
            current_index = file_ids.index(current_file_id)
            if current_index < len(file_ids) - 1:
                self.show_file(file_ids[current_index + 1])

    def show_previous_file(self, current_file_id):
        if current_file_id in self.app.db['files']:
            file_ids = list(self.app.db['files'].keys())
            current_index = file_ids.index(current_file_id)
            if current_index > 0:
                self.show_file(file_ids[current_index - 1])

    def new_file_selection(self, path):
        self.app.exit_manager()

        if path:
            if os.path.exists(path) and os.path.isfile(path):
                if path.endswith('.pdf') or path.endswith('.PDF'):
                    self.app.open_name_entry_dialog(
                                                    callback=self.new_file_named, 
                                                    name="Enter display name", 
                                                    default_text=os.path.basename(path),
                                                    path=path
                                                    )
                else:
                    toast("File must be a PDF")

    def render_pdf(self, pdf_path, cache_path):
        try:
            doc = fitz.open(pdf_path)
            pix = doc[0].get_pixmap()
            pix.save(cache_path)
            return True
        except Exception as e:
            print("Error rendering pdf: ", e)
            toast("Error rendering pdf")
            return False
        
    def new_file_named(self, name, path):
        self.app.name_entry_dialog.dismiss()

        file_id = self.generate_id()
        cache_path = f"./db/render/{file_id}.png"

        if self.render_pdf(path, cache_path):
            self.app.db['files'][file_id] ={
                'name': name,
                'path': path
            }
            self.app.write_db()
            self.update_data()
    
    def generate_id(self):
        file_id = 0
        while file_id in self.app.db['files']:
            file_id += 1
        return file_id

    def check_delete_file(self, file_id):
        for item in self.app.db['ques']:
            if file_id in self.app.db['ques'][item]['list']:
                return False
        return True
    
    def remap_file(self, file_id):
        print("TODO: remap file")

    def remove_file(self, file_id):
        if self.check_delete_file(file_id):
            self.app.db['files'].pop(file_id)
            self.app.write_db()
            self.update_data()
        else:
            print ("File is used in a que")
            toast("File is used in a que")



class FileListItem(OneLineAvatarIconListItem):
    def __init__(self, text, file_id, remove_func, remap_func, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.file_id = file_id
        self.remove_func = remove_func
        self.remap_func = remap_func