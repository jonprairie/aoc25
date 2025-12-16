import math
import itertools


def read_file_lines(fl):
    with open(fl) as f:
        return f.read().splitlines()


def p1_1(data):
    counter = 0
    location = 50

    for rot in data:
        direction = rot[0]
        value = int( rot[1:] )

        if direction == "L":
            value *= -1

        location += value

        if location % 100 == 0:
            counter += 1

    return counter


def p1_2(data):
    counter = 0
    location = 50

    for rot in data:
        direction = rot[0]
        value = int( rot[1:] )

        counter += value // 100
        value %= 100

        if direction == "L":
            value *= -1

        location %= 100
        started_on_zero = location == 0
        location += value

        if location <= 0 or location >= 100:
            if not started_on_zero:
                counter += 1

    return counter


def p2_1(data):
    ranges = data[0].split(",")

    counter = 0

    for r in ranges:
        start, end = r.split("-")

        start = int(start)
        end = int(end)

        for num in range(start, end+1):
            digits = 1 + math.floor( math.log10(num) )

            if digits % 2 != 0:
                continue
            
            half_digits = digits / 2
            pivot = 10**half_digits

            if num % pivot == num // pivot:
                counter += num

    return counter


def p2_2(data):
    def digits(n):
        return 1 + math.floor( math.log10(n) )
    def get_divisibles(n):
        num_digits = digits(n)
        return [i for i in range(1, num_digits//2+1) if num_digits%i==0]

    ranges = data[0].split(",")

    counter = 0

    for r in ranges:
        start, end = r.split("-")

        start = int(start)
        end = int(end)

        for num in range(start, end+1):
            divisibles = get_divisibles(num)

            num_str = str(num)
            invalid = False
            
            for divisible in divisibles:
                batched_num = ["".join(sub) for sub in itertools.batched(num_str, divisible)]

                if all([sub==batched_num[0] for sub in batched_num]):
                    invalid = True

            if invalid:
                counter += num

    return counter


def p3_1(data):
    total_power = 0
    
    for bank in data:
        right_max_lookup = []
        largest_to_right = -1
        largest = -1 # doesn't include last digit since it can't be in the tens place
        largest_idx = -1
        idx = len(bank) - 1

        while idx >= 0:
            digit = int(bank[idx])
            right_max_lookup.insert(0, largest_to_right)
            if digit > largest_to_right:
                largest_to_right = digit
            if digit >= largest and idx != (len(bank) - 1):
                largest = digit
                largest_idx = idx
            idx -= 1

        power = 10*largest + right_max_lookup[largest_idx]

        total_power += power

    return total_power


problem_table = {
    "p1_1": ["aoc1_1.data", p1_1],
    "p1_2": ["aoc1_1.data", p1_2],
    "p2_1": ["aoc2_1.data", p2_1],
    "p2_2": ["aoc2_1.data", p2_2],
    "p3_1": ["aoc3_1.data", p3_1]

}


def ex(problem_key):
    problem = problem_table[problem_key]
    f = problem[1]
    data = read_file_lines(problem[0])
    print(f(data))


if __name__ == "__main__":
    ex("p3_1")
