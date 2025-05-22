import chromadb
from sentence_transformers import SentenceTransformer

client = chromadb.Client()
collection = client.get_or_create_collection(name="faq")
model = SentenceTransformer('all-MiniLM-L6-v2')

def retrieve_relevant_chunks(query, top_k=3):
    query_embedding = model.encode([query])[0]
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)
    return "\n".join(results['documents'][0])