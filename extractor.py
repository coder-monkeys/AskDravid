import json

from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

from utils import extract_video_id, transform_transcript


def extract_transcript(url: str):
    """
    Fetch transcript from YouTube video.
    Saves as JSON file with {timestamp, text} entries.
    Returns list of dicts or None if unavailable.
    """
    try:
        video_id = extract_video_id(url)
        transcripts = YouTubeTranscriptApi().fetch(video_id=video_id)
        transformed_transcripts = transform_transcript(transcripts)

        with open("transcript.json", "w", encoding="utf-8") as f:
            json.dump(transformed_transcripts, f, ensure_ascii=False, indent=2)

        return transformed_transcripts

    except (TranscriptsDisabled, NoTranscriptFound) as e:
        raise ValueError(e)


extract_transcript("https://www.youtube.com/watch?v=Ihriju_4kYQ")
