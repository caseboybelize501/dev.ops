import chromadb
import json
from sentence_transformers import SentenceTransformer

class IncidentStore:
    """
    Stores and retrieves incidents using ChromaDB for similarity search.
    """

    def __init__(self):
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection("incidents")
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')

    def store_incident(self, incident_data: dict):
        """
        Store an incident in the database.
        """
        try:
            # Embed the incident description for similarity search
            embedding = self.embedder.encode(incident_data.get("description", ""))
            
            self.collection.add(
                documents=[incident_data["description"]],
                metadatas=[{
                    "root_cause": incident_data["root_cause"],
                    "fix_applied": incident_data["fix_applied"],
                    "timestamp": incident_data.get("timestamp", time.time())
                }],
                embeddings=[embedding.tolist()],
                ids=[f"incident_{int(time.time())}"]
            )
        except Exception as e:
            print(f"Error storing incident: {e}")

    def search_similar_incidents(self, query: str, top_k: int = 5) -> list:
        """
        Search for similar incidents using vector similarity.
        """
        try:
            embedding = self.embedder.encode(query)
            results = self.collection.query(
                query_embeddings=[embedding.tolist()],
                n_results=top_k
            )
            return results["metadatas"]
        except Exception as e:
            print(f"Error searching incidents: {e}")
            return []