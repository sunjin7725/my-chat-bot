"""
This file is used to ask a question to a youtube video.
"""

from typing import Iterable, List
from urllib.parse import urlparse, parse_qs

from youtube_transcript_api import YouTubeTranscriptApi

from utils.client import OpenAIClient


def get_youtube_video_id_from_url(url: str) -> str:
    """
    Example url: https://youtu.be/UeCpRaP9nKw?t=159
    https://youtu.be/UeCpRaP9nKw
    """
    url = urlparse(url)
    path = url.path
    query = parse_qs(url.query)

    if path == "/watch":
        video_id = query.get("v")[0] if query.get("v") else None
    else:
        video_id = path[1:]

    return video_id


def get_youtube_transcript(video_id: str, languages: Iterable[str] = ("ko",)) -> List[dict]:
    """
    This function is used to get the transcript of a youtube video.

    Args:
        video_id: str: The id of the youtube video.
        languages: Iterable[str]: The languages to get the transcript in.
    Returns:
        List[dict]: The transcript of the youtube video.
    """
    return YouTubeTranscriptApi.get_transcript(video_id, languages=languages)


def get_answer_in_youtube(video_id: str, question: str) -> str:
    """
    This function is used to get the summary of a youtube video.

    Args:
        video_id: str: The id of the youtube video.
        question: str: The question to ask the youtube video.
    Returns:
        str: The summary of the youtube video.
    """
    transcript = get_youtube_transcript(video_id)
    text_list = [f"{t.get('start')}s: {t.get('text')}" for t in transcript]
    text = " ".join(text_list)

    client = OpenAIClient()

    prompt_role = """
        You are a helpful assistant.
        You are given a TRANSCRIPT of a youtube video.
        You should answer USER`s question.
        The answer is not politcal. You have to answer friendly.
    """

    prompt = f"""
        {prompt_role}
        TRANSCRIPT: {text}
        USER: {question}
    """
    return client.chat([{"role": "user", "content": prompt}])
