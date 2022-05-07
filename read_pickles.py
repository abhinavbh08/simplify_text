import pickle

with open('dkt_names.pickle', 'rb') as handle:
    dkt_names = pickle.load(handle)

with open('words_files.pickle', 'rb') as handle:
    words_files = pickle.load(handle)

cnt = 0
print("abc")
with open("synonyms_ranked.txt", "a") as file:
    for k, v in dkt_names.items():
        v = sorted(v, key=lambda x: x[1], reverse=True)
        file.write(str(cnt)+"\n")
        file.write(k+"\n")
        for item in v:
            file.write(str(item[0])+"\t"+str(item[1])+"\n")
        file.write("\n\n")
        cnt+=1

for line in words_files:
    with open("files_replacement.txt", "a") as file:
        file.write("\t".join(line))
        file.write("\n")
