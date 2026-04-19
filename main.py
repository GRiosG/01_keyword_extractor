"""
Project Keyword Extractor
-------------------------
Extracts structured keywords from a project description using response_mime_type="application/json" for valid JSON
output.
"""

# Imports --------------------------------------------------------------------------------------------------------------
import json
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

load_dotenv()

# APP initialization ---------------------------------------------------------------------------------------------------
app = FastAPI(
    title = 'Project Keyword Extractor',
    description = 'Extract structured keywords from a project description using an LLM api call - Gemini Flash.',
    version = '1.0',
)

client = genai.Client(api_key=os.environ['GEMINI_API_KEY'])

# Pydantic Schemas (in-out) --------------------------------------------------------------------------------------------
class ProjectInput(BaseModel):
    """Request body: free-text project description."""
    project_description: str

class ExtractedKeywords(BaseModel):
    """Response body: a list of keyword strings."""
    keywords: list[str]

# Prompt template ------------------------------------------------------------------------------------------------------
SYSTEM_PROMPT="""
You are a technical keyword extractor. Given a project description, return a JSON object with a single key "keywords"
whose value is a list of concise, relevant keywords of short phrases (2-4 words maximum each).

Focus on:
- Technologies and frameworks mentioned or implied
- Domain concepts (e.g. "natural language processing", "authentication")
- Key actions or patterns (e.g. "real-time updates", "REST API")

Return ONLY valid JSON. No markdown, no explanation, no code fences.

Example output:
{"keywords": ["FastAPI", "REST API", "Pydantic validation", "async Python"]} 
"""

# Endpoint -------------------------------------------------------------------------------------------------------------
@app.post("/extract-keywords", response_model=ExtractedKeywords)
async def extract_keywords(payload: ProjectInput) -> ExtractedKeywords:
    """
    Extract keywords from a project description using Gemini Flash.
    """
    response = await client.aio.models.generate_content(
        model = "gemini-flash-latest",
        contents = payload.project_description,
        config = types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            response_mime_type="application/json",
        ),
    )

    # Parsing the guaranteed JSON string into a Python dictionary
    try:
        data = json.loads(response.text)
    except json.JSONDecodeError as exc:
        # Just in case...
        raise HTTPException(
            status_code = 502,
            detail = f"Gemini returned non-JSON output: {exc}",
        ) from exc

    # Pydantic output validation
    return ExtractedKeywords(**data)

# Health check ---------------------------------------------------------------------------------------------------------
@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}