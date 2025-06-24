from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        user_prompt = data.get("prompt", "")

        payload = {
            "model": "tinyllama",     # Lighter model for low-RAM systems
            "prompt": f"In 5 lines or less, answer the following: {user_prompt}",
            "stream": False           # TURN OFF streaming to simplify response
        }

        response = requests.post("http://localhost:11434/api/generate", json=payload)

        # This will be a complete JSON object, no need to parse line by line
        response_json = response.json()
        full_response = response_json.get("response", "")

        return {"response": full_response}

    except Exception as e:
        print(f"💥 Error in /chat: {e}")
        return {"error": str(e)}
