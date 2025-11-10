"""Tool registrations for the FastMCP project."""

from __future__ import annotations

from fastmcp import FastMCP

from config import ProjectConfig
from . import city, echo, prompt_runner

MODULE_MAP = {
    "echo": echo,
    "city": city,
    "prompt_runner": prompt_runner,
}


def register_tools(mcp: FastMCP, config: ProjectConfig) -> None:
    """Eagerly register every tool module."""
    for module in MODULE_MAP.values():
        module.register(mcp, config)
