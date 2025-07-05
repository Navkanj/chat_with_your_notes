
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class EmbeddingsIndex:
    def __init__(self):
        self.chunks = []
        self.vectorizer = TfidfVectorizer()
        self.vectors = None

    def build_index(self, chunks):
        """Takes a LIST of text chunks and builds the index"""
        self.chunks = chunks
        self.vectors = self.vectorizer.fit_transform(self.chunks)

    def search(self, query, top_k=3):
        if self.vectors is None:
            return []

        query_vector = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vector, self.vectors).flatten()
        ranked_indices = scores.argsort()[::-1][:top_k]
        return [self.chunks[i] for i in ranked_indices]
