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
def semantic_search(query, top_k):
    query_embedding = model.encode([query]).astype("float32")
    distances, indices = index.search(query_embedding, top_k)
    return [metadata["chunks"][i]["text_preview"] for i in indices[0] if i < len(metadata["chunks"])]


def load_system_prompt(file_path="./system.txt"):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        return f'''"""{content}"""'''
    except FileNotFoundError:
        return '"""System prompt file not found."""'

# Step 5: Ask Gemini using top-k relevant chunks
def ask_gemini(query, top_k=10):
    context_chunks = semantic_search(query, top_k)
    context = "\n\n".join(context_chunks)
    sys_prompt = load_system_prompt()
    prompt = f"""
You are a telegram bot created by IIT Mandi for answering JOSAA Related Queries
You are to answer josaa related queries
system instructions: {sys_prompt}
    
You have this data to answer doubts
context: {context}
    
"""

    response = gemini.models.generate_content(
        model='gemini-2.0-flash',
        contents=query,
        config=types.GenerateContentConfig(
            system_instruction=prompt,
            temperature=0.9
        )
    )
    print(f"Response : {response.text}")
    return response.text

# Step 6: Sample test
if __name__ == "__main__":
    question = "Can you tell me about vlsi"
    answer = ask_gemini(question, top_k=12)
    print("Answer:", answer)