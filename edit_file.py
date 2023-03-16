with open("numbers.txt") as f:
    lines = f.readlines()

for x in range(len(lines)):
    try:
        number = float(lines[x]) * 2
        lines[x] = f"{number}\n"
    except Exception as e:
        pass

f = open("numbers.txt", "w")
f.writelines(lines)
f.close()
