"""Tools that leverage registered prompts."""

from __future__ import annotations

from typing import Any, Dict, List

from fastmcp import Context, FastMCP

from config import ProjectConfig


def _serialize_messages(messages: List[Any]) -> List[Dict[str, Any]]:
    serialized: List[Dict[str, Any]] = []
    for message in messages:
        if hasattr(message, "model_dump"):
            serialized.append(message.model_dump())
        else:
            serialized.append({"role": "user", "content": str(message)})
    return serialized


def register(mcp: FastMCP, config: ProjectConfig) -> None:
    """Register prompt-centric utilities."""

    @mcp.tool
    async def prompt_runner(city: str, ctx: Context) -> dict:
        """Render the itinerary prompt for a city and return the raw messages."""
        await ctx.info(f"Rendering itinerary_brief prompt for {city}")
        prompt = await mcp.prompts.render_prompt("itinerary_brief", {"city": city})
        return {
            "description": prompt.description,
            "messages": _serialize_messages(prompt.messages),
        }
