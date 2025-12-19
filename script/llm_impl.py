from transformers import AutoTokenizer, AutoModelForCausalLM
from global_var import Constant
import ollama

class RAGGenerator:
    def __init__(self, retriever, llm_model_name=Constant.LLM_MODEL, top_k=Constant.TOP_K, max_context_chars=Constant.MAX_CONTEXT_LENGTH):

        self.retriever = retriever
        self.llm_model_name = llm_model_name
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

    def collect_sources(self, retrieved_docs):
        sources = []
        seen = set()

        for doc in retrieved_docs:
            meta = doc["metadata"]
            key = meta.get("source", "") + meta.get("title", "")

            if key not in seen:
                seen.add(key)
                sources.append(meta)

        return sources

    def _build_prompt(self, query, context):
        return f"""
                Answer the following question using only the information provided in the context below.
                If the answer is not contained in the context, respond with "I don't know."

                Context:
                {context}

                Question:
                {query}

                Answer:
            """.strip()

    def generate(self, query: str) -> str:

        retrieved_docs = self.retriever.retrieve(query)[:self.top_k]
        if not retrieved_docs:
            return "No relevant documents found."
        
        sources = self.collect_sources(retrieved_docs)
        context = self._build_context(retrieved_docs)
        prompt = self._build_prompt(query, context)

        # Generate response using Ollama
        response = ollama.generate(
            model=self.llm_model_name,
            prompt=prompt,
            options={"num_predict":self.max_context_chars}
        )
        answer = response['response']
        answer_with_sources = {
            "answer": answer,
            "sources": sources
        }

        return answer_with_sources
