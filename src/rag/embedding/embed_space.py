from sentence_transformers import SentenceTransformer
from rag.config.global_var import Constant

class EmbeddingManager:

    def __init__(self, model_name: str = Constant.MODEL_NAME):

        self.model_name = model_name
        self.model = None
        self._load_model()

    def _load_model(self):
        try:
            print(f"Loading embedding model: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
            print(f"Model is loaded successfully. Embedding dimensions {self.model.get_sentence_embedding_dimension()}")
        except Exception as e:
            print(f"Error loading the model {self.model_name}:{e}") 
            raise

    def generate_embedding(self, texts):

        if not self.model:
            raise ValueError("Model is not loaded")

        print(f"Generating embedding for {len(texts)} texts.")
        embeddings = self.model.encode(texts, show_progress_bar=True)
        print(f"Generated embeddings with shape: {embeddings.shape}")
        return embeddings