from fetch_wiki import WikiData
from local_corpus import LocalData
from doc_chunk import ChunkDocWithStrategy
from vector_store import VectorStore
from embed_space import EmbeddingManager
from utils import sanitize_collection_name
from retriever import Retriever
from global_var import Constant
from llm_impl import RAGGenerator

### =========== Get and Save RAW data ==================================#

search_text = 'David Michelangelo'
print(f"Collecting corpus for -> '{search_text}'")
raw_corpus_name = sanitize_collection_name(search_text)
wiki_data = WikiData()
wiki_corpus = wiki_data.get_wiki_corpus(search_text)
print(len(wiki_corpus))
local_data = LocalData()

for i, page_text in enumerate(wiki_corpus):
    file_name = f'{raw_corpus_name}_{i}'
    local_data.save_wiki_corpus_local(file_name, page_text)

### =========== Chunk the RAW data ====================================#

ch = ChunkDocWithStrategy()
chunks = ch.chunk_documents(wiki_corpus)

### =========== Generate Embeddings ===================================#

texts = [chunk.page_content for chunk in chunks] 
embedder = EmbeddingManager(model_name=Constant.MODEL_NAME)
embeddings = embedder.generate_embedding(texts)

### =========== Vectorize Embeddings ==================================#

vector_store = VectorStore(sanitize_collection_name(search_text))
vector_store.add_documents(chunks, embeddings)

### =========== Retrieval==============================================#

retriever = Retriever(embedder, vector_store, top_k=3)
results = retriever.retrieve("Who created the statue of David?")

### =========== Deduplicate ===========================================#
unique = []
seen = set()

for r in results:
    key = r['content'][:Constant.RESULT_LENGTH]   # 120-char
    if key not in seen:
        seen.add(key)
        unique.append(r['content'])

### ========== LLM integration ========================================#

rag_generation = RAGGenerator(retriever)

query = 'Who created the statue of David?'
answer = rag_generation.generate(query)
print(answer)
