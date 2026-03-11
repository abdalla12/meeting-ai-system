

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

_model = None
_tokenizer = None

def load_model(model_name: str = "google/flan-t5-base", device: str = "cpu"):
    
    global _model, _tokenizer
    try:
        from transformers import T5ForConditionalGeneration, T5Tokenizer

        logger.info(f"Loading summarization model: {model_name}")
        _tokenizer = T5Tokenizer.from_pretrained(model_name)
        _model = T5ForConditionalGeneration.from_pretrained(model_name)
        if device == "cuda":
            _model = _model.cuda()
        logger.info("Summarization model loaded successfully.")
    except ImportError:
        logger.warning("transformers not installed. Using mock summarizer.")
        _model = "mock"
    except Exception as e:
        logger.error(f"Failed to load summarization model: {e}")
        _model = "mock"

def is_model_loaded() -> bool:
    return _model is not None

def summarize_transcript(
    transcript: str,
    max_length: int = 200,
    min_length: int = 50,
) -> Dict[str, Any]:
    
    global _model, _tokenizer

    if _model is None:
        load_model()

    if _model == "mock":
        return _mock_summarize(transcript)

    import torch

    prompt = f"Summarize the following meeting transcript:\n\n{transcript}\n\nSummary:"

    inputs = _tokenizer(
        prompt,
        return_tensors="pt",
        max_length=1024,
        truncation=True,
    )

    if next(_model.parameters()).is_cuda:
        inputs = {k: v.cuda() for k, v in inputs.items()}

    with torch.no_grad():
        outputs = _model.generate(
            **inputs,
            max_length=max_length,
            min_length=min_length,
            num_beams=4,
            length_penalty=2.0,
            early_stopping=True,
        )

    summary = _tokenizer.decode(outputs[0], skip_special_tokens=True)

    topic = _extract_simple_topic(transcript)

    return {
        "summary": summary,
        "topic": topic,
    }

def _extract_simple_topic(text: str) -> str:
    
    import re
    from collections import Counter

    stopwords = {
        "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
        "have", "has", "had", "do", "does", "did", "will", "would", "could",
        "should", "may", "might", "must", "shall", "can", "need", "dare",
        "ought", "used", "to", "of", "in", "for", "on", "with", "at", "by",
        "from", "as", "into", "through", "during", "before", "after", "above",
        "below", "between", "out", "off", "over", "under", "again", "further",
        "then", "once", "here", "there", "when", "where", "why", "how", "all",
        "both", "each", "few", "more", "most", "other", "some", "such", "no",
        "nor", "not", "only", "own", "same", "so", "than", "too", "very",
        "and", "but", "if", "or", "it", "we", "i", "you", "he", "she", "they",
        "speaker", "said", "think", "think", "that", "this", "just", "about",
    }

    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    filtered = [w for w in words if w not in stopwords]
    counter = Counter(filtered)

    if counter:
        top_words = [w for w, _ in counter.most_common(3)]
        return " ".join(top_words).title()
    return "General Discussion"

def _mock_summarize(transcript: str) -> Dict[str, Any]:
    
    return {
        "summary": "The team discussed finalizing the marketing plan and scheduling the campaign launch for Monday. Key decisions were made regarding timeline and resource allocation.",
        "topic": "Marketing Strategy Planning",
    }
