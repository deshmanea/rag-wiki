from global_var import Constant

from typing import List

class RAGGenerator:
    def __init__(self, retriever, llm_model, top_k=Constant.TOP_K, max_context_chars=Constant.MAX_CONTEXT_LENGTH):

        self.retriever = retriever
        self.llm_model = llm_model
        self.top_k = top_k
        self.max_context_chars = max_context_chars

    def _build_context(self, retrieved_docs):
        context_text = ""
        for doc in retrieved_docs:
            snippet = doc["content"]
            if len(context_text) + len(snippet) > self.max_context_chars:
                remaining = self.max_context_chars - len(context_text)  
                context_text += snippet[:remaining]
                break
            context_text += snippet + "\n\n"
        return context_text.strip()

    def _build_prompt(self, query, context):
        return f"""
                Answer the following question using only the information provided in the context below.
                If the answer is not contained in the context, respond with "I don't know."

                Context:
                {context}

                Question:
                {query}

                Answer:
            """

    def generate(self, query: str) -> str:

        retrieved_docs = self.retriever.retrieve(query)
        retrieved_docs = retrieved_docs[:self.top_k]

        if not retrieved_docs:
            return "No relevant documents found."

        context = self._build_context(retrieved_docs)

        prompt = self._build_prompt(query, context)

        response = self.llm_model.generate(prompt)  # Replace with your model's generate method

        return response
