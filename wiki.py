import wikipedia

print(wikipedia.summary("atherogenesis"))


import wikipediaapi


wiki_wiki = wikipediaapi.Wikipedia('en')

page_py = wiki_wiki.page('Hypertension')

print(page_py.summary)

wiki_wiki = wikipediaapi.Wikipedia('simple')

page_py = wiki_wiki.page('Hypertension')

print(page_py.summary)