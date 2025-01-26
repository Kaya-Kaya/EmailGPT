from abc import ABC, abstractmethod
import os

class LLM(ABC):
    def __init__(self, token: str, model: str, temperature: float = 1.0):
        '''Initialize the LLM with token, model, and temperature.'''
        self.token = token
        self.model = model
        self.temperature = temperature

        # Read the prompt from a file
        with open("emailgpt/prompt.txt", "r") as file:
            self.prompt = file.read()

    @abstractmethod
    def respond(self, message: str, stream: bool = False) -> str:
        '''Respond to a message.'''
        pass

    @abstractmethod
    def message(self, role: str, message: str) -> None:
        '''Add a message with a specific role.'''
        pass

    @abstractmethod
    def respond_no_memory(self, message: str) -> str:
        '''Respond to a message without memory.'''
        pass

class ChatGPT(LLM):
    def __init__(self, token: str = os.getenv("OPENAI_API_KEY"), model: str = "gpt-4o-mini", temperature: float = 1.0):
        super().__init__(token, model, temperature)

        from openai import OpenAI

        self.client = OpenAI(api_key=self.token)
        # Initialize messages with the developer's prompt
        self.messages = [{"role": "developer", "content": self.prompt}]

    def respond(self, message: str, stream: bool = False) -> str:
        self.messages.append({"role": "user", "content": message})

        # Get response from the model
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            temperature=self.temperature,
            max_tokens=256
        ).choices[0].message.content

        # Add assistant's response to the conversation
        self.messages.append({"role": "assistant", "content": response})
        return response
    
    def message(self, role: str, message: str) -> None:
        self.messages.append({"role": role, "content": message})

    def respond_no_memory(self, message: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages + [{"role": "user", "content": message}],
            temperature=self.temperature,
            max_tokens=256
        ).choices[0].message.content
        return response