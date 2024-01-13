import os

from kivy.animation import Animation
from kivy.clock import Clock

from kivymd.uix.screen import MDScreen
from kivymd.toast import toast


class ShowFileScreen(MDScreen):
    def __init__(self, **kwargs):
        self.file_id = None
        self.file_info = None
        self.show_next_func = None
        self.show_previous_func = None
        super().__init__(**kwargs)

    def on_touch_down(self, *args):
        touch = args[-1]
        if not self.ids.float_left_button.collide_point(*touch.pos) and not self.ids.float_right_button.collide_point(*touch.pos) and not self.ids.float_back_button.collide_point(*touch.pos):
            if not touch.is_double_tap and not touch.is_mouse_scrolling:
                touch.ud['start_pos'] = touch.pos
                touch.ud['is_tap'] = True
            else:
                touch.ud['is_tap'] = False
        else:
            touch.ud['is_tap'] = False
        return super().on_touch_down(touch)
    
    def on_touch_up(self, *args):
        touch = args[-1]

        movement_threshold = 20
        if touch.ud['is_tap']:
            dx = touch.pos[0] - touch.ud['start_pos'][0]
            dy = touch.pos[1] - touch.ud['start_pos'][1]
            if abs(dx) < movement_threshold and abs(dy) < movement_threshold:
                self.toggle_buttons()
        
        touch.ud['is_tap'] = False
        return super().on_touch_up(touch)
    
    def show_buttons(self):
        self.ids.float_left_button.disabled = False
        self.ids.float_right_button.disabled = False
        self.ids.float_back_button.disabled = False
        animation = Animation(opacity=0.5, duration=0.1)
        animation.start(self.ids.float_left_button)
        animation.start(self.ids.float_right_button)
        animation.start(self.ids.float_back_button)

        Clock.unschedule(self.hide_buttons)
        Clock.schedule_once(self.hide_buttons, 5)

    def hide_buttons(self, *args):
        Clock.unschedule(self.hide_buttons)

        self.ids.float_left_button.disabled = True
        self.ids.float_right_button.disabled = True
        self.ids.float_back_button.disabled = True
        animation = Animation(opacity=0, duration=0.5)
        animation.start(self.ids.float_left_button)
        animation.start(self.ids.float_right_button)
        animation.start(self.ids.float_back_button)

    def toggle_buttons(self):
        if self.ids.float_left_button.disabled:
            self.show_buttons()
        else:
            self.hide_buttons()

    def update_image(self, image_path):
        self.show_buttons()
        self.ids.image.source = image_path
        self.ids.image.reload()

    def show_file(self, file_info, file_id, show_next_func, show_previous_func):
        self.file_info = file_info
        self.file_id = file_id
        self.show_next_func = show_next_func
        self.show_previous_func = show_previous_func

        cache_path = f"./db/render/{file_id}.png"
        if not os.path.exists(cache_path):
            toast("File not found")
            self.app.root.change_screen('main_screen')
        else:
            self.update_image(cache_path)
