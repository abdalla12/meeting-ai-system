from pydantic import BaseModel, Field
from typing import List, Optional

class SummarizationRequest(BaseModel):
    transcript: str = Field(..., description="Full meeting transcript")
    max_length: int = Field(200, description="Maximum summary length")
    min_length: int = Field(50, description="Minimum summary length")

class SummarizationResponse(BaseModel):
    summary: str = Field(..., description="Generated meeting summary")
    topic: str = Field("", description="Detected main topic")

class ActionItem(BaseModel):
    description: str = Field(..., description="Action item description")
    assignee: Optional[str] = Field(None, description="Assigned speaker")
    priority: str = Field("medium", description="Priority: high, medium, low")

class ActionExtractionRequest(BaseModel):
    transcript: str = Field(..., description="Meeting transcript")

class ActionExtractionResponse(BaseModel):
    action_items: List[ActionItem] = Field(..., description="Extracted action items")

class TopicKeyword(BaseModel):
    name: str
    keywords: List[str]
    relevance: float

class TopicExtractionRequest(BaseModel):
    transcript: str = Field(..., description="Meeting transcript")
    num_topics: int = Field(5, description="Number of topics to extract")

class TopicExtractionResponse(BaseModel):
    topics: List[TopicKeyword] = Field(..., description="Extracted topics")

class HealthResponse(BaseModel):
    status: str = "healthy"
    model_loaded: bool = False
    version: str = "1.0.0"
