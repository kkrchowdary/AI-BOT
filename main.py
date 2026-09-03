"""Main entrypoint for the AI-BOT application.

Provides a ChatBot class that wraps the language model + tool calls, a FastAPI
endpoint, and a CLI mode for interactive use.
"""
import json

import ollama
from fastapi import FastAPI, HTTPException
import uvicorn

from models import weather, chatRequest, chatResponse
from prompts import SYSTEM_PROMPT
from tools import TOOLS


MODEL = "llama3.2"
app = FastAPI()


OPTIONS = {
    "temperature": 0.7,
    "top_p": 0.9,
    "num_predict": 300,
    "num_ctx": 4096,
}


class ChatBot:
    """Manages chatbot interactions with the language model and tool calling.

    This class holds the conversation messages, calls the model, and handles
    any tool invocations that the model requests. It keeps the code modular
    so the same logic can be used for both the FastAPI endpoint and the CLI.
    """

    def __init__(self, model: str = MODEL, options: dict | None = None):
        """Initialize the chatbot with the given model and options.

        Args:
            model: Model name to use for ollama.chat.
            options: Generation options; if None, a copy of OPTIONS is used.
        """
        self.model = model
        # Avoid using a mutable default argument
        self.options = options.copy() if options is not None else OPTIONS.copy()
        self.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    def _call_model(self):
        """Call the underlying model and return a stream (generator) of chunks."""
        return ollama.chat(
            model=self.model,
            messages=self.messages,
            tools=TOOLS,
            stream=True,
            options=self.options,
        )

    def _consume_stream(self, stream):
        """Print content as it arrives; return (full_text, tool_calls|None).

        This consumes the streaming generator from ollama.chat, printing pieces
        to stdout and aggregating the content. If the model emits tool_calls,
        they will be returned for subsequent handling.
        """
        content = ""
        tool_calls = None
        for chunk in stream:
            msg = chunk["message"]
            if msg.get("tool_calls"):
                tool_calls = msg["tool_calls"]
            piece = msg.get("content")
            if piece:
                print(piece, end="", flush=True)
                content += piece
        return content, tool_calls

    def ask(self, user_input: str) -> str:
        """Process a user input string and return the bot's response.

        The method appends the user message, calls the model, handles any tool
        calls by invoking the appropriate helper (e.g., weather), and then
        obtains the final assistant response.
        """
        self.messages.append({"role": "user", "content": user_input})
        print("Bot: ", end="", flush=True)
        content, tool_calls = self._consume_stream(self._call_model())

        if tool_calls:
            # Record the assistant partial response that included the tool call
            self.messages.append({"role": "assistant", "content": content, "tool_calls": tool_calls})
            for call in tool_calls:
                function = call["function"] if isinstance(call, dict) else call.function
                name = function["name"] if isinstance(function, dict) else function.name
                arguments = function["arguments"] if isinstance(function, dict) else function.arguments

                # Resolve supported tool calls explicitly
                if name == "get_weather":
                    result = weather(arguments.get("city"))
                else:
                    result = {"error": f"Unknown tool '{name}'"}

                self.messages.append({"role": "tool", "content": json.dumps(result)})

            # Get final assistant response after tool outputs are available
            final_content, _ = self._consume_stream(self._call_model())
            print()
            self.messages.append({"role": "assistant", "content": final_content})
            return final_content

        print()
        self.messages.append({"role": "assistant", "content": content})
        return content


@app.post("/chat", response_model=chatResponse)
def askbot(payload: chatRequest):
    """Chat endpoint that accepts user input and returns bot response.

    Args:
        payload: chatRequest object containing user_input

    Returns:
        chatResponse object with bot reply
    """
    bot = ChatBot()
    try:
        reply = bot.ask(payload.user_input)
    except Exception as exc:
        # Use explicit exception chaining to preserve original traceback
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return chatResponse(reply=reply)


def run_cli():
    """Run the chatbot in CLI mode (interactive terminal)."""
    bot = ChatBot()
    print("AI chatbot (weather-aware). Type 'exit' or 'quit' to stop\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            print("Bot: Goodbye..!")
            break
        if not user_input:
            continue

        try:
            bot.ask(user_input)
            print()
        except Exception as exc:
            # Keep a broad catch here for CLI so the REPL doesn't crash;
            # in production code you might restrict this to expected errors.
            print(f"\nBot: Sorry, something went wrong: {exc}\n")


if __name__ == "__main__":
    # Run with: uvicorn main:app --reload
    # Or uncomment run_cli() below to run interactive CLI mode instead:
    # run_cli()

    uvicorn.run(
        "main:app",
        host="0.0.0.0",  # Listen on all network interfaces
        port=8000,        # Default FastAPI port
        reload=True,      # Auto-reload on code changes (disable in production)
    )
