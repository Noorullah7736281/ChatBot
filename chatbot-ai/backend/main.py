from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import openai
import os
import requests

app = FastAPI()

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

openai.api_key = os.getenv("OPENAI_API_KEY")
SERP_API_KEY = os.getenv("SERPAPI_API_KEY")

def get_search_snippets(query):
    url = "https://serpapi.com/search"
    params = {
        "q": query,
        "api_key": SERP_API_KEY,
        "engine": "google",
    }
    response = requests.get(url, params=params)
    results = response.json()
    snippets = []

    for result in results.get("organic_results", []):
        if "snippet" in result:
            snippets.append(result["snippet"])
    return "\n".join(snippets[:5])  # Use top 5 snippets

@app.post("/ask")
async def ask_question(request: Request):
    data = await request.json()
    question = data.get("question")

    search_data = get_search_snippets(question)

    prompt = f"""Use the information below to answer the user's question:
Information:
{search_data}

Question: {question}
Answer:"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or "gpt-4"
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return {"answer": response.choices[0].message["content"]}