from pathlib import Path
from global_var import Constant

class LocalData:

    def save_wiki_corpus_local(self, search_text, wiki_corpus):
        corpus_dir_path = Constant.CORPUS_DIR_PATH
        file_name =  search_text + Constant.TEXT_EXTENTION
        file_path = corpus_dir_path + "/" + file_name
        print(Path.cwd())
        corpus_file = Path(file_path)


        if corpus_file.is_file() and corpus_file.stat().st_size > 0:
            print(f'Corpus file {file_name} exists, skipping append !!')
        else:
            print(f'Writing Corpus file {file_name}')
            with open(file_path, "w", encoding='utf-8') as file:
                file.write(wiki_corpus)


if __name__ == "__main__":
    print("local debug!!")
    search_text = "abc"
    wiki_corpus = "def"
    local_data = LocalData()
    local_data.save_wiki_corpus_local(search_text, wiki_corpus)