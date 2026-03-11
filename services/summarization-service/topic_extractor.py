

import re
import logging
from collections import Counter
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

_topic_model = None

def load_model():
    
    global _topic_model
    try:
        from bertopic import BERTopic

        logger.info("Loading BERTopic model...")
        _topic_model = BERTopic(language="multilingual", verbose=False)
        logger.info("BERTopic loaded.")
    except ImportError:
        logger.warning("BERTopic not installed. Using fallback TF-IDF topic extraction.")
        _topic_model = "fallback"
    except Exception as e:
        logger.error(f"Failed to load BERTopic: {e}")
        _topic_model = "fallback"

def extract_topics(
    transcript: str,
    num_topics: int = 5,
) -> List[Dict[str, Any]]:
    
    global _topic_model

    if _topic_model is None:
        load_model()

    if _topic_model == "fallback" or _topic_model is None:
        return _tfidf_topics(transcript, num_topics)

    try:

        sentences = re.split(r'[.!?\n]+', transcript)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 10]

        if len(sentences) < 5:
            return _tfidf_topics(transcript, num_topics)

        topics, probs = _topic_model.fit_transform(sentences)

        topic_info = _topic_model.get_topic_info()
        results = []

        for _, row in topic_info.iterrows():
            if row["Topic"] == -1:
                continue
            topic_words = _topic_model.get_topic(row["Topic"])
            keywords = [word for word, _ in topic_words[:5]]
            results.append({
                "name": " ".join(keywords[:3]).title(),
                "keywords": keywords,
                "relevance": round(row.get("Count", 1) / len(sentences), 2),
            })

            if len(results) >= num_topics:
                break

        return results if results else _tfidf_topics(transcript, num_topics)

    except Exception as e:
        logger.error(f"BERTopic extraction failed: {e}. Using fallback.")
        return _tfidf_topics(transcript, num_topics)

def _tfidf_topics(text: str, num_topics: int = 5) -> List[Dict[str, Any]]:
    

    stopwords = {
        "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
        "have", "has", "had", "do", "does", "did", "will", "would", "could",
        "should", "may", "might", "can", "to", "of", "in", "for", "on", "with",
        "at", "by", "from", "as", "into", "through", "and", "but", "if", "or",
        "it", "we", "i", "you", "he", "she", "they", "that", "this", "what",
        "which", "who", "how", "when", "where", "why", "not", "no", "so",
        "very", "just", "about", "also", "then", "than", "more", "said",
        "speaker", "think", "know", "going", "want", "get", "make", "like",
    }

    words = re.findall(r'\b[a-zA-Z가-힣]{3,}\b', text.lower())
    filtered = [w for w in words if w not in stopwords]
    counter = Counter(filtered)

    common = counter.most_common(num_topics * 3)
    topics = []

    used_words = set()
    for i in range(min(num_topics, len(common))):
        keyword = common[i][0]
        if keyword in used_words:
            continue

        related = [w for w, _ in common if w != keyword and w not in used_words][:4]
        used_words.add(keyword)
        used_words.update(related[:2])

        topic_keywords = [keyword] + related[:4]
        relevance = round(counter[keyword] / len(filtered), 2) if filtered else 0

        topics.append({
            "name": keyword.title(),
            "keywords": topic_keywords,
            "relevance": max(relevance, 0.1),
        })

    return topics
