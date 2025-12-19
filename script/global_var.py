
class Constant:
     
     # General
     CORPUS_DIR_PATH = 'rag-wiki/corpus'
     JSON_EXTENTION = '.json'
     MODEL_NAME = 'all-miniLM-L6-v2'
     PERSIST_DB_PATH = 'rag-wiki/vector_db'
     COLLECTION_NAME= 'wiki_art_history'

     # Chunking
     CHUNK_SIZE = 500
     CHUNK_OVERLAP = 10

     # Similarity Score
     SCORE_THRESHOLD = 0.30

     # Result
     RESULT_LENGTH = 120
     TOP_K = 8

     # LLM
     MAX_CONTEXT_LENGTH = 2000
