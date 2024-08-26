from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window


class StandardUI(App):
    '''
    content_controller interface:
    init_state(initial_state)
        creates the state which will be rendered as content
    init_content(layout)
        adds UI content
    update_state()
        called on each step
    update_content()
        make the content reflect the updated state
    '''
    def __init__(self, content_controller, initial_state, speed=1.0/4.0, **kwargs):
        super().__init__(**kwargs)
        self.content_controller = content_controller
        self.initial_state = initial_state
        self.speed = speed

    def build(self):
        self.content_controller.init_state(self.initial_state)
        self.init_ui()
        Clock.schedule_interval(self.custom_update, self.speed)
        Window.bind(on_key_down=self.on_key_down)
        return self.layout

    def init_ui(self):
        self.layout = BoxLayout(orientation='vertical')
        self.running = False
        self.content_controller.init_content(self.layout)
        self.add_bottom_banner(self.layout)

    def add_bottom_banner(self, layout):
        bottom_banner = BoxLayout(size_hint=(1, None), height=50, orientation='horizontal')

        self.start_stop_button = Button(text="Start")
        self.start_stop_button.bind(on_press=self.on_start_stop)
        bottom_banner.add_widget(self.start_stop_button)

        self.step_button = Button(text="Step")
        self.step_button.bind(on_press=self.on_step)
        bottom_banner.add_widget(self.step_button)

        self.restart_button = Button(text="Restart")
        self.restart_button.bind(on_press=self.on_restart)
        bottom_banner.add_widget(self.restart_button)

        layout.add_widget(bottom_banner)

    def on_restart(self, instance):
        self.content_controller.init_state(None)
        self.content_controller.update_content()

    def on_step(self, instance):
        self.content_controller.update_state()
        self.content_controller.update_content()

    def custom_update(self, instance):
        if self.running:
            self.on_step(None)

    def on_start_stop(self, instance):
        if self.start_stop_button.text == "Start":
            self.start_stop_button.text = "Stop"
            self.running = True
        else:
            self.start_stop_button.text = "Start"
            self.running = False

    def on_key_down(self, window, key, *args):
        # Right arrow key is usually represented by the keycode 275
        if key == 275:
            self.on_step(None)
