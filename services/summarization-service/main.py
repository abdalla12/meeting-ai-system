

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import config
from schemas import (
    SummarizationRequest, SummarizationResponse,
    ActionExtractionRequest, ActionExtractionResponse, ActionItem,
    TopicExtractionRequest, TopicExtractionResponse, TopicKeyword,
    HealthResponse,
)
from summarizer import load_model as load_summarizer, is_model_loaded, summarize_transcript
from action_extractor import extract_action_items
from topic_extractor import extract_topics, load_model as load_topic_model

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    load_summarizer(model_name=config.SUMMARIZATION_MODEL, device=config.DEVICE)
    load_topic_model()
    yield

app = FastAPI(
    title="Meeting AI — Summarization Service",
    description="Meeting summarization, action items, and topic extraction",
    version=config.SERVICE_VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="healthy",
        model_loaded=is_model_loaded(),
        version=config.SERVICE_VERSION,
    )

@app.post("/summarize", response_model=SummarizationResponse)
async def summarize(request: SummarizationRequest):
    
    logger.info(f"Summarize request: transcript length={len(request.transcript)}")

    result = summarize_transcript(
        transcript=request.transcript,
        max_length=request.max_length,
        min_length=request.min_length,
    )

    return SummarizationResponse(
        summary=result["summary"],
        topic=result["topic"],
    )

@app.post("/extract-actions", response_model=ActionExtractionResponse)
async def extract_actions(request: ActionExtractionRequest):
    
    logger.info(f"Action extraction request: transcript length={len(request.transcript)}")

    items = extract_action_items(request.transcript)

    return ActionExtractionResponse(
        action_items=[ActionItem(**item) for item in items]
    )

@app.post("/extract-topics", response_model=TopicExtractionResponse)
async def extract_topics_endpoint(request: TopicExtractionRequest):
    
    logger.info(f"Topic extraction request: transcript length={len(request.transcript)}")

    topics = extract_topics(
        transcript=request.transcript,
        num_topics=request.num_topics,
    )

    return TopicExtractionResponse(
        topics=[TopicKeyword(**t) for t in topics]
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8004, reload=True)
