from retriever import retrieve_relevant_chunks
from gemini_api import generate_answer

async def handle_query(query):
    context = retrieve_relevant_chunks(query)
    prompt = f"Answer this question: {query}\n\nUse this context:\n{context}"
    return await generate_answer(prompt)
