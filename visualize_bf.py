from kivy.uix.label import Label
from cross_react_programs import to_str, to_human_readable_str, random_program, to_int_arr
from kivy.uix.floatlayout import FloatLayout
from kivy_ui import StandardUI


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


class BrainfuckExecutor:
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

    def init_content(self, layout):
        self.text_layout = FloatLayout()

        self.parans_label = self.add_label(" " * 64, 0)
        self.pointer_label = self.add_label("v"+" "*63, 50)
        bf_text = to_human_readable_str(self.program1, False)
        self.bf_label = self.add_label(bf_text, 100)
        self.h_label = self.add_label("^" + " " * 63, 150)

        layout.add_widget(self.text_layout)

    def update_state(self):
        self.state = update_state(**self.state)

    def update_content(self):
        self.program1 = self.state["tape"]
        self.bf_label.text = to_human_readable_str(self.program1, False)
        pointer = self.state["pointer"]
        if pointer >= len(self.program1):
            self.running = False
        num_reads = self.state["num_reads"]
        print(num_reads, pointer, self.program1)
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

    def add_label(self, text, y_down):
        label = Label(
            text=text,
            halign="left",
            valign="middle",
            font_name="Courier_Prime/CourierPrime-Regular.ttf",
            pos=(0, self.text_layout.height - y_down),
            size=(300, 10)
        )
        self.text_layout.add_widget(label)
        return label


if __name__ == '__main__':
    initial_state = None
    StandardUI(BrainfuckExecutor(), initial_state).run()
