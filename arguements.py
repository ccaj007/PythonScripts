import sys


total = 1
del(sys.argv[0])
for argument in sys.argv:
    try:
        number = int(argument)
        total *= number
    except Exception as e:
        print(e)
        print(f"{argument} is not a number")
        sys.exit(1)

print(total)
