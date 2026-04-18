# Project Keyword Extractor
A minimal FastAPI service that takes a free-text description of a project and
returns a structured list of keywords (powered by Gemini 1.5 Flash).

This project is part of a personal series on AI/ML Engineering, exploring how
to build reliable, structured pipelines on top of LLMs. This is the very first
and most basic implementation of the series.

## What it features:

* Structured LLM output: `response_mime_type=application/json` forces valid
JSON from the model.
* Request/response contracts: Pydantic `BaseModel` validates both the input and
output.
* Non-blocking I/O: `async def` + `await` lets the server handle concurrent
requests during the LLM call.
* Modern dependency management: `uv` replaces pip+virtualenv in a single tool.

## Stack:

* FastAPI - HTTP framework with automatic validation and `/docs` UI.
* Uvicorn - ASGI server running the app.
* Pydantic v2 - data validation and schema enforcement.
* Google Generative AI SDK - Gemini 1.5 Flash client.
* uv - project and dependency management.

## Project structure:
01_keyword_extractor/
├── main.py           # All application code (single-file in this case)
├── pyproject.toml    # Project metadata and dependencies (managed by uv)
├── uv.lock           # Dependency versions
├── .env              # secrets
└── .gitignore

## Trying it out:

1. Prerequisites:
* Python 3.11+
* uv installed
* A Google AI Studio API key (free or paid)

2. Clone and install:
git clone https://github.com/GRiosG/01_keyword_extractor.git
cd keyword-extractor
uv sync

3. Set your API Key (in .env)

4. Run the server:
uv run uvicorn main:app --reload

5. Doc & request:
Open http://localhost:8000/docs for the interactive Swagger UI.

curl:
curl -X POST http://localhost:8000/extract_keywords \
  -H "Content-Type: application/json" \
  -d '{"project_description": "A real-time chat app with end-to-end encryption, build on WebSockets and deployed on AWS Lambda."}'

Expected response:
{
  "keywords": [
    "real-time chat",
    "end-to-end encryption",
    "WebSockets",
    "AWS Lambda",
    "serverless deployment"
  ]
}

## License:
MIT
