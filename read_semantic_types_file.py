with open("sem_types.txt", "r") as file:
    data = file.read().split("\n")

dkt = {}
for line in data:
    line = line.split("|")
    dkt[line[0]] = line[2]

print(dkt)