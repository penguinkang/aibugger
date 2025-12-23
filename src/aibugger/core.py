import sys
import traceback
from typing import List, Optional, Type
from types import TracebackType
from .llm import LLMClient, MockLLMClient
from .handlers import NotificationHandler, ConsoleHandler

class AIBugger:
    def __init__(self, llm_client: Optional[LLMClient] = None, handlers: Optional[List[NotificationHandler]] = None):
        self.llm_client = llm_client or MockLLMClient() # Default to mock for safety, user should override
        self.handlers = handlers or [ConsoleHandler()]
        self._original_excepthook = sys.excepthook

    def install(self):
        """Install the exception hook."""
        sys.excepthook = self.handle_exception
        print("AIBugger installed. Ready to catch exceptions.")

    def uninstall(self):
        """Restore the original exception hook."""
        sys.excepthook = self._original_excepthook
        print("AIBugger uninstalled.")

    def handle_exception(self, exc_type: Type[BaseException], exc_value: BaseException, exc_traceback: TracebackType):
        """Custom exception handler."""
        # First, ensure valid strings
        etype_str = exc_type.__name__
        evalue_str = str(exc_value)
        tb_str = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))

        # 1. Print original traceback first so user sees it immediately
        # (We can rely on sys.__excepthook__ or just print it ourselves)
        # Using original excepthook might be better to prefer standard behavior
        self._original_excepthook(exc_type, exc_value, exc_traceback)

        # 2. Analyze with LLM
        try:
            analysis = self.llm_client.analyze_exception(etype_str, evalue_str, tb_str)
        except Exception as e:
            analysis = f"Error during AI analysis: {e}"

        # 3. Notify handlers
        context = {
            "exception_type": etype_str,
            "exception_value": evalue_str,
            "traceback": tb_str
        }
        
        for handler in self.handlers:
            try:
                handler.handle(analysis, context)
            except Exception as h_err:
                print(f"Error in notification handler {type(handler).__name__}: {h_err}")
