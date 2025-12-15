import pathlib
from global_var import Constant
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


class ChunkDocWithStrategy:

    def get_all_files_from_folder(self):
        doc_path = pathlib.Path(Constant.CORPUS_DIR_PATH)
        doc_list = list(doc_path.rglob('*'))
        return doc_list
    
    # Since these all files are text skipping loader

    def load_documents(self, files):
        all_file_text = []
        for file in files:
            loader = TextLoader(file, encoding='utf-8')
            documents = loader.load()
            all_file_text.extend(documents)

            for doc in documents:
                print(f"Source: {doc.metadata['source']}")
                print(f"Content: {doc.page_content[:200]}...")

        return all_file_text

    def chunk_documents(self, docs):
        chunks = []
        splitter = RecursiveCharacterTextSplitter(
            chunk_size = 500,
            chunk_overlap = 50,
            length_function=len,
            separators=["\n\n","\n"," " ,""]
        )
        chunks = splitter.split_documents(docs)
        print(len(chunks))
        

if __name__ == '__main__':
    ch = ChunkDocWithStrategy()
    print('Chunk local testing!!')
    files = ch.get_all_files_from_folder()
    full_text = ch.load_documents(files)
    ch.chunk_documents(full_text)

