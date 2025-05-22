import chromadb
from sentence_transformers import SentenceTransformer


def load_documents(file_path):
    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def embed_and_store(docs):
    client = chromadb.Client()
    collection = client.get_or_create_collection(name="faq")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(docs)
    for i, doc in enumerate(docs):
        collection.add(documents=[doc], embeddings=[embeddings[i]], ids=[f"id_{i}"])

if __name__ == "__main__":
    docs = load_documents("data/faq.txt")
    embed_and_store(docs)