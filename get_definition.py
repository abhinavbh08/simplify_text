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
import string
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

    # ordered_concepts, sent = get_concepts(sent_test)
    # cnt_addeds = 0
    # for concept in ordered_concepts:
    #     parts = concept[8].split('/')
    #     rep = sent[int(parts[0])-1:int(parts[0])-1+int(parts[1])]
    #     if len(rep)>2 and rep not in stopwords.words("english") and not wordnet.synsets(rep):
    #         cnt_addeds+=1
    # return cnt_addeds

# print(cnt_eng_words("Clinical hypoglycemia has diverse etiologies."))

# def cnt_synset_words(sent_test):

#     cnt = 0
#     for word in nltk.word_tokenize(sent_test.lower()):
#         if word in string.punctuation:
#             continue
#         if word in stopwords.words('english'):
#             continue
#         if not wordnet.synsets(word):
#             cnt+=1
#     return cnt


# print(cnt_synset_words("A syndrome of abnormally low BLOOD GLUCOSE level"))


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

    flag = True
    if len(word)<=4 and all([True if c in string.ascii_uppercase else False for c in word]):
        flag = False

    ## Google search results
    if flag==True and len(senses)==0:
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

    return replacement

# get_definition("C0022646", "CHB")