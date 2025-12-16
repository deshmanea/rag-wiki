import os
import numpy as np
import uuid
import chromadb
from global_var import Constant

class VectorStore:

    def __init__(self, collection_name = Constant.COLLECTION_NAME, persist_directory = Constant.PERSIST_DB_PATH):

        self.collection_name = collection_name
        self.persist_directory = persist_directory
        self.client = None
        self.collection = None
        self._initialize_store()

    def _initialize_store(self):

        try:
            os.makedirs(self.persist_directory, exist_ok=True)
            self.client = chromadb.PersistentClient(path=self.persist_directory)

            self.collection = self.client.get_or_create_collection(
                name = self.collection_name,
                metadata={'description':'Wiki text embedding for RAG'}
            )

            print(f'Vector store initialized. Collection: {self.collection_name}')
            print(f'Existing documents in collection: {self.collection.count()}')

        except Exception as e:
            print(f'Error initializing vector store: {e}' )
            raise
    
    def add_documents(self, documents, embeddings):

        if len(documents) != len(embeddings):
            raise ValueError('Number of documents must match number of embeddings')
        
        ids = []
        metadatas = []
        documents_text = []
        embeddings_list = []

        for i, (doc, embedding) in enumerate(zip(documents, embeddings)):
            doc_id = f'doc_{uuid.uuid4().hex[:8]}'
            ids.append(doc_id)

            metadata = dict(doc.metadata)
            metadata['doc_index'] = i
            metadata['content_length'] = len(doc.page_content)
            metadatas.append(metadata)

            documents_text.append(doc.page_content)
            embeddings_list.append(embedding.tolist())

            try:
                self.collection.add(
                    ids = ids,
                    embeddings = embeddings_list,
                    metadatas = metadatas,
                    documents = documents_text
                )

                print(f'Successfully added {len(documents)} documents to vector store')
                print(f'Total documents in collection: {self.collection.count()}')
            
            except Exception as e:
                print(f'Error adding documents to vector store: {e}')
                raise


if __name__ == '__main__':
    vector_store= VectorStore()
    print(vector_store.collection_name)
