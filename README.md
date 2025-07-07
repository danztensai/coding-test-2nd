# Handoko
#Ini Surya yang mengubah readme di branch sendiri
# This is my first commit in this repository - Tuntun
# Anas
## Overview

This project is a full-stack application using **RAG (Retrieval Augmented Generation)** technology:
- **Next.js** frontend for chat-based Q&A
- **FastAPI** backend for PDF processing, vector search, and LLM integration
- **ChromaDB** for vector storage
- **Google Gemini, HuggingFace, Ollama, or Bedrock** for embeddings and LLMs

## Check Video for Demo

Users can upload financial statement PDFs, ask questions, and receive AI-generated answers with cited document sources.

---

## Features

- Multi-PDF file upload and processing
- Real-time chat Q&A interface
- Conversation history and context continuity
- Answer source display with file, page, and relevance
- Visual highlighting of document chunks
- Upload progress and status display
- Error handling and loading indicators

---

## Project Structure

```
coding-test-2nd/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration
│   ├── models/              # Data models
│   ├── services/            # RAG service logic
|   |── utils/               # Common Utility
│   ├── requirements.txt     # Python dependencies
├── frontend/
│   ├── pages/               # Next.js pages
│   ├── components/          # React components
│   ├── styles/              # CSS files
│   ├── package.json         # Node.js dependencies
│   ├── tsconfig.json        # TypeScript config
│   ├── .env.local           # Frontend environment variables
├── data/
│   └── sample.pdf           # Example PDF
├── .env                     # Backend environment variables
├── .env.example             # Example env file
└── README.md
```

---

## Getting Started

### 1. Environment Setup

```bash
git clone <your-repository-url>
cd coding-test-2nd
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. Backend Setup

```bash
cd backend
pip install -r requirements.txt
# Set up .env file (see .env.example)
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Frontend Setup

```bash
cd frontend
npm install
# Set up .env.local (see .env.example)
npm run dev
```

### 4. Initial Data Processing

Upload a PDF via the UI or:
```bash
curl -X POST "http://localhost:8000/api/upload" -F "file=@../data/sample.pdf"
```

---

## API Endpoints

### **POST /api/upload**
Upload PDF file and store in vector database

### **POST /api/chat**
Generate RAG-based answer to question

### **GET /api/documents**
Retrieve processed document information

---

## Performance Analysis or Optimization Notes

- **Vector Search Speed:** ChromaDB is fast for small/medium datasets; use Pinecone/FAISS for scale.
- **Chunking & Embedding:** Can be parallelized or offloaded to background workers for large files.
- **API Response Time:** Typically <2s; LLM inference is the main bottleneck.
- **Frontend Optimization:** React rendering is efficient; consider caching and optimistic UI.
- **Resource Usage:** Monitor memory/CPU for embedding and LLM inference.

---

## Future Improvement Suggestions

- **Scalability:** Use managed vector DBs for large-scale deployments.
- **Background Processing:** Offload heavy tasks to background jobs.
- **User Authentication:** Add user accounts for personalized experience.
- **Advanced Analytics:** Integrate dashboards for usage and feedback.
- **Enhanced PDF Viewer:** Directly highlight referenced chunks in the PDF.
- **Multi-language Support:** Add multilingual embeddings and LLMs.
- **Streaming Responses:** Implement real-time answer streaming.
- **Accessibility:** Improve a11y for all users.

---

## Troubleshooting

**Frontend TypeScript Errors**:
- Ensure `npm install` was completed successfully
- Check that `node_modules` directory exists and is populated
- Verify all configuration files are present

**Backend Import Errors**:
- Activate Python virtual environment
- Install all requirements: `pip install -r requirements.txt`
- Check Python path and module imports

**CORS Issues**:
- Ensure backend CORS settings allow frontend origin
- Check that API endpoints are accessible from frontend

---

# Local LLM Instance using llama
# Ollama LLaMA 3 Deployment with Docker Compose

```
docker compose up -d --build
```

After the server is running, connect into the running container:
you can change `llama3` based on your model that you want to use

```
docker exec -it ollama ollama pull llama3

```
If you gonna use llama on local as your llm processing dont forget to change your .env


**Build a smarter document Q&A system with RAG technology!**
