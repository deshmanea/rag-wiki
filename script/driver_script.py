from fetch_wiki import WikiData
from local_corpus import LocalData

search_text = 'David (Michelangelo)'
wiki_data = WikiData()
wiki_corpus = wiki_data.get_wiki_corpus(search_text)
print(len(wiki_corpus))

local_data = LocalData()
local_data.save_wiki_corpus_local(search_text, wiki_corpus)

