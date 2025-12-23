from abc import ABC, abstractmethod
import os
import requests

class LLMClient(ABC):
    @abstractmethod
    def analyze_exception(self, exception_type: str, exception_message: str, stack_trace: str) -> str:
        pass

class MockLLMClient(LLMClient):
    """Used for testing without API keys."""
    def analyze_exception(self, exception_type: str, exception_message: str, stack_trace: str) -> str:
        return (
            f"Analysis of {exception_type}: {exception_message}\n\n"
            "CAUSE:\n"
            "This is a mock analysis. The exception likely occurred because something went wrong.\n\n"
            "SUGGESTED FIX:\n"
            "1. Check your logic.\n"
            "2. Add try/except blocks.\n"
            "3. Verify inputs."
        )

class GeminiClient(LLMClient):
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is not set.")
        self.url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

    def analyze_exception(self, exception_type: str, exception_message: str, stack_trace: str) -> str:
        prompt = (
            f"You are an expert Python debugger. Explain the following exception clearly and provide 3 actionable fixes.\n\n"
            f"Exception Type: {exception_type}\n"
            f"Message: {exception_message}\n"
            f"Stack Trace:\n{stack_trace}\n"
        )
        
        headers = {"Content-Type": "application/json"}
        params = {"key": self.api_key}
        data = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
        try:
            response = requests.post(self.url, headers=headers, params=params, json=data)
            response.raise_for_status()
            result = response.json()
            return result['candidates'][0]['content']['parts'][0]['text']
        except Exception as e:
            return f"Failed to get analysis from Gemini: {str(e)}"

class OpenAIClient(LLMClient):
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is not set.")
        self.url = "https://api.openai.com/v1/chat/completions"

    def analyze_exception(self, exception_type: str, exception_message: str, stack_trace: str) -> str:
        prompt = (
            f"Analyze this Python exception:\n"
            f"Type: {exception_type}\n"
            f"Message: {exception_message}\n"
            f"Stack Trace:\n{stack_trace}\n\n"
            "Provide a clear explanation and 3 specific solutions."
        )
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        data = {
            "model": "gpt-4",
            "messages": [
                {"role": "system", "content": "You are a helpful debugging assistant."},
                {"role": "user", "content": prompt}
            ]
        }

        try:
            response = requests.post(self.url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content']
        except Exception as e:
            return f"Failed to get analysis from OpenAI: {str(e)}"
