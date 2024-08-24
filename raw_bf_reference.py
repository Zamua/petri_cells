'''
< head0 = head0 - 1
> head0 = head0 + 1
{ head1 = head1 - 1
} head1 = head1 + 1
- tape[head0] = tape[head0] - 1
+ tape[head0] = tape[head0] + 1
. tape[head1] = tape[head0]
, tape[head0] = tape[head1]
[ if (tape[head0] == 0): jump forwards to matching ] command.
] if (tape[head0] != 0): jump backwards to matching [ command.
'''


def execute_brainfuck(code):
    # print("A")
    head0 = 0
    head1 = 0
    tape = [0] * len(code)
    loop_stack = []
    pointer = 0
    while pointer < len(code):
        # print("B")
        char = code[pointer]
        match char:
            case "<":
                head0 = head0 - 1
            case ">":
                head0 = head0 + 1
            case "{":
                head1 = head1 - 1
            case "}":
                head1 = head1 + 1
            case "-":
                tape[head0] = tape[head0] - 1
            case "+":
                tape[head0] = tape[head0] + 1
            case ".":
                tape[head1] = tape[head0]
            case ",":
                tape[head0] = tape[head1]
            case "[":
                if tape[head0] == 0:
                    loop_level = 1
                    while loop_level > 0 and pointer < len(code)-1:
                        # print("C")
                        pointer += 1
                        if code[pointer] == '[':
                            loop_level += 1
                        elif code[pointer] == ']':
                            loop_level -= 1
                else:
                    loop_stack.append(pointer)
            case "]":
                if tape[head0] != 0:
                    pointer = loop_stack[-1]
                else:
                    if len(loop_stack) > 0:
                        loop_stack.pop()
        pointer += 1
    return tape


program = "+>"*100
res = execute_brainfuck(program)
assert res == [1]*100+[0]*100

program = "<+"*100
res = execute_brainfuck(program)
assert res == [0]*100+[1]*100

program = "->"*100
res = execute_brainfuck(program)
assert res == [-1]*100+[0]*100

program = "}}++."
res = execute_brainfuck(program)
assert res == [2, 0, 2, 0, 0]

program = "{{++.--,"
res = execute_brainfuck(program)
assert res == [2, 0, 0, 0, 0, 0, 2, 0]

program = "----[+]"
res = execute_brainfuck(program)
assert res == [0]*len(program)

program = "[+"
res = execute_brainfuck(program)
assert res == [0, 0]

program = "+[+"
res = execute_brainfuck(program)
assert res == [2, 0, 0]

# program = "+[]"
# res = execute_brainfuck(program)
# print(res)
# assert res == [0, 0, 0]