"""Prompts used by the AI-BOT application.

Keep prompts small and focused. This module centralizes system and developer
prompts so they can be easily tested and updated.
"""

SYSTEM_PROMPT = (
    "You are an AI assistant that helps users and can call a small set of tools "
    "to look up real-world facts such as current weather. Be helpful, concise, "
    "and ask clarifying questions when the user request is ambiguous."
)
