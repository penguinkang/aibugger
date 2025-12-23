from abc import ABC, abstractmethod
import logging
import requests
import json
from typing import Any, Dict, Optional

class NotificationHandler(ABC):
    @abstractmethod
    def handle(self, error_report: str, context: Optional[Dict[str, Any]] = None) -> None:
        """Handle the error report notification."""
        pass

class ConsoleHandler(NotificationHandler):
    def handle(self, error_report: str, context: Optional[Dict[str, Any]] = None) -> None:
        print("\n" + "="*80)
        print("🤖 AIBugger Report 🤖")
        print("="*80)
        print(error_report)
        print("="*80 + "\n")

class WebhookHandler(NotificationHandler):
    def __init__(self, url: str):
        self.url = url

    def handle(self, error_report: str, context: Optional[Dict[str, Any]] = None) -> None:
        try:
            payload = {
                "text": error_report,
                "context": context or {}
            }
            response = requests.post(self.url, json=payload)
            response.raise_for_status()
        except Exception as e:
            logging.error(f"Failed to send webhook notification: {e}")

class SlackHandler(NotificationHandler):
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def handle(self, error_report: str, context: Optional[Dict[str, Any]] = None) -> None:
        try:
            # Format specifically for Slack blocks if needed, but text is fine for simple implementation
            payload = {
                "text": f"🚨 *Exception Detected* 🚨\n\n{error_report}"
            }
            response = requests.post(self.webhook_url, json=payload)
            response.raise_for_status()
        except Exception as e:
            logging.error(f"Failed to send Slack notification: {e}")
