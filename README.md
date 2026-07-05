# Enterprise Knowledge Assistant

Enterprise Knowledge Assistant is a Retrieval-Augmented Generation (RAG) application for uploading enterprise documents and asking natural-language questions over their contents. It combines a FastAPI backend, Azure OpenAI for embeddings and chat completion, ChromaDB for vector search, Azure Blob Storage for uploaded files, and a React/Vite frontend.

## Features

- Upload `.pdf`, `.docx`, and `.txt` documents.
- Validate file type and size before ingestion.
- Store original files in Azure Blob Storage.
- Parse documents into text and split them into searchable chunks.
- Generate Azure OpenAI embeddings for each chunk.
- Store document chunks and metadata in a persistent ChromaDB collection.
- Ask questions against the uploaded knowledge base.
- Return concise answers with confidence and source document metadata.
- View uploaded documents and chat with the assistant from the React frontend.

## Tech Stack

- Backend: Python, FastAPI, Uvicorn
- Frontend: React, Vite, Tailwind CSS, Axios
- AI: Azure OpenAI chat and embedding deployments
- Vector database: ChromaDB
- Storage: Azure Blob Storage
- Document parsing: PyPDF, python-docx, plain text parsing

## Project Structure

```text
.
+-- backend/
|   +-- requirements.txt
|   +-- src/
|       +-- api/
|       |   +-- health.py
|       |   +-- routers/
|       |       +-- chat_router.py
|       |       +-- document_router.py
|       +-- config/
|       |   +-- settings.py
|       +-- models/
|       +-- parsers/
|       +-- repositories/
|       |   +-- chroma_repository.py
|       +-- services/
|       +-- utils/
+-- data/
|   +-- chroma/
+-- frontend/
|   +-- package.json
|   +-- src/
+-- docker-compose.yml
+-- Dockerfile
+-- render.yaml
+-- README.md
```

## Prerequisites

- Python 3.12+
- Node.js 20+
- Azure OpenAI resource with:
  - a chat model deployment, for example `gpt-4o`
  - an embedding model deployment, for example `text-embedding-3-small`
- Azure Storage account and blob container

## Environment Variables

Create a `.env` file in the project root:

```env
APP_NAME=Enterprise Knowledge Assistant

AZURE_OPENAI_API_KEY=your_azure_openai_api_key
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-10-21
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o
AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME=text-embedding-3-small

AZURE_STORAGE_CONNECTION_STRING=your_azure_storage_connection_string
AZURE_STORAGE_CONTAINER=documents

DATABASE_URL=sqlite:///./data/app.db
CHROMA_DIRECTORY=./data/chroma
CHROMA_DB_PATH=./data/chroma
```

For the frontend, create `frontend/.env` if your backend is not running at the default URL:

```env
VITE_API_URL=http://127.0.0.1:8000
```

## Backend Setup

From the project root:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Run the API:

```powershell
uvicorn src.main:app --reload --host 127.0.0.1 --port 8000
```

The backend will be available at:

- API: `http://127.0.0.1:8000`
- Swagger docs: `http://127.0.0.1:8000/docs`
- Health check: `http://127.0.0.1:8000/health/`

## Frontend Setup

Open a second terminal from the project root:

```powershell
cd frontend
npm install
npm run dev
```

The frontend will usually be available at:

```text
http://localhost:5173
```

## API Endpoints

### Health Check

```http
GET /health/
```

Returns service status.

### Upload Document

```http
POST /api/documents/upload
```

Uploads and indexes a document. The request must use `multipart/form-data` with a `file` field.

Supported file types:

- `.pdf`
- `.docx`
- `.txt`

Maximum file size:

- 20 MB

### List Documents

```http
GET /api/documents
```

Returns unique documents currently indexed in ChromaDB.

### Ask a Question

```http
POST /api/chat/query
```

Example request:

```json
{
  "question": "What is the company's leave policy?",
  "top_k": 5
}
```

Example response:

```json
{
  "answer": "Employees are eligible for leave according to the policy described in the uploaded document.",
  "confidence": 0.86,
  "sources": [
    {
      "document_id": "document-id",
      "document_name": "policy.pdf",
      "chunk_index": 2
    }
  ]
}
```

## How It Works

1. A user uploads a supported document from the frontend.
2. The backend validates the file and checks whether the same file hash already exists.
3. The original document is uploaded to Azure Blob Storage.
4. The parser extracts text from the document.
5. The chunking service splits the text into smaller chunks.
6. Azure OpenAI generates embeddings for each chunk.
7. ChromaDB stores chunks, embeddings, and metadata.
8. When a user asks a question, the backend embeds the query and retrieves similar chunks.
9. The assistant builds context from retrieved chunks and asks Azure OpenAI to answer only from that context.

## Deployment Notes

The repository includes `Dockerfile`, `docker-compose.yml`, and `render.yaml` files for deployment work. Review these before deploying because the current Python dependency file is located at:

```text
backend/requirements.txt
```

If deploying from the repository root, make sure your build command points to the backend requirements file or move/copy the requirements file to the expected path.

## Troubleshooting

- If uploads fail, verify `AZURE_STORAGE_CONNECTION_STRING` and `AZURE_STORAGE_CONTAINER`.
- If chat answers fail, verify Azure OpenAI endpoint, API key, API version, and deployment names.
- If no documents appear, check that ChromaDB is writing to the expected `CHROMA_DB_PATH`.
- If the frontend cannot reach the backend, set `VITE_API_URL` in `frontend/.env`.
- If duplicate uploads return `Document already exists.`, the file hash is already indexed.

## License

No license file is currently included. Add one before distributing or publishing the project.
