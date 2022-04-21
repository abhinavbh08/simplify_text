import os
import re
import numpy as np
import glob
from metamap_test import get_concepts
from get_atoms import get_synonyms
from word_finder import find_word_frequency

path = "../abstrct/AbstRCT_corpus/data/test/mixed_test"
files = glob.glob(path + "/*.ann")


for first in files:
    # first = files[88]
    print(first)
    # first = "../abstrct/AbstRCT_corpus/data/test/mixed_test/29527973.ann"
    # first[:-4]+"_edited.txt"
    new_name = "../abstrct/AbstRCT_corpus/data/test/mixed_test/edited/" + os.path.basename(first)[:-4]+"_edited.txt"
    # if os.path.exists(new_name):
    #     continue
    # if "28178150" not in new_name:
    #     continue
    with open(first, "r") as file:
        data = file.read()
    # print(first)
    data = data.split("\n")
    for line in data:
        if len(line)>0 and line[0]=="T":
            line = line.split("\t")
            # simplified_sentence = line[2].lower()
            # print(line[0] + "\t" + line[1] + "\t" + simplified_sentence)

            ordered_concepts, sent = get_concepts(line[2])
            start_idx = 0
            mm_sent = ''
            for concept in ordered_concepts:
                parts = concept[8].split('/')
                end_idx = int(parts[0]) - 1
                mm_sent += sent[start_idx: end_idx]
                replacement_list = []
                replacement = sent[int(parts[0])-1:int(parts[0])-1+int(parts[1])]
                replacement_list.append({"name": concept[3]})
                replacement_list.append({"name": replacement})
                replacement_list += get_synonyms(concept[4])
                
                # sent[int(parts[0])-1:int(parts[0])-1+int(parts[1])]
                if replacement_list:
                    max_cnt = -2
                    for rep in replacement_list:
                        if rep["name"]=="":
                            continue
                        freq = find_word_frequency(rep["name"])
                        if freq > max_cnt:
                            max_cnt = freq
                            replacement = rep["name"]
                mm_sent += replacement
                start_idx = end_idx + int(parts[1])

            # If no concepts are found, copy everything!
            if start_idx != 0:
                mm_sent += sent[start_idx: len(sent)]
            else:
                mm_sent = sent

            print(mm_sent)

            with open(new_name, "a") as file:
                file.write(line[0] + "\t" + line[1] + "\t" + line[2]+"\n")
                file.write(line[0] + "\t" + line[1] + "\t" + mm_sent+"\n\n")