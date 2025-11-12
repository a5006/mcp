"""Tool registrations for the FastMCP project."""

from __future__ import annotations

from fastmcp import FastMCP

from config import ProjectConfig
from . import cmdb


def register_tools(mcp: FastMCP, config: ProjectConfig) -> None:
    """Eagerly register every tool module."""
    cmdb.register(mcp, config)
