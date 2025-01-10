"""
This file is a client for the OpenAI API.
"""

from dataclasses import dataclass
from typing import Union, List, Iterable

import yaml

from openai import OpenAI
from PyPDF2 import PdfReader

from settings import secret_path

EMBED_MODEL = "text-embedding-3-small"


@dataclass
class Embedding:
    """
    This class is a data class for storing embeddings.
    """

    id: str
    vector: List[float]
    text: str

    def to_dict(self):
        """
        This method is used to convert the embedding to a dictionary.

        Args:
            None
        Returns:
            dict: The embedding as a dictionary.
        """
        return {"id": self.id, "vector": self.vector, "text": self.text}


class OpenAIClient:
    """
    This class is a client for the OpenAI API.
    """

    def __init__(self):
        with open(secret_path, "r", encoding="utf-8") as f:
            __secret = yaml.safe_load(f)
        __api_key = __secret["openai"]["api_key"]

        if not hasattr(self, "client") or self.client is None:
            self.client = OpenAI(api_key=__api_key)

        self.model = "gpt-4o-mini"

    def __del__(self):
        if hasattr(self, "client") and self.client is not None:
            self.client.close()
            self.client = None

    def chat(self, messages: List[dict]) -> str:
        """
        This method is used to send a message to the OpenAI API and return the response.

        Args:
            messages: list[dict]: The messages to send to the OpenAI API.
        Returns:
            str: The response message from the OpenAI API.
        """
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )
        return completion.choices[0].message.content

    def embeddings(
        self, text_input: Union[str, List[str], Iterable[int], Iterable[Iterable[int]]], model: str = EMBED_MODEL
    ) -> List[Embedding]:
        """
        This method is used to generate embeddings for the input.

        Args:
            text_input: Union[
                str,
                List[str],
                Iterable[int],
                Iterable[Iterable[int]],
            ]: The input to generate embeddings for.
            model: str: The model to use for generating embeddings(default: EMBED_MODEL).
        Returns:
            list[Embedding]: The embeddings for the input.
        """
        return self.client.embeddings.create(
            model=model,
            input=text_input,
        )

    def pdf_to_embeddings(
        self,
        pdf_path: str,
        chunk_size: int = 1000,
    ) -> List[Embedding]:
        """
        This method is used to generate embeddings for the input.

        Args:
            pdf_path: str: The path to the PDF file.
            chunk_size: int: The size of the chunks to split the PDF into(default: 1000).
        Returns:
            List[Embedding]: The embeddings for the input.
        """
        pdf_reader = PdfReader(pdf_path)
        chunks = []
        for page in pdf_reader.pages:
            text = page.extract_text()
            chunks.extend([text[i : i + chunk_size] for i in range(0, len(text), chunk_size)])

        response = self.embeddings(chunks)
        return [Embedding(id=value.index, vector=value.embedding, text=chunks[value.index]) for value in response.data]
