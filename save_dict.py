import pickle
from collections import Counter

# a = {'hello': 'world'}

# with open('filename.pickle', 'wb') as handle:
#     pickle.dump(a, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('sem_types.pickle', 'rb') as handle:
    cnts = pickle.load(handle)

with open('sem_examples.pickle', 'rb') as handle:
    examples = pickle.load(handle)

cnts = dict(sorted(cnts.items(), key=lambda x: x[1], reverse=True))
for ind, k in enumerate(cnts.keys()):
    sorted_examples = sorted(list(Counter(examples[k]).items()), key = lambda x: x[1], reverse=True)[:10]
    ex_str = k
    for item in sorted_examples:
        ex_str += "\t" + item[0] + "(" + str(item[1]) + ")"
    ex_str+="\n\n"    

    with open("semantic_types.txt", "a") as file:
        file.write(ex_str)
