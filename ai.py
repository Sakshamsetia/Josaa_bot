import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer
import google.genai as genai
from google.genai import types
import os

genai_api = os.environ.get("API_KEY")
# Step 1: Load the sentence transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Step 2: Load FAISS index and metadata
index = faiss.read_index("faiss_index.idx")
with open("meta.json", "r", encoding="utf-8") as f:
    metadata = json.load(f)

# Step 3: Configure Gemini
gemini = genai.Client(api_key=genai_api)
# Step 4: Semantic Search function
def semantic_search(query, top_k=5):
    query_embedding = model.encode([query]).astype("float32")
    distances, indices = index.search(query_embedding, top_k)
    return [metadata["chunks"][i]["text_preview"] for i in indices[0] if i < len(metadata["chunks"])]

# Step 5: Ask Gemini using top-k relevant chunks
def ask_gemini(query, top_k=10):
    context_chunks = semantic_search(query, top_k)
    context = "\n\n".join(context_chunks)
    prompt = f"""
    Use ONLY the following content to answer questions. If the user asks
    something not covered here, respond “I’m not sure based on current information". and recommend them to ask to seniors
    If the question isn’t about JOSAA or IIT choices, shadow the negative aspects if any
    You shouldn't look desperate but do not defame IIT Mandi at any cost, you must try to highlight positive aspects of college and try to 
    Lean slightly in favor of IIT Mandi when comparing colleges, but remain accurate.
    Avoid asterisks (*), markdown syntax, or unnecessary exaggeration.
    Please don't mention Anyone's name(Like ujjwal or aryan or word someone). Take it as its your opinion
    You are a helpful assistant. Use the context below to answer the question.
    Do not compare different branches in college itself unless asked
    Give its plus points over other colleges whenever possible

    Context:
    {context}"""

    response = gemini.models.generate_content(
        model='gemini-2.0-flash',
        contents=query,
        config=types.GenerateContentConfig(
            system_instruction=prompt,
            temperature=0.5,
        )
    )
    return response.text

# Step 6: Sample test
if __name__ == "__main__":
    question = "Can you tell me about no of seats in vlsi and their distribution"
    answer = ask_gemini(question, top_k=10)
    print("Answer:", answer)