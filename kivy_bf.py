from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock
from cross_react_programs import to_str, to_human_readable_str, random_program, to_int_arr
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window

program = None


class KivyBf(App):
    def build(self):
        self.round = 0
        global program
        self.init_state(program)
        self.init_ui()
        Clock.schedule_interval(self.custom_update, 1.0 / 4.0)
        Window.bind(on_key_down=self.on_key_down)
        return self.layout

    def init_state(self, starting_tape):
        if starting_tape is not None:
            if type(starting_tape) is list:
                starting_tape = to_str(starting_tape)
            self.program1 = starting_tape
        else:
            self.program1 = random_program()
        self.state = {
            "tape": to_int_arr(self.program1),
            "pointer": 0,
            "head0": 0,
            "head1": 0,
            "loop_stack": [],
            "num_reads": 0,
            "max_reads": 2 ** 13
        }
        print(self.program1)

    def init_ui(self):
        self.layout = FloatLayout()
        self.running = False
        self.add_bottom_banner(self.layout)
        self.add_labels(self.layout)

    def get_label(self, text, y_down):
        return Label(
            text=text,
            halign="left",
            valign="middle",
            font_name="Courier_Prime/CourierPrime-Regular.ttf",
            pos=(0, self.text_layout.height - y_down),
            size=(300, 10)
        )

    def add_labels(self, layout):
        self.text_layout = FloatLayout()

        self.parans_label = self.get_label(" " * 64, 0)
        self.text_layout.add_widget(self.parans_label)

        self.pointer_label = self.get_label("v"+" "*63, 50)
        self.text_layout.add_widget(self.pointer_label)

        bf_text = to_human_readable_str(self.program1, False)
        self.bf_label = self.get_label(bf_text, 100)
        self.text_layout.add_widget(self.bf_label)

        self.h_label = self.get_label("^" + " " * 63, 150)
        self.text_layout.add_widget(self.h_label)

        layout.add_widget(self.text_layout)

    def add_bottom_banner(self, layout):
        bottom_banner = BoxLayout(size_hint=(1, None), height=50, orientation='horizontal')
        bottom_banner.pos_hint = {'x': 0, 'y': 0}

        self.start_stop_button = Button(text="Start")
        self.start_stop_button.bind(on_press=self.on_start_stop)
        bottom_banner.add_widget(self.start_stop_button)

        self.step_button = Button(text="Step")
        self.step_button.bind(on_press=self.on_step)
        bottom_banner.add_widget(self.step_button)

        def on_restart(instance):
            self.init_state(None)
            self.re_render()

        self.restart_button = Button(text="Restart")
        self.restart_button.bind(on_press=on_restart)
        bottom_banner.add_widget(self.restart_button)

        layout.add_widget(bottom_banner)

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

    def on_step(self, instance):
        self.round += 1
        self.state = update_state(**self.state)
        self.re_render()

    def re_render(self):
        self.program1 = self.state["tape"]
        self.bf_label.text = to_human_readable_str(self.program1, False)
        pointer = self.state["pointer"]
        if pointer >= len(self.program1):
            self.running = False
        print(self.round, pointer, self.program1)
        h0 = self.state["head0"]
        h1 = self.state["head1"]
        self.pointer_label.text = (" "*pointer)+"v"+(" "*(63-pointer))

        def address_convert(i):
            if i == h0 and i == h1:
                return "^"
            elif i == h0:
                return "0"
            elif i == h1:
                return "1"
            else:
                return " "
        self.h_label.text = "".join([address_convert(i) for i in range(64)])
        loop_stack = self.state["loop_stack"]
        self.parans_label.text = "".join(["[" if i in loop_stack else " " for i in range(64)])


def update_state(tape, pointer, head0, head1, loop_stack, num_reads, max_reads):
    num_reads += 1
    char = tape[pointer]
    match char:
        case 1:
            head0 = (head0 - 1) % len(tape)
        case 2:
            head0 = (head0 + 1) % len(tape)
        case 3:
            head1 = (head1 - 1) % len(tape)
        case 4:
            head1 = (head1 + 1) % len(tape)
        case 5:
            tape[head0] = tape[head0] - 1
        case 6:
            tape[head0] = tape[head0] + 1
        case 7:
            tape[head1] = tape[head0]
        case 8:
            tape[head0] = tape[head1]
        case 9:
            to_skip_loop = tape[head0] == 0
            if to_skip_loop:
                loop_level = 1
                while loop_level > 0 and pointer < len(tape) - 1 and num_reads < max_reads:
                    num_reads += 1
                    pointer += 1
                    if tape[pointer] == 9:
                        loop_level += 1
                    elif tape[pointer] == 10:
                        loop_level -= 1
            else:
                loop_stack.append(pointer)
        case 10:
            if tape[head0] != 0:
                if len(loop_stack) == 0:
                    pointer = -1
                else:
                    pointer = loop_stack[-1]
            else:
                if len(loop_stack) > 0:
                    loop_stack.pop()
    pointer += 1
    return {
        "tape": tape,
        "pointer": pointer,
        "head0": head0,
        "head1": head1,
        "loop_stack": loop_stack,
        "num_reads": num_reads,
        "max_reads": max_reads
    }

if __name__ == '__main__':
    KivyBf().run()
