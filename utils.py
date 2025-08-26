import re

from youtube_transcript_api import FetchedTranscriptSnippet


def extract_video_id(url: str) -> str:
    """
    Extracts video ID from YouTube URL.
    """
    match = re.search(r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})", url)
    if not match:
        raise ValueError("Invalid YouTube URL")
    return match.group(1)


def transform_transcript(transcript):
    """
    Transform transcript entries into {id, text, start, end} format.
    """
    transformed = []
    for i, entry in enumerate(transcript, start=1):
        transformed.append({
            "id": f"c{i}",
            "text": entry.text,
            "start": entry.start,
            "end": entry.start + entry.duration
        })
    return transformed
