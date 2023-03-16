import sys

file_name = "todos.txt"

# read file
try:
    with open(file_name) as f:
        lines = f.readlines()
except:
    pass

# add todo
if len(sys.argv) >= 3 and sys.argv[1].lower() == "add":
    lines.append(f"{sys.argv[2]}\n")

# remove todo
if len(sys.argv) >= 3 and sys.argv[1].lower() == "remove":
    try:
        index_delete = int(sys.argv[2])
        if index_delete < 1:
            print(f"{sys.argv[2]} is not valid")
            sys.exit(1)
        index_delete -= 1
        del(lines[index_delete])

    except Exception as e:
        print(e)
        sys.exit(1)

# save file
f = open(file_name, "w")
f.writelines(lines)
f.close()

# print list
print("\nHere's your ToDo list:\n")
for x in range(len(lines)):
    print(f"{x+1}. {lines[x]}", end="")

# print Commands
print("\n****************************\n")
print(f"To view ToDos:\n{sys.argv[0]}")
print(f"To Add a ToDo:\n{sys.argv[0]} add \"Clean Room\"\n")
print(f"To remove a ToDo:\n{sys.argv[0]} remove 2\n")

