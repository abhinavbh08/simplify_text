import glob

path = "../abstrct/AbstRCT_corpus/data/test/mixed_test"
files = glob.glob(path + "/*.ann")
first = files[88]
print(first)
# first = "../abstrct/AbstRCT_corpus/data/test/mixed_test/29527973.ann"
new_name = first[:-4]+"_edited.txt"

with open(new_name, "a") as file:
    file.write("This is so cool."+"\n")

with open(new_name, "a") as file:
    file.write("Yes this is very very cool."+"\n")