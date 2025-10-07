"""Digital journal entry processor.

This module provides a small command line interface that accepts a freeform
journal entry and automatically separates it into themed sections.  The goal is
to let someone write about their day once and have the script extract useful
structured information that can be reviewed later.

The script keeps a persistent JSON file (``data/journal_entries.json``) where
each entry stores the original text alongside the detected people, events,
feelings, situations, and health updates.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Set


DATA_PATH = Path("data")
JOURNAL_FILE = DATA_PATH / "journal_entries.json"


FEELING_KEYWORDS = {
    "happy",
    "joy",
    "joyful",
    "glad",
    "excited",
    "content",
    "peaceful",
    "sad",
    "upset",
    "angry",
    "frustrated",
    "anxious",
    "nervous",
    "worried",
    "calm",
    "relaxed",
    "tired",
    "exhausted",
    "stressed",
    "grateful",
    "thankful",
    "lonely",
    "confident",
    "proud",
    "hopeful",
}


EVENT_KEYWORDS = {
    "meeting",
    "birthday",
    "anniversary",
    "party",
    "presentation",
    "conference",
    "interview",
    "deadline",
    "vacation",
    "trip",
    "wedding",
    "graduation",
    "celebration",
    "appointment",
    "game",
    "practice",
    "ceremony",
}


HEALTH_KEYWORDS = {
    "exercise",
    "workout",
    "gym",
    "run",
    "running",
    "walk",
    "walking",
    "yoga",
    "meditation",
    "doctor",
    "dentist",
    "medicine",
    "medication",
    "pill",
    "headache",
    "stomach",
    "flu",
    "cold",
    "fever",
    "pain",
    "ache",
    "injury",
    "therapy",
    "sleep",
    "rest",
    "hydrate",
    "hydrated",
    "nutrition",
    "diet",
}


SITUATION_KEYWORDS = {
    "work",
    "office",
    "project",
    "school",
    "class",
    "lesson",
    "family",
    "friends",
    "home",
    "travel",
    "commute",
    "study",
    "exam",
    "shopping",
    "errand",
    "cooking",
    "cleaning",
    "house",
    "weather",
    "rain",
    "sunny",
    "storm",
}


STOP_WORDS = {
    "I",
    "We",
    "My",
    "The",
    "A",
    "An",
    "It",
    "He",
    "She",
    "They",
    "Today",
    "Tonight",
    "Morning",
    "Evening",
    "Afternoon",
    "Later",
    "Yesterday",
    "Tomorrow",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
}


NAME_PATTERN = re.compile(r"\b([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)\b")


def sentence_split(text: str) -> List[str]:
    """Split freeform text into a list of sentences."""

    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    return [sentence.strip() for sentence in sentences if sentence.strip()]


def detect_keywords(sentence: str, keywords: Iterable[str]) -> bool:
    """Return True if any keyword appears as a whole word in ``sentence``."""

    normalized = sentence.lower()
    return any(re.search(rf"\b{re.escape(word)}\b", normalized) for word in keywords)


def extract_people(text: str) -> List[str]:
    """Extract capitalized names from the text using a light-weight heuristic."""

    candidates = {
        match.group(1)
        for match in NAME_PATTERN.finditer(text)
        if match.group(1) not in STOP_WORDS
    }
    # Sort to keep ordering predictable for tests and ease of reading.
    return sorted(candidates)


@dataclass
class JournalEntry:
    raw_entry: str
    timestamp: str
    feelings: List[str] = field(default_factory=list)
    events: List[str] = field(default_factory=list)
    health: List[str] = field(default_factory=list)
    situations: List[str] = field(default_factory=list)
    people: List[str] = field(default_factory=list)

    @classmethod
    def from_text(cls, entry_text: str, timestamp: datetime | None = None) -> "JournalEntry":
        timestamp = timestamp or datetime.now()
        sentences = sentence_split(entry_text)

        feelings = [s for s in sentences if detect_keywords(s, FEELING_KEYWORDS)]
        events = [s for s in sentences if detect_keywords(s, EVENT_KEYWORDS)]
        health = [s for s in sentences if detect_keywords(s, HEALTH_KEYWORDS)]

        # A situation is a sentence with general context keywords that is not
        # already stored as a feeling, event, or health update.
        categorized_sentences: Set[str] = set(feelings + events + health)
        situations = [
            s
            for s in sentences
            if s not in categorized_sentences and detect_keywords(s, SITUATION_KEYWORDS)
        ]

        people = extract_people(entry_text)

        return cls(
            raw_entry=entry_text.strip(),
            timestamp=timestamp.isoformat(timespec="seconds"),
            feelings=feelings,
            events=events,
            health=health,
            situations=situations,
            people=people,
        )

    def to_dict(self) -> Dict[str, Sequence[str] | str]:
        return {
            "timestamp": self.timestamp,
            "raw_entry": self.raw_entry,
            "feelings": self.feelings,
            "events": self.events,
            "health": self.health,
            "situations": self.situations,
            "people": self.people,
        }


def load_journal() -> Dict[str, List[Dict[str, Sequence[str] | str]]]:
    if not JOURNAL_FILE.exists():
        return {"entries": []}
    with JOURNAL_FILE.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def save_journal(data: Dict[str, List[Dict[str, Sequence[str] | str]]]) -> None:
    DATA_PATH.mkdir(parents=True, exist_ok=True)
    with JOURNAL_FILE.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)


def add_entry(entry_text: str, timestamp: datetime | None = None) -> JournalEntry:
    journal = load_journal()
    entry = JournalEntry.from_text(entry_text, timestamp=timestamp)
    journal.setdefault("entries", []).append(entry.to_dict())
    save_journal(journal)
    return entry


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Log a structured journal entry")
    parser.add_argument(
        "--entry",
        help="The journal entry text. If omitted, the script will read from standard input.",
    )
    parser.add_argument(
        "--timestamp",
        help="Optional ISO timestamp for the entry (defaults to the current time).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_arguments()

    if args.entry:
        entry_text = args.entry
    else:
        print("Enter your journal entry. Finish with Ctrl-D (or Ctrl-Z on Windows) and press Enter:")
        try:
            entry_text = sys.stdin.read()
        except KeyboardInterrupt:
            raise SystemExit("Journal entry cancelled.")

    entry_text = entry_text.strip()
    if not entry_text:
        raise SystemExit("No journal entry provided.")

    timestamp: datetime | None = None
    if args.timestamp:
        try:
            timestamp = datetime.fromisoformat(args.timestamp)
        except ValueError as exc:
            raise SystemExit(f"Invalid timestamp: {args.timestamp}") from exc

    entry = add_entry(entry_text, timestamp=timestamp)

    print("Journal entry saved! Here's the structured summary:\n")
    print(json.dumps(entry.to_dict(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

