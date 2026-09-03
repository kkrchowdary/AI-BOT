"""Tool definitions exported to the language model runtime.

The chat runtime expects a sequence (list/iterable) of tools describing what
external functions the assistant can call. For now this package exposes a
small, empty list so that the runtime receives a valid value. Add tool
specifications here if you integrate with ollama tool-calling features.
"""

from typing import List

# TOOLS should be a list of tool descriptors understood by the model runtime.
# Keep this empty until you have concrete tool definitions to avoid runtime
# errors during development.
TOOLS: List[dict] = []
