#################################################################################################
# usage of the script
# usage: python retrieve-cui-or-code.py -k APIKEY -v VERSION -i IDENTIFIER -s SOURCE
# If you do not provide the -s parameter, the script assumes you are retrieving information for a
# known UMLS CUI
#################################################################################################

from Authentication import *
import requests
import json
import argparse
import heapq as hq
from googleapi import google
import nltk
import time
from word_finder import find_word_frequency
from nltk.corpus import wordnet
import wikipediaapi
from metamap_test import get_concepts

# parser = argparse.ArgumentParser(description='process user given parameters')
#parser.add_argument("-u", "--username", required =  True, dest="username", help = "enter username")
#parser.add_argument("-p", "--password", required =  True, dest="password", help = "enter passowrd")
# parser.add_argument("-k", "--apikey", required = True, dest = "apikey", help = "enter api key from your UTS Profile")
# parser.add_argument("-v", "--version", required =  False, dest="version", default = "current", help = "enter version example-2015AA")
# parser.add_argument("-i", "--identifier", required =  True, dest="identifier", help = "enter identifier example-C0018787")
# parser.add_argument("-s", "--source", required =  False, dest="source", help = "enter source name if known")

# args = parser.parse_args()

#username = args.username
#password = args.password
# apikey = args.apikey
# version = args.version
# identifier = args.identifier
# source = args.source

apikey = "1214614b-5188-463a-92f4-1365a18813cf"
version = "current"
# cui = "C0027051"
AuthClient = Authentication(apikey)

###################################
#get TGT for our session
###################################

tgt = AuthClient.gettgt()
uri = "https://uts-ws.nlm.nih.gov"

# try:
#    source
# except NameError:
#    source = None

##if we don't specify a source vocabulary, assume we're retrieving UMLS CUIs
# if source is None:
#     content_endpoint = "/rest/content/"+str(version)+"/CUI/"+str(identifier)

# else:
#     content_endpoint = "/rest/content/"+str(version)+"/source/"+str(source)+"/"+str(identifier)
import string
from nltk.corpus import stopwords

with open("sem_types.txt", "r") as file:
    sts = file.read().split("\n")


dkt_fullforms = {}
for line in sts:
    line = line.split("|")
    dkt_fullforms[line[0]] = line[2]


def cnt_eng_words(sent_test):
    cnt = 0
    for word in nltk.word_tokenize(sent_test.lower()):
        if word in string.punctuation:
            continue
        if word in stopwords.words('english'):
            continue
        if not wordnet.synsets(word):
            cnt+=1
    return cnt


def get_definition(cui, word):
    content_endpoint = "/rest/content/2020AA/CUI/" + cui + "/definitions"
    # content_endpoint = "rest/content/2020AA/CUI/" + cui + "/definitions"	
    ##ticket is the only parameter needed for this call - paging does not come into play because we're only asking for one Json object
    query = {'ticket':AuthClient.getst(tgt)}
    r = requests.get(uri+content_endpoint,params=query)
    r.encoding = 'utf-8'
    items  = json.loads(r.text)
    try:
        jsonData = items["result"]
    except:
        jsonData = []
    # for data in jsonData:
    #     print(data["name"], data['rootSource'])

    h = []
    for data_item in jsonData:
        if data_item["rootSource"] == "MSH":
            # hq.heappush(h, (1, data_item["value"]))
            h.append(data_item["value"])
        elif data_item["rootSource"] == "NCI":
            # hq.heappush(h, (2, data_item["value"]))
            h.append(data_item["value"])
        elif data_item["rootSource"] == "SNOMEDCT_US":
            # hq.heappush(h, (3, data_item["value"]))
            h.append(data_item["value"])
    # if len(h)>0:
    #     full_text = hq.heappop(h)[1]
    #     return nltk.sent_tokenize(full_text)[0]
    # word = "abc"
    # time.sleep(10)

    senses = []
    for sense in h:
        descs = nltk.sent_tokenize(sense)
        senses += descs[:min(len(descs), 5)]

    wiki_wiki = wikipediaapi.Wikipedia('simple')
    page_py = wiki_wiki.page(word)
    if page_py.summary != "":
        descs = nltk.sent_tokenize(page_py.summary)
        senses += descs[:min(len(descs), 3)]


    ## Wikipedia
    wiki_wiki = wikipediaapi.Wikipedia('en')
    page_py = wiki_wiki.page(word)
    if page_py.summary != "":
        descs = nltk.sent_tokenize(page_py.summary)
        senses += descs[:min(len(descs), 3)]
    # print(page_py.summary)


    ## Google search results
    cnt_res = 0
    search_results = google.search(word, 1)
    for sres in search_results:
        if sres.description:
            descs = nltk.sent_tokenize(sres.description)
            senses += descs[:min(len(descs), 3)]
            cnt_res+=1
        if cnt_res==2:
            break
    
    max_cnt = 10000
    replacement = ""
    for rep in senses:
        if len(rep.split()) < 5:
            continue
        freq = cnt_eng_words(rep)
        if freq < max_cnt:
            max_cnt = freq
            replacement = rep
    if replacement=="":
        return replacement

    ordered_concepts, sent = get_concepts(replacement)
    start_idx = 0
    cnt_addeds = 0
    mm_sent = ''
    for concept in ordered_concepts:
        parts = concept[8].split('/')
        end_idx = int(parts[0]) - 1
        mm_sent += sent[start_idx: end_idx]
        rep = sent[int(parts[0])-1:int(parts[0])-1+int(parts[1])]
        part_to_add = ""
        if len(rep)>2 and rep not in stopwords.words("english") and not wordnet.synsets(rep):
            lst_concepts_short = concept[5][1:-1].split(",")
            if "phsu" in lst_concepts_short:
                lst_concepts_short = ["phsu"]
            lst_concepts_full = [dkt_fullforms[sm_type] for sm_type in lst_concepts_short]
            part_to_add = " (" + "/".join(lst_concepts_full) + ")"
            cnt_addeds+=1
        mm_sent += rep + part_to_add
        start_idx = end_idx + int(parts[1])

    # If no concepts are found, copy everything!
    if start_idx != 0:
        mm_sent += sent[start_idx: ]
    else:
        mm_sent = sent

    if cnt_addeds > 0:
        return ""
    return mm_sent

# get_definition("C0020538", "Hypertension")
