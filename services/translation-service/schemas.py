from pydantic import BaseModel, Field
from typing import Optional

class TranslationRequest(BaseModel):
    text: str = Field(..., description="Text to translate")
    source_language: str = Field(..., description="Source language code (ko or en)")
    target_language: str = Field(..., description="Target language code (ko or en)")

class TranslationResponse(BaseModel):
    translated_text: str = Field(..., description="Translated text")
    source_language: str = Field(..., description="Source language")
    target_language: str = Field(..., description="Target language")
    confidence: float = Field(0.0, description="Translation confidence score")

class BatchTranslationRequest(BaseModel):
    texts: list[str] = Field(..., description="List of texts to translate")
    source_language: str = Field(..., description="Source language code")
    target_language: str = Field(..., description="Target language code")

class BatchTranslationResponse(BaseModel):
    translations: list[TranslationResponse] = Field(..., description="List of translations")

class HealthResponse(BaseModel):
    status: str = "healthy"
    model_loaded: bool = False
    version: str = "1.0.0"
