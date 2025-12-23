import sys
sys.path.append('src')
from aibugger import AIBugger, MockLLMClient

def main():
    # Initialize AIBugger with the Mock Client (so we don't need API keys for this demo)
    # It defaults to ConsoleHandler, which is what we want to see.
    debugger = AIBugger(llm_client=MockLLMClient())
    debugger.install()

    print("Running some dangerous code...")
    result = 1 / 0  # This will crash
    print(f"Result: {result}")

if __name__ == "__main__":
    main()
