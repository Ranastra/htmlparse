# gets all important lines from htmlparse.py and prints them

with open("htmlparse.py", "r") as file:
    lines = file.readlines()

a = []
for line in lines:
    if "class " in line: a.append("\n")
    if " def " in line or "class " in line: a.append(line)
    if "@" in line: a.append(line.strip())

print("".join(a)) 