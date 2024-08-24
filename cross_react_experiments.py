import random
from cross_react_programs import cross_react_programs, random_program, to_human_readable_str

round_outcome = {"looping": 0, "timed out": 1}


# create 2 random brainfuck programs and run them against each other repeatedly using cross_react_programs()
def execute_cycle(num_rounds):
    x = random_program()
    y = random_program()
    first, second = to_human_readable_str(x), to_human_readable_str(y)
    print(f"round 0 : {first} {second}")
    seen = set()
    for curr_round in range(1, num_rounds):
        x, y = cross_react_programs(x, y)
        first, second = to_human_readable_str(x), to_human_readable_str(y)
        if (x, y) in seen:
            pad = " " if curr_round < 10 else ""
            print(f"round {curr_round}{pad}: terminal: {first} {second}\n")
            return round_outcome["looping"]
        seen.add((x, y))
        pad = " " if curr_round < 10 else ""
        print(f"round {curr_round}{pad}: {first} {second}")
    print("")
    return round_outcome["timed out"]


# run execute_cycle several times and print the results
def run_experiments(max_runs=25, max_rounds=50):
    num_looping = 0
    num_timed_out = 0
    for run in range(max_runs):
        print(f"run {run}")
        outcome = execute_cycle(max_rounds)
        if outcome == round_outcome["looping"]:
            num_looping += 1
        elif outcome == round_outcome["timed out"]:
            num_timed_out += 1
    print(f"{num_looping} ({100*num_looping/max_runs}% of) runs were looping")
    print(f"{num_timed_out} ({100*num_timed_out/max_runs}% of) runs timed out")


run_experiments()

