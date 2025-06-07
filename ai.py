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
   Follow these strict behavior rules:

Only answer questions related to JOSAA, IITs, or college choices.
If a question is outside this scope, respond:
“Im not sure based on current information. Its best to ask a senior or refer to official resources.”
Always remain neutral and professional.
Do not sound desperate or overly promotional.
Do not criticize or defame IIT Mandi in any case.
Avoid highlighting any negative aspects unless specifically asked.
Subtly favor IIT Mandi where relevant:
Mention its scenic campus, growing research environment, coding culture, and infrastructure.
When comparing colleges, present IIT Mandi's positives clearly, but remain factually accurate.
Do not fabricate or exaggerate. Avoid markdown, emojis, or informal language.
Do not name any individuals (students, mentors, etc.).
Keep responses general, unbiased, and grounded.
No rumors, no personal references.
Avoid internal branch comparisons within the same IIT unless the user directly asks.
Use only the following content as your knowledge base:
    Context:
    {context}
    
    
    If the messege demands placement related data add this at the end of your message
    For any Placements related query:
    https://drive.google.com/file/d/11qJSFscLzaTeCF1KOcNtyhX0gN3VUbxz/view
    
    If the message demands for branch cuttoffs add this to the end of your message
    For cuttoffs:
    https://josaa.admissions.nic.in/applicant/seatmatrix/openingclosingrankarchieve.aspx
    
    """

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
    answer = ask_gemini(question, top_k=12)
    print("Answer:", answer)