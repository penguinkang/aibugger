# API Reference

## `AIBugger`

The main controller class.

### `__init__(llm_client: Optional[LLMClient], handlers: Optional[List[NotificationHandler]])`
- **llm_client**: Instance of `LLMClient`. Defaults to `MockLLMClient` (no-op) if not provided.
- **handlers**: List of `NotificationHandler`. Defaults to `[ConsoleHandler()]`.

### `install()`
Hooks `sys.excepthook` to intercept uncaught exceptions.

### `uninstall()`
Restores the original `sys.excepthook`.

## LLM Clients

### `GeminiClient(api_key: str = None)`
Uses Google's Gemini Pro model.
- **api_key**: Defaults to `os.environ["GEMINI_API_KEY"]`.

### `OpenAIClient(api_key: str = None)`
Uses OpenAI's GPT-4 model.
- **api_key**: Defaults to `os.environ["OPENAI_API_KEY"]`.

## Handlers

### `ConsoleHandler`
Prints the analysis report to stdout.

### `SlackHandler(webhook_url: str)`
Sends the report to a Slack Incoming Webhook.

### `WebhookHandler(url: str)`
Sends a POST request with the report to any URL.
