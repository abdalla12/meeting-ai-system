

import re
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

ACTION_PATTERNS = [
    r"(?:we |i |you |they )?need(?:s)? to\s+(.+?)(?:\.|$)",
    r"(?:we |i |you |they )?should\s+(.+?)(?:\.|$)",
    r"(?:we |i |you |they )?must\s+(.+?)(?:\.|$)",
    r"(?:we |i |you |they )?have to\s+(.+?)(?:\.|$)",
    r"(?:please |let's |let us )\s*(.+?)(?:\.|$)",
    r"(?:will |going to )\s*(.+?)(?:\.|$)",
    r"action item[:\s]+(.+?)(?:\.|$)",
    r"todo[:\s]+(.+?)(?:\.|$)",
    r"task[:\s]+(.+?)(?:\.|$)",
    r"(?:by |before |until )(?:monday|tuesday|wednesday|thursday|friday|next week|end of (?:day|week|month))[\s,]*(.+?)(?:\.|$)",
    r"(?:finalize|complete|finish|submit|prepare|review|update|create|send|schedule|organize|arrange)\s+(.+?)(?:\.|$)",
]

HIGH_PRIORITY_KEYWORDS = [
    "urgent", "asap", "immediately", "critical", "must",
    "deadline", "today", "right away", "priority",
]

LOW_PRIORITY_KEYWORDS = [
    "eventually", "when possible", "sometime", "maybe",
    "consider", "nice to have", "optional",
]

def extract_action_items(transcript: str) -> List[Dict[str, Any]]:
    
    action_items = []
    seen = set()

    lines = transcript.split("\n")

    current_speaker = None
    for line in lines:
        line = line.strip()
        if not line:
            continue

        speaker_match = re.match(r"(Speaker \d+|SPEAKER_\d+)[:\s]*(.*)", line, re.IGNORECASE)
        if speaker_match:
            current_speaker = speaker_match.group(1)
            line = speaker_match.group(2)

        if not line:
            continue

        for pattern in ACTION_PATTERNS:
            matches = re.finditer(pattern, line, re.IGNORECASE)
            for match in matches:
                action_text = match.group(1).strip() if match.lastindex else match.group(0).strip()

                action_text = re.sub(r"^(that |the )", "", action_text)
                action_text = action_text.strip().rstrip(".,;:")

                if len(action_text) < 5 or action_text in seen:
                    continue

                seen.add(action_text)

                priority = _determine_priority(line)

                action_items.append({
                    "description": action_text.capitalize(),
                    "assignee": current_speaker,
                    "priority": priority,
                })

    if not action_items:
        action_items = _fallback_extraction(transcript)

    return action_items

def _determine_priority(text: str) -> str:
    
    text_lower = text.lower()
    if any(kw in text_lower for kw in HIGH_PRIORITY_KEYWORDS):
        return "high"
    if any(kw in text_lower for kw in LOW_PRIORITY_KEYWORDS):
        return "low"
    return "medium"

def _fallback_extraction(transcript: str) -> List[Dict[str, Any]]:
    
    sentences = re.split(r'[.!?]+', transcript)
    items = []

    action_verbs = [
        "finalize", "complete", "finish", "submit", "prepare",
        "review", "update", "create", "send", "schedule",
        "organize", "arrange", "launch", "start", "begin",
        "implement", "develop", "design", "test", "deploy",
    ]

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        words = sentence.lower().split()
        if any(verb in words for verb in action_verbs):
            items.append({
                "description": sentence.strip().capitalize(),
                "assignee": None,
                "priority": "medium",
            })

    return items[:10]
