# Avolve Backend - Resume Parser API

A high-performance FastAPI backend designed for modular PDF parsing and structured data extraction using AI.

## Features

- **Robust PDF Parsing**: Leveraging **Docling** for accurate conversion of complex PDF documents to clean Markdown.
- **AI-Powered Extraction**: Integrated with **Google Gemini 1.5 Flash** (via LangChain) to transform unstructured resume text into validated Pydantic objects.
- **Structured Logging**: Automatic **JSONL logging** for every processing step, tracking session history and performance.
- **Modular Architecture**: Clean separation between API endpoints, processing services, and configuration.

## Setup & Installation

### 1. Prerequisites

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) (Extremely fast Python package installer and resolver)

### 2. Dependency Installation

To install all required libraries and synchronize your environment, run:

```bash
uv sync
```

Or to add specific libraries manually:

```bash
uv add docling langchain-google-genai
```

### 3. Configuration

Initialize your secrets in `secrets/secrets.yml`:

```yaml
app:
  secret_key: "your_secret_key"
  algorithm: "HS256"
  access_token_expire_minutes: 30
  google_api_key: "your_gemini_api_key"  # Register at Google AI Studio
```

---

## API Usage

### Upload Resume

- **Endpoint**: `POST /api/v1/resume/upload`
- **Content-Type**: `multipart/form-data`
- **Body**: `file` (PDF document)

**Example Request**:

```bash
curl -X POST "http://localhost:8000/api/v1/resume/upload" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@/path/to/resume.pdf"
```

**Success Response (JSON)**:

```json
{
  "name": "Jane Doe",
  "email": "jane.doe@example.com",
  "skills": ["Python", "FastAPI", "React"],
  "experience": [
    {
      "company": "Tech Corp",
      "position": "Software Engineer",
      "duration": "2021 - Present",
      "responsibilities": ["Developing high-scale APIs"]
    }
  ],
  "education": [
    {
      "institution": "University of Science",
      "degree": "B.S. in Computer Science",
      "year": "2021"
    }
  ]
}
```

---

## Logging

Detailed step-by-step logs are stored in `logs/processing_logs.jsonl`. Each entry includes:
- `timestamp`: UTC isoformat.
- `step`: Service or function name (e.g., `ParserService.parse_pdf`).
- `status`: `START`, `SUCCESS`, `FAILED`, etc.
- `details`: Context-specific data (char count, file path, error messages).

*Note: The `logs/` directory is gitignored and will be created automatically on first run.*
