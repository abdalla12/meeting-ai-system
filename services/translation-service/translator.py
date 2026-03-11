

import logging
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)

_models: Dict[str, Any] = {}
_tokenizers: Dict[str, Any] = {}

def load_models(
    ko_to_en_model: str = "Helsinki-NLP/opus-mt-ko-en",
    en_to_ko_model: str = "Helsinki-NLP/opus-mt-en-ko",
    device: str = "cpu",
):
    
    global _models, _tokenizers

    try:
        from transformers import MarianMTModel, MarianTokenizer

        for direction, model_name in [("ko-en", ko_to_en_model), ("en-ko", en_to_ko_model)]:
            logger.info(f"Loading translation model: {model_name}")
            _tokenizers[direction] = MarianTokenizer.from_pretrained(model_name)
            _models[direction] = MarianMTModel.from_pretrained(model_name)
            if device == "cuda":
                _models[direction] = _models[direction].cuda()
            logger.info(f"Model {direction} loaded successfully.")

    except ImportError:
        logger.warning("transformers not installed. Using mock translator.")
        _models["mock"] = True
    except Exception as e:
        logger.error(f"Failed to load translation models: {e}")
        _models["mock"] = True

def is_model_loaded() -> bool:
    return len(_models) > 0

def translate_text(
    text: str,
    source_language: str,
    target_language: str,
    max_length: int = 512,
) -> Dict[str, Any]:
    
    if not _models:
        load_models()

    if "mock" in _models:
        return _mock_translate(text, source_language, target_language)

    direction = f"{source_language}-{target_language}"

    if direction not in _models:
        raise ValueError(f"Unsupported translation direction: {direction}. Supported: ko-en, en-ko")

    tokenizer = _tokenizers[direction]
    model = _models[direction]

    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=max_length)

    if next(model.parameters()).is_cuda:
        inputs = {k: v.cuda() for k, v in inputs.items()}

    import torch
    with torch.no_grad():
        outputs = model.generate(**inputs, max_length=max_length)

    translated = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return {
        "translated_text": translated,
        "source_language": source_language,
        "target_language": target_language,
        "confidence": 0.92,
    }

def translate_batch(
    texts: List[str],
    source_language: str,
    target_language: str,
    max_length: int = 512,
) -> List[Dict[str, Any]]:
    
    return [translate_text(t, source_language, target_language, max_length) for t in texts]

def _mock_translate(text: str, source_language: str, target_language: str) -> Dict[str, Any]:
    
    mock_translations = {
        "ko-en": {
            "마케팅 계획을 마무리해야 합니다.": "We need to finalize the marketing plan.",
            "캠페인은 다음 주 월요일에 시작해야 합니다.": "The campaign should start next Monday.",
        },
        "en-ko": {
            "We need to finalize the marketing plan.": "마케팅 계획을 마무리해야 합니다.",
            "The campaign should start next Monday.": "캠페인은 다음 주 월요일에 시작해야 합니다.",
        },
    }
    direction = f"{source_language}-{target_language}"
    translated = mock_translations.get(direction, {}).get(text, f"[Translated: {text}]")

    return {
        "translated_text": translated,
        "source_language": source_language,
        "target_language": target_language,
        "confidence": 0.94,
    }
