with open("./input.txt", "r") as f:
    lines = f.readlines()

numbers = []
for line in lines:
    first_digit = ""
    last_digit = ""
    for char in line:
        if char.isdigit():
            first_digit = char
            break

    for char in reversed(line):
        if char.isdigit():
            last_digit = char
            break

    numbers.append(int(f"{first_digit}{last_digit}"))

print(sum(numbers))
