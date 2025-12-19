import json
from pathlib import Path
from global_var import Constant

class LocalData:

    def save_wiki_corpus_local(self, search_text, wiki_corpus):
        corpus_dir_path = Path(Constant.CORPUS_DIR_PATH)
        file_name =  search_text + Constant.JSON_EXTENTION
        corpus_file = corpus_dir_path / file_name 

        corpus_file.parent.mkdir(parents=True, exist_ok=True)     

        wiki_corpus_json = {
            "metadata": wiki_corpus.metadata,
            "content": wiki_corpus.page_content
        }

        if corpus_file.is_file() and corpus_file.stat().st_size > 0:
            print(f'Corpus file {file_name} exists, skipping append !!')
        else:
            print(f'Writing Corpus file {file_name}')
            with open(corpus_file, "w", encoding="utf-8") as json_file:
                json.dump(wiki_corpus_json, json_file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    print("local debug!!")
    search_text = "abc"
    wiki_corpus = "def"
    local_data = LocalData()
    local_data.save_wiki_corpus_local(search_text, wiki_corpus)