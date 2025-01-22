"""
This is an example of how to use the OpenAI API to ask a question using a microphone.
"""

from typing import List

from common.client import OpenAIClient


STARTING_PROMPT = """
    You are a helpful assistant.
    You can discuss with the user, or perform some actions like sending an email.
    If user ask you to send an email, you have to ask for the subject, recipient, and message.
    You will receive either intructions starting with [INSTRUCTION] and respond questions.
    Follow the [INSTRUCTION] and respond questions.
    but, if the user wants to exit the conversation, write "EXIT" only one word.
"""

prompts = {
    "START": """
        [INSTRUCTION]
            Write "WRITE_EMAIL" if the user wants to write an email, 
            "QUESTION" if the user has a precise question, 
            "OTHER"  in any other case. Only write one word,
            Only answer one word.
    """,
    "QUESTION": """
        [INSTRUCTION]
            If you can answer the question: ANSWER,
            if you need more information: MORE,
            if you cannot answer: OTHER. Only answer one word.
    """,
    "ANSWER": """
        [INSTRUCTION]
            Answer the user question
    """,
    "MORE": """
        [INSTRUCTION]
            Ask the user for more information as specified by previous intructions
    """,
    "OTHER": """
        [INSTRUCTION]
            Give a polite answer or greetings if the user is making polite conversation. 
            Else, answer to the user that you cannot answer the question or do the action.
    """,
    "WRITE_EMAIL": """
        [INSTRUCTION]
           If the subject or recipient or body is missing, answer "MORE". 
           Else if you have all the information answer 
           "ACTION_WRITE_EMAIL | subject:subject, recipient:recipient, message:message".
           
    """,
    "ACTION_WRITE_EMAIL": """
        [INSTRUCTION]
            The mail has been sent. 
            Answer to the user to tell the action is done
    """,
    "EXIT": """
        [INSTRUCTION]
            Not answer "EXIT" only one word.
            Answer the user to tell the conversation is ended very politely.
    """,
}

actions = ["ACTION_WRITE_EMAIL"]


class Chat:
    """
    This class is used to chat with the user.
    """

    def __init__(
        self,
        state: str = "START",
        history: List[dict] = None,
    ) -> None:
        self.previous_state = None
        self.state = state
        self.history = (
            history
            if history is not None
            else [
                {"role": "system", "content": STARTING_PROMPT},
            ]
        )
        self.client = OpenAIClient()

    def reset(self):
        """
        This function is used to reset the chat.
        """
        self.previous_state = None
        self.state = "START"
        self.history = [{"role": "system", "content": STARTING_PROMPT}]

    def reset_to_previous_state(self):
        """
        This function is used to reset the chat to the previous state.
        """
        self.state = self.previous_state
        self.previous_state = None

    def to_state(self, state: str):
        """
        This function is used to change the state.

        Args:
            state: The state to change to.
        """
        self.previous_state = self.state
        self.state = state

    def do_action(self, action: str) -> str:
        """
        This function is used to do the action.

        Args:
            action: The action to do.

        Returns:
            The result of the action.
        """
        print(f"DEBUG perform action={action}")

    def discuss(self, user_input: str = None) -> str:
        """
        This function is used to continue the conversation.

        Args:
            user_input: The user input. If None, just use the action prompts.

        Returns:
            The response of the conversation.
        """
        if user_input:
            self.history.append({"role": "user", "content": user_input})

        complete_messages = self.history + [{"role": "user", "content": prompts[self.state]}]
        _response = self.client.chat(complete_messages)

        # If the response is in prompts, change the state
        if _response in prompts:
            self.to_state(_response)
            return self.discuss()

        # If the response is an action, perform the action
        if _response.split("|")[0].strip() in actions:
            action = _response.split("|")[0].strip()
            self.to_state(action)
            self.do_action(_response)
            return self.discuss()

        # If the response is not an action, add it to the history
        self.history.append({"role": "assistant", "content": _response})

        if self.state == "EXIT":
            self.reset()
        else:
            self.reset_to_previous_state()
        return _response
