"""
This file is a client for the OpenAI API.
"""

import json
from dataclasses import dataclass
from typing import Union, List, Iterable

import yaml
import requests

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


class NaverAPIClient:
    """
    This class is a client for interacting with the Naver API.
    It provides methods to search for content based on user queries
    and to determine the appropriate search service type.
    """

    def __init__(self):
        with open(secret_path, "r", encoding="utf-8") as f:
            __secret = yaml.safe_load(f)
        __client_id = __secret["naver"]["client_id"]
        __client_secret = __secret["naver"]["client_secret"]

        self.base_url = "https://openapi.naver.com/v1/search"
        self.headers = {"X-Naver-Client-Id": __client_id, "X-Naver-Client-Secret": __client_secret}

    def search(self, query, display=10, start=1, sort="sim"):
        """
        This method performs a search using the Naver API based on the provided query.

        Args:
            query (str): The search query.
            display (int): The number of results to display (default: 10).
            start (int): The starting point for the results (default: 1).
            sort (str): The sorting method for the results (default: 'sim').

        Returns:
            dict: The search results from the Naver API.
        """
        __service_type = get_search_service_type(query)
        __search_query = make_search_query(query, __service_type)
        url = f"{self.base_url}/{__service_type.lower()}"

        params = {
            "query": __search_query,
            "start": start,
            "display": display,
            "sort": sort,
        }
        response = requests.get(url, params=params, headers=self.headers, timeout=10)
        return json.loads(response.text.replace("<b>", "").replace("</b>", ""))


class KakaoAPIClient:
    """
    This class is a client for interacting with the Kakao API.
    It provides methods to search for content based on user queries
    and to retrieve video search results.
    """

    def __init__(self):
        with open(secret_path, "r", encoding="utf-8") as f:
            __secret = yaml.safe_load(f)
        __api_key = __secret["kakao"]["api_key"]

        self.base_url = "https://dapi.kakao.com/v2/search"
        self.headers = {"Authorization": f"KakaoAK {__api_key}"}

    def search(self, query, size=10, page=1, sort="accuracy"):
        """
        This method performs a search using the Kakao API based on the provided query.

        Args:
            query (str): The search query.
            size (int): The number of results to display (default: 10).
            page (int): The page number for pagination (default: 1).
            sort (str): The sorting method for the results (default: 'accuracy').

        Returns:
            dict: The search results from the Kakao API.
        """
        __service_type = get_search_service_type(query)
        __search_query = make_search_query(query, __service_type)
        if __service_type == "BOOK":
            __service_type = "BOOK"
        elif __service_type == "BLOG":
            __service_type = "BLOG"
        elif __service_type == "CAFEARTICLE":
            __service_type = "CAFE"
        elif __service_type in ("NEWS", "SHOP", "DOC", "ENCYC", "WEBKR"):
            __service_type = "WEB"

        if __service_type == "BOOK":
            url = f"https://dapi.kakao.com/v3/search/{__service_type.lower()}"
        else:
            url = f"{self.base_url}/{__service_type.lower()}"

        params = {
            "query": __search_query,
            "page": page,
            "size": size,
            "sort": sort,
        }
        response = requests.get(url, params=params, headers=self.headers, timeout=10)
        return json.loads(response.text.replace("<b>", "").replace("</b>", ""))

    def video_search(self, query, size=10, page=1, sort="accuracy"):
        """

        This method performs a video search using the Kakao API based on the provided query.

        Args:
            query (str): The search query for videos.
            size (int): The number of results to display (default: 10).
            page (int): The page number for pagination (default: 1).
            sort (str): The sorting method for the results (default: 'accuracy').

        Returns:
            dict: The video search results from the Kakao API.
        """
        url = f"{self.base_url}/vclip"
        params = {
            "query": query,
            "page": page,
            "size": size,
            "sort": sort,
        }
        response = requests.get(url, params=params, headers=self.headers, timeout=10)
        return json.loads(response.text.replace("<b>", "").replace("</b>", ""))


def get_search_service_type(query):
    """
    This method extracts the type of search service based on the provided query.

    Args:
        query: str: The search query to analyze.

    Returns:
        str: The type of search service (e.g., 'BLOG', 'NEWS', etc.).
    """
    open_ai_client = OpenAIClient()

    prompt = """
        Please extract the type of search service based on the following QUERY. The available options are: 
        - 'BLOG': Blog posts
        - 'NEWS': News articles
        - 'BOOK': Books
        - 'ENCYC': Encyclopedia entries
        - 'CAFEARTICLE': Cafe posts
        - 'WEBKR': Web documents
        - 'SHOP': Shopping items
        - 'DOC': Professional documents
        Make sure to choose the most relevant type that best fits the content of the QUERY provided.
        **Output Format:** Please respond with only the type (e.g., BOOK) without any additional text or formatting.
    """
    response = open_ai_client.chat(
        [
            {
                "role": "user",
                "content": f"""
            {prompt}
            QUERY: {query}
            """,
            }
        ]
    )
    return response


def make_search_query(query, service_type=None):
    """
    This method creates a search query for a search engine based on the provided query and service type.

    Args:
        query: str: The search query.
        service_type: str: The type of service to use for the search.

    Returns:
        str: The formatted search query for the search engine.
    """
    open_ai_client = OpenAIClient()

    service_types = {
        "BLOG": "Blog posts",
        "NEWS": "News articles",
        "BOOK": "Books",
        "ENCYC": "Encyclopedia entries",
        "CAFEARTICLE": "Cafe posts",
        "WEBKR": "Web documents",
        "SHOP": "Shopping items",
        "DOC": "Professional documents",
    }

    prompt = """
    Please create a search query for a search engine (e.g., Google, Naver) based on the following QUERY and SERVICE_TYPE. 

    Make sure to:
    1. Use clear and concise language.
    2. Include relevant keywords that capture the essence of the QUERY.
    3. Format the query in a way that is likely to yield useful search results.
    Please don't return special characters like double quotes, and avoid including today's year, month, etc.
    **Output Format:** Provide the search query as a single string without any additional text or explanation. 
    """
    response = open_ai_client.chat(
        [
            {
                "role": "user",
                "content": f"""
            {prompt}
            SERVICE_TYPE: {service_types.get(service_type)}
            QUERY: {query}
            """,
            }
        ]
    )
    return response


def is_video_search_need(query):
    """
    This function determines if the provided QUERY indicates a need for video search.

    Args:
        query (str): The search query to analyze.

    Returns:
        str: 'TRUE' if the QUERY suggests that a video search is needed,
              'FALSE' if it does not suggest a need for video search.
    """
    open_ai_client = OpenAIClient()

    prompt = """
    You are a helpful assistant.

    When a user provides a QUERY, determine if the QUERY indicates a need for video search (e.g., YouTube). 

    Please analyze the QUERY and respond with:
    - TRUE if the QUERY suggests that a video search is needed.
    - FALSE if the QUERY does not suggest a need for video search.

    Make sure to consider keywords and phrases that typically indicate a request for video content, such as "watch," "video," "clip," "film," or specific video-related questions.

    **Output Format:** Please respond with only TRUE or FALSE without any additional text or explanation.
    """
    response = open_ai_client.chat(
        [
            {
                "role": "user",
                "content": f"""
            {prompt}
            QUERY: {query}
            """,
            }
        ]
    )
    return response


def get_sorting_type(query):
    """
    This function determines if the provided QUERY indicates a need for sorting the search results.

    Args:
        query (str): The search query to analyze.

    Returns:
        str: 'LATEST' if the QUERY suggests that the search results should be sorted by the latest,
              'SIMILARITY' if the QUERY suggests that the search results should be sorted by similarity.
    """
    open_ai_client = OpenAIClient()

    prompt = """
    You are a helpful assistant.

    When a user provides a QUERY, determine if the QUERY indicates a need for sorting the search results by the latest or by similarity.

    Please analyze the QUERY and respond with:
    - "LATEST" if the QUERY suggests that the search results should be sorted by the latest.
    - "SIMILARITY" if the QUERY suggests that the search results should be sorted by similarity.

    Make sure to consider keywords and phrases that typically indicate a request for sorting, such as "latest," "new," "recent," "similar," or "related."

    **Output Format:** Please respond with only "LATEST" or "SIMILARITY" without any additional text or explanation.
    """
    response = open_ai_client.chat(
        [
            {
                "role": "user",
                "content": f"""
            {prompt}
            QUERY: {query}
            """,
            }
        ]
    )
    return response


def is_need_search(query):
    open_ai_client = OpenAIClient()

    prompt = """
    You are a helpful assistant.

    When a user provides a QUERY, determine if the QUERY indicates a need for an internet search.

    Please analyze the QUERY and respond with:
    - "TRUE" if the QUERY suggests that an internet search is needed.
    - "FALSE" if the QUERY does not suggest a need for an internet search.

    Make sure to consider keywords and phrases that typically indicate a request for information retrieval, such as "find," "search," "look up," "what is," "how to," or specific questions that require external information.

    **Output Format:** Please respond with only "TRUE" or "FALSE" without any additional text or explanation.
    """
    response = open_ai_client.chat(
        [
            {
                "role": "user",
                "content": f"""
            {prompt}
            QUERY: {query}
            """,
            }
        ]
    )
    return response


if __name__ == "__main__":
    print(is_need_search("침투부 영상에서 제일 재밌는 영상 추천해줘"))
