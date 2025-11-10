"""Prompt registrations for the FastMCP server."""

from __future__ import annotations

from pathlib import Path

from fastmcp import FastMCP

from config import ProjectConfig


def _read_prompt(prompt_dir: Path, filename: str) -> str:
    path = prompt_dir / filename
    if not path.exists():
        raise FileNotFoundError(f"Missing prompt file: {path}")
    return path.read_text(encoding="utf-8").strip()


def register_prompts(mcp: FastMCP, config: ProjectConfig) -> None:
    """Register reusable prompt templates."""
    system_prompt = _read_prompt(config.prompt_dir, "system_prompt.txt")

    @mcp.prompt
    def operating_context() -> str:
        """Base system prompt used by downstream assistants."""
        return system_prompt

    @mcp.prompt
    def itinerary_brief(city: str) -> str:
        """Prompt template that requests a structured travel brief."""
        return (
            "You are a travel planning assistant. "
            f"Create a short itinerary overview for {city}, "
            "highlighting key neighborhoods, signature cuisine, "
            "and one hidden gem locals love."
        )
