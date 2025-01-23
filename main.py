from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import json
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware


import google.generativeai as genai

# ------------------------------------------------------------
# 1. Load environment variables and configure Gemini API key
# ------------------------------------------------------------
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # from .env
if not GEMINI_API_KEY:
    raise ValueError("Missing GEMINI_API_KEY environment variable.")

genai.configure(api_key=GEMINI_API_KEY)

# ------------------------------------------------------------
# 2. Initialize the Gemini Pro model
# ------------------------------------------------------------
model = genai.GenerativeModel("gemini-pro")

# ------------------------------------------------------------
# 3. Create FastAPI application
# ------------------------------------------------------------
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)



# ------------------------------------------------------------
# 4. Define data models
# ------------------------------------------------------------
class MCQ(BaseModel):
    question: str
    options: List[str]
    correct_answer: str


# ------------------------------------------------------------
# 5. Helper functions
# ------------------------------------------------------------
def load_data(file_path: str):
    """Load JSON data from a file."""
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"JSON file not found: {file_path}")
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format")


def generate_mcq_with_gemini_pro(raw_text: str, main_topic: str):
    """
    Generates a single MCQ using the 'gemini-pro' model via `model.generate_content`.
    We request JSON in the prompt for easier parsing.
    """
    prompt = f"""
Generate a multiple-choice question (MCQ) based on the following text:

Text: {raw_text}

Main Topic: {main_topic}

Requirements:
1. A clear and concise question.
2. One correct answer.
3. Three plausible but incorrect distractors.

Output strictly in valid JSON (without extra commentary) using this schema:
{{
  "question": "...",
  "correct_answer": "...",
  "distractors": ["...","...","..."]
}}
"""

    try:
        # Call gemini-pro with generate_content
        response = model.generate_content(prompt)

        # If no response text, return None
        if not response or not response.text:
            return None

        generated_text = response.text.strip()

        # Convert the string to a Python dict
        mcq_data = json.loads(generated_text)
        return mcq_data
    except Exception as e:
        print("Error generating MCQ:", e)
        return None


# ------------------------------------------------------------
# 6. Define FastAPI endpoints
# ------------------------------------------------------------
@app.get("/generate-mcqs/", response_model=List[MCQ])
def generate_mcqs():
    try:
        # Adjust the path to your JSON file as necessary
        data = load_data("challenge_data/challenge_nikola/economics.json")

        chunks = [item for item in data if item.get('type') == 'chunk']
        mcq_list = []

        for chunk in chunks:
            content = chunk.get('content', {})
            if 'main_topic' not in content or 'text' not in content:
                continue

            main_topic = content['main_topic']
            raw_text = content['text']

            mcq_data = generate_mcq_with_gemini_pro(raw_text, main_topic)
            if mcq_data:
                # Construct the MCQ object
                mcq_list.append(
                    MCQ(
                        question=mcq_data["question"],
                        options=[mcq_data["correct_answer"]] + mcq_data["distractors"],
                        correct_answer=mcq_data["correct_answer"]
                    )
                )

        return mcq_list

    except Exception as e:
        print("Error in /generate-mcqs/:", str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def read_root():
    return {"message": "Welcome to the Studyflash MCQ Generator API with Gemini Pro!"}
