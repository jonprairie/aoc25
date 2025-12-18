import sys
import math
import itertools
import bisect


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


def p3_2(data):
    def find_largest_n(s, n):
        if n > len(s):
            raise ValueError(f"not enough digits in '{s}', needed {n}.")

        if n == 0:
            return ""

        largest = "" 
        largest_idx = -1
        for i in range( len(s) - n + 1 ):
            if s[i] > largest:
                largest = s[i]
                largest_idx = i

        return largest + find_largest_n(s[largest_idx+1:], n-1)

    total_power = 0
    
    for bank in data:
        power = find_largest_n(bank, 12)
        total_power += int(power)

    return total_power


def p4_1(data):
    PAPER_ROLL = "@"
    PAPER_ROLL_LIMIT = 4
    row_end = len(data)

    DIRS = [
        [-1,1],
        [0,1],
        [1,1],
        [-1,0],
        [1,0],
        [-1,-1],
        [0,-1],
        [1,-1],
    ]

    total_accessible = 0

    for i, row in enumerate(data):
        col_end = len(row)

        for j, col in enumerate(row):
            near_paper_rolls = 0

            if data[i][j] != PAPER_ROLL:
                continue

            for dr, dc in DIRS:
                r = i + dr
                c = j + dc

                if r >= 0 and r < row_end and c >= 0 and c < col_end:
                    if data[r][c] == PAPER_ROLL:
                        near_paper_rolls += 1

            if near_paper_rolls < PAPER_ROLL_LIMIT:
                total_accessible += 1

    return total_accessible


def p4_2(data):
    PAPER_ROLL = "@"
    PAPER_ROLL_LIMIT = 4
    DIRS = [
        [-1,1],
        [0,1],
        [1,1],
        [-1,0],
        [1,0],
        [-1,-1],
        [0,-1],
        [1,-1],
    ]

    def is_accessible(grid, r, c):
        near_paper_rolls = 0
        row_len = len(grid[0])
        col_len = len(grid)

        for dr, dc in DIRS:
            new_r = r + dr
            new_c = c + dc

            if new_r >= 0 and new_r < row_len and new_c >= 0 and new_c < col_len:
                if grid[new_r][new_c] == PAPER_ROLL:
                    near_paper_rolls += 1

        return near_paper_rolls < PAPER_ROLL_LIMIT

    total_accessible = 0
    next_input = []

    for i, row in enumerate(data):
        next_input.append([])
        
        for j, char in enumerate(row):
            if char == PAPER_ROLL:
                if is_accessible(data, i, j):
                    total_accessible += 1
                    next_input[i].append(".")
                else:
                    next_input[i].append("@")
            else:
                next_input[i].append(".")

    next_input = ["".join(row) for row in next_input]

    if total_accessible > 0:
        return total_accessible + p4_2(next_input)
    else:
        return 0


def read_p5_data(data):
    ranges = []
    ids = []

    phase = 0

    for row in data:
        if row == "":
            phase = 1
        elif phase == 0: # ranges
            start, end = row.split("-")

            start = int(start)
            end = int(end)
            
            ranges.append([start, end])
        else: # ids
            ids.append(int(row))

    return ranges, ids
    

def p5_1(data):
    total = 0

    ranges, ids = read_p5_data(data)

    for i in ids:
        fresh = False
        for r in ranges:
            if i >= r[0] and i <= r[1]:
                fresh = True
                break
        if fresh:
            total += 1

    return total


def p5_2(data):
    input_ranges, _ = read_p5_data(data)
    ranges = []
    
    for row in input_ranges:
        lo = bisect.bisect_left(ranges, row[0], key=lambda x: x[1])
        hi = bisect.bisect_right(ranges, row[1], key=lambda x: x[0])

        if hi == lo or lo == len(ranges):
            # no overlap
            ranges.insert(lo, row)
        elif hi - lo == 1:
            # overlap with single item at idx lo
            ranges[lo][0] = min(ranges[lo][0], row[0])
            ranges[lo][1] = max(ranges[lo][1], row[1])
        else:
            # overlap with multiple items from idx lo to idx hi-1
            row[0] = min(ranges[lo][0], row[0])
            row[1] = max(ranges[hi-1][1], row[1])
            del ranges[lo:hi]
            ranges.insert(lo, row)

    total = 0
    for r in ranges:
        total += r[1] - r[0] + 1

    return total


if __name__ == "__main__":
    problem = sys.argv[1]

    if len(sys.argv) > 2:
        phase = sys.argv[2]
    else:
        phase = "1"

    problem_name = f"p{problem}_{phase}"
    
    if problem_name in locals():
        f = locals()[problem_name]

        data_file_name = f"aoc{problem}.data"
        data = read_file_lines(data_file_name)
        print(f(data))
    else:
        print(f"problem not found: {problem} {phase}")
