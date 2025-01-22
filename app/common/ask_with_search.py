"""
This module provides functionality to interact with the Naver API
and to facilitate chat responses based on search results.
"""

from common.client import (
    NaverAPIClient,
    OpenAIClient,
    KakaoAPIClient,
    GoogleAPIClient,
    get_sorting_type,
    is_need_search,
)


def chat_with_search(question, history=None):
    """
    This function interacts with the Naver API to perform a search based on the user's question
    and formulates a response using the search results.

    Args:
        question (str): The question asked by the user.
        history (list): A list of previous chat messages (default is an empty list).

    Returns:
        str: The response generated based on the search results and user question.
    """
    if history is None:
        history = []  # Initialize history as an empty list if None

    openai_client = OpenAIClient()
    naver_client = NaverAPIClient()
    kakao_client = KakaoAPIClient()
    google_client = GoogleAPIClient()

    real_search = None
    if is_need_search(question) == "TRUE":
        sorting_type = get_sorting_type(question)
        if sorting_type == "LATEST":
            naver_search = naver_client.search(query=question, sort="date")
            kakao_search = kakao_client.search(query=question, sort="recency")
        else:
            naver_search = naver_client.search(query=question)
            kakao_search = kakao_client.search(query=question)
        google_search = google_client.search(query=question)
        real_search = {
            "search time": naver_search.get("lastBuildDate"),
            "items": list(naver_search.get("items"))
            + list(kakao_search.get("documents"))
            + list(google_search.get("items")),
        }

    prompt_role = """
        You are a helpful assistant.
        When a user asks a question, use the provided search results (REAL_SEARCH) to formulate your response. 
        If REAL_SEARCH is not available, provide a general answer based on your knowledge.
        You should generally respond in a formal manner. However, if the user requests to change your chat style, you should switch to what they need.
        
        Ensure that your answer is relevant to the user's inquiry and incorporates information from the search results when available. 
        For example, if the user asks about a specific topic, summarize the key points from the REAL_SEARCH and provide a clear and concise answer. 
        If there are no search results, respond with a helpful and informative answer based on what you know.
        Always aim to assist the user by delivering accurate and helpful information based on the search results or your general knowledge.
    """

    prompt = f"""
        {prompt_role}
        REAL_SEARCH: 
            {real_search}
        USER: {question}
    """
    return openai_client.chat(history + [{"role": "user", "content": prompt}])
