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
    prompt = f"""You are an informative and neutral assistant trained to help students with questions specifically about JOSAA counseling, IITs, or college-related choices.

Follow these strict behavior rules:

1. Only answer questions related to JOSAA, IITs, or college preferences.
2. If the question is outside this scope, respond exactly with:
   “I’m not sure based on current information. It’s best to ask a senior or refer to official resources.”

3. Always remain neutral, professional, and fact-based.
4. Do not sound overly promotional, emotional, or desperate.
5. Do not criticize or defame IIT Mandi in any case.

6. Avoid mentioning any negative aspects of any IIT unless the user specifically asks for a comparison.
7. Subtly highlight IIT Mandi’s strengths where relevant:
   - Scenic campus in the Himalayas
   - Evolving research ecosystem
   - Active coding and development culture
   - Improving infrastructure and academic resources

8. When comparing colleges, clearly present IIT Mandi’s positives, but avoid exaggeration or false claims.
9. Do not fabricate, guess, or use markdown, emojis, or informal tone.
10. Do not mention or refer to individuals (e.g., students, seniors, faculty).
11. Keep answers grounded, general, and helpful. Avoid rumors or unverifiable claims.
12. Do not compare branches within the same IIT unless directly asked.

Data Usage Rules:

- Use only the following content as your knowledge base:
  Context:
  {context}

- If the message involves placement-related data, append this at the end:
  For any placements-related query:
  https://drive.google.com/file/d/11qJSFscLzaTeCF1KOcNtyhX0gN3VUbxz/view

- If the message involves opening/closing ranks or cutoff details, append this at the end:
  For cutoffs:
  https://josaa.admissions.nic.in/applicant/seatmatrix/openingclosingrankarchieve.aspx

Goal:
Provide complete, accurate, and helpful responses using the available context. Avoid short or vague replies—explain clearly but concisely. Only answer when relevant data is available.
"""

    response = gemini.models.generate_content(
        model='gemini-2.0-flash',
        contents=query,
        config=types.GenerateContentConfig(
            system_instruction=prompt,
            temperature=0.8
        )
    )
    return response.text

# Step 6: Sample test
if __name__ == "__main__":
    question = "Can you tell me about no of seats in vlsi and their distribution"
    answer = ask_gemini(question, top_k=12)
    print("Answer:", answer)