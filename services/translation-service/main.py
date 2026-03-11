

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import config
from schemas import (
    TranslationRequest, TranslationResponse,
    BatchTranslationRequest, BatchTranslationResponse,
    HealthResponse,
)
from translator import load_models, is_model_loaded, translate_text, translate_batch

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    load_models(
        ko_to_en_model=config.MODEL_KO_TO_EN,
        en_to_ko_model=config.MODEL_EN_TO_KO,
        device=config.DEVICE,
    )
    yield

app = FastAPI(
    title="Meeting AI — Translation Service",
    description="Bidirectional Korean ↔ English translation with MarianMT",
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

@app.post("/translate", response_model=TranslationResponse)
async def translate(request: TranslationRequest):
    
    logger.info(f"Translate: {request.source_language} → {request.target_language}, len={len(request.text)}")

    result = translate_text(
        text=request.text,
        source_language=request.source_language,
        target_language=request.target_language,
    )

    return TranslationResponse(**result)

@app.post("/translate/batch", response_model=BatchTranslationResponse)
async def translate_batch_endpoint(request: BatchTranslationRequest):
    
    results = translate_batch(
        texts=request.texts,
        source_language=request.source_language,
        target_language=request.target_language,
    )
    return BatchTranslationResponse(
        translations=[TranslationResponse(**r) for r in results]
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8003, reload=True)
