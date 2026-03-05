import chromadb
import json
from sentence_transformers import SentenceTransformer
import time

class SolutionLibrary:
    """
    Stores and retrieves solution patterns.
    """

    def __init__(self):
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection("solutions")
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')

    def store_pattern(self, pattern_data: dict):
        """
        Store a solution pattern in the library.
        """
        try:
            # Embed the failure signature for similarity search
            embedding = self.embedder.encode(pattern_data.get("failure_signature", ""))
            
            self.collection.add(
                documents=[pattern_data["failure_signature"]],
                metadatas=[{
                    "pattern_name": pattern_data["pattern_name"],
                    "root_cause_class": pattern_data["root_cause_class"],
                    "solution_template": pattern_data["solution_template"],
                    "applicability_conditions": pattern_data["applicability_conditions"],
                    "confidence": pattern_data["confidence"],
                    "tags": pattern_data["tags"],
                    "created_at": time.time()
                }],
                embeddings=[embedding.tolist()],
                ids=[f"solution_{int(time.time())}"]
            )
        except Exception as e:
            print(f"Error storing solution: {e}")

    def search_similar_solutions(self, query: str, top_k: int = 5) -> list:
        """
        Search for similar solutions using vector similarity.
        """
        try:
            embedding = self.embedder.encode(query)
            results = self.collection.query(
                query_embeddings=[embedding.tolist()],
                n_results=top_k
            )
            return results["metadatas"]
        except Exception as e:
            print(f"Error searching solutions: {e}")
            return []