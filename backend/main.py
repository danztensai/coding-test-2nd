from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from models.schemas import ChatRequest, ChatResponse, DocumentsResponse, UploadResponse, DocumentInfo, DocumentSource, ChunkInfo, ChunksResponse
from services.pdf_processor import PDFProcessor
from services.vector_store import VectorStoreService
from services.rag_pipeline import RAGPipeline
from services.get_embedding_function import get_embedding_function
from config import settings
import logging
import time
import os
from datetime import datetime

logging.basicConfig(level=settings.log_level)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="RAG-based Financial Statement Q&A System",
    description="AI-powered Q&A system for financial documents using RAG",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pdf_processor = PDFProcessor()
vector_store = VectorStoreService(
    persist_directory=settings.vector_db_path,
    embedding_function=get_embedding_function()
)
rag_pipeline = RAGPipeline()

UPLOAD_DIR = getattr(settings, "upload_dir", "./data")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.on_event("startup")
async def startup_event():
    logger.info("Starting RAG Q&A System...")

@app.get("/")
async def root():
    return {"message": "RAG-based Financial Statement Q&A System is running"}

@app.post("/api/upload", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    save_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(save_path, "wb") as f:
        content = await file.read()
        f.write(content)
    start_time = time.time()
    try:
        chunks = pdf_processor.process_pdf(save_path)
        vector_store.add_documents(chunks)
    except Exception as e:
        logger.error(f"PDF processing or vector store add failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to process PDF.")
    processing_time = round(time.time() - start_time, 2)
    return UploadResponse(
        message="File processed successfully",
        filename=file.filename,
        chunks_count=len(chunks),
        processing_time=processing_time
    )

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if not request.question or not request.question.strip():
        raise HTTPException(status_code=400, detail="Question is required.")
    start_time = time.time()
    try:
        result = rag_pipeline.generate_answer(request.question, chat_history=request.chat_history)
    except Exception as e:
        logger.error(f"RAG pipeline failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate answer.")
    processing_time = round(time.time() - start_time, 2)
    sources = [
        DocumentSource(
            content=src["content"],
            page=src.get("page", 0),
            score=src.get("score", 0.0),
            metadata=src.get("metadata", {})
        )
        for src in result["sources"]
    ]
    return ChatResponse(
        answer=result["answer"],
        sources=sources,
        processing_time=processing_time
    )

@app.get("/api/documents", response_model=DocumentsResponse)
async def get_documents():
    docs = []
    for fname in os.listdir(UPLOAD_DIR):
        if fname.lower().endswith(".pdf"):
            items = vector_store.db.get(include=[])
            chunk_count = sum(1 for id in items["ids"] if fname in id)
            docs.append(DocumentInfo(
                filename=fname,
                upload_date=datetime.utcfromtimestamp(os.path.getmtime(os.path.join(UPLOAD_DIR, fname))),
                chunks_count=chunk_count,
                status="processed"
            ))
    return DocumentsResponse(documents=docs)

@app.get("/api/chunks", response_model=ChunksResponse)
async def get_chunks():
    items = vector_store.db.get(include=["metadatas", "documents"])
    chunks = []
    for doc, meta in zip(items["documents"], items["metadatas"]):
        chunks.append(ChunkInfo(
            id=meta.get("id", ""),
            content=doc,
            page=meta.get("page", 0),
            metadata=meta
        ))
    return ChunksResponse(chunks=chunks, total_count=len(chunks))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.host, port=settings.port, reload=settings.debug)
