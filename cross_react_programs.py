import random


def execute_self_modifying_brainfuck(tape, max_reads=2**13):
    if type(tape) is str:
        tape = to_int_arr(tape)
    head0 = 0
    head1 = 0
    loop_stack = []
    pointer = 0
    num_reads = 0
    while pointer < len(tape) and num_reads < max_reads:
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
                    while loop_level > 0 and pointer < len(tape)-1 and num_reads < max_reads:
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
                        pointer = 0
                        continue
                    else:
                        pointer = loop_stack[-1]
                else:
                    if len(loop_stack) > 0:
                        loop_stack.pop()
        pointer += 1
    return tape


program = [6]
res = execute_self_modifying_brainfuck(program)
assert res == [7]

program = [5]
res = execute_self_modifying_brainfuck(program)
assert res == [4]

program = [0, 6, 6, 6]
res = execute_self_modifying_brainfuck(program)
assert res == [3, 6, 6, 6]

program = [11, 9, 6, 10]
res = execute_self_modifying_brainfuck(program)
assert res == [4106, 9, 6, 10]


def random_program(size=64, min_int=0, max_int=10):
    rand_program = [random.randint(min_int, max_int) for _ in range(size)]
    return to_str(rand_program)


def to_int_arr(as_str, bit_offset=128):
    return [ord(char) - bit_offset for char in as_str]


def to_str(as_int_arr, bit_offset=128):
    as_int_arr = [max(num + bit_offset, 0) for num in as_int_arr]
    return "".join([chr(num) for num in as_int_arr])


def to_human_readable_str(input_arg, with_bolds=True):
    int_arr = input_arg
    if type(input_arg) is str:
        int_arr = to_int_arr(input_arg)

    def int_to_hr_char(_int):
        bf_mapping = {
            0: "0", 1: "<", 2: ">", 3: "{", 4: "}", 5: "-", 6: "+", 7: ".", 8: ",", 9: "[", 10: "]"
        }
        # 0-10 --> brainfuck characters
        if _int in bf_mapping:
            return bf_mapping[_int]
        # -1 to -10 --> "1" to "10"
        elif -10 <= _int < 0:
            return str(_int * -1)
        # 11 to 36 --> "A" to "Z"
        elif 10 < _int <= 26+10:
            return chr(_int + 65 - 11)
        # -11 to -36 --> "a" to "z"
        elif -26-10 <= _int < -10:
            return chr(_int * -1 + 97 - 11)
        # <36 --> "%" (bolded)
        elif _int > 26+10:
            if with_bolds:
                return "\033[1m%\033[0m"
            else:
                return "%"
        # -36< --> "&" (bolded)
        elif _int < -26-10:
            if with_bolds:
                return "\033[1m&\033[0m"
            else:
                return "&"
    return "".join([int_to_hr_char(num) for num in int_arr])


program = [11, 9, 6, 10, 88, -88]
res = to_human_readable_str(program)
assert res == "A[+]\033[1m%\033[0m\033[1m&\033[0m"


def cross_react_programs(a, b):
    a = to_int_arr(a)
    b = to_int_arr(b)
    out = execute_self_modifying_brainfuck(a+b)
    half_len = len(out)//2
    a = out[:half_len]
    b = out[half_len:]
    a = to_str(a)
    b = to_str(b)
    return a, b

