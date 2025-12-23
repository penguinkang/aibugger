# AIBugger 🤖

**AIBugger** is a powerful, AI-driven debugging tool for Python. It automatically catches exceptions, analyzes them using an LLM, and provides actionable fixes and explanations directly in your console (or via Slack/Webhooks).

## Features
- 🪝 **Automatic Exception Hooking**: Catches uncaught exceptions seamlessly.
- 🧠 **AI Analysis**: Uses Gemini or OpenAI to explain *why* the error happened.
- 🚀 **Multi-Channel Notifications**:
    - Console (Default)
    - Slack
    - Custom Webhooks
- 🔌 **Pluggable Architecture**: Easily add your own handlers or LLM providers.

## Installation

```bash
pip install aibugger
```

*(Note: Package is not yet on PyPI, install from source/git)*

## Usage

### Basic Usage (Console)

```python
from aibugger import AIBugger, GeminiClient

# Initialize with your API key
client = GeminiClient(api_key="your-api-key")
debugger = AIBugger(llm_client=client)

# Install the hook
debugger.install()

# Your code here...
print(1 / 0)  # Exception will be caught and analyzed!
```

### Slack Integration

```python
from aibugger import AIBugger, OpenAIClient, SlackHandler

client = OpenAIClient(api_key="sk-...")
slack = SlackHandler(webhook_url="https://hooks.slack.com/...")

debugger = AIBugger(llm_client=client, handlers=[slack])
debugger.install()
```

## Configuration

You can also use environment variables:
- `GEMINI_API_KEY`
- `OPENAI_API_KEY`
