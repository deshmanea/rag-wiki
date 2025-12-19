from global_var import Constant

class Retriever:
    def __init__(self, embedder, vector_store, top_k = Constant.TOP_K):
        self.embedder = embedder
        self.vector_store = vector_store
        self.top_k = top_k

    def retrieve(self, query: str):
        # 1. embed query
        query_embedding = self.embedder.generate_embedding([query])[0]
        print(len(query_embedding))

        print(self.vector_store.collection.count())


        # 2. query vector DB
        results = self.vector_store.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=self.top_k,
            include=["documents", "metadatas", "distances"]
        )

        # 3. format results
        retrieved_docs = []
        for i in range(len(results["documents"][0])):
            distance = results["distances"][0][i]
            similarity = 1 - distance

            if similarity >= Constant.SCORE_THRESHOLD:
                retrieved_docs.append({
                    "content": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i],
                    "distance": results["distances"][0][i],
                    "similarity": 1- distance,
                    "rank": i + 1
                    })
                        
        return retrieved_docs
