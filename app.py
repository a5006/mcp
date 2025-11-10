"""Entrypoint that assembles the FastMCP server."""

from __future__ import annotations

from fastmcp import FastMCP

from config import ProjectConfig
from logging_config import setup_logging
from prompts import register_prompts
from resources import register_resources
from tools import register_tools


def build_app(config: ProjectConfig | None = None) -> FastMCP:
    """Create and configure the FastMCP server instance."""
    config = config or ProjectConfig()
    setup_logging(config.log_level)

    mcp = FastMCP(
        config.name,
        instructions=config.instructions,
        version=config.version,
    )

    register_resources(mcp, config)
    register_prompts(mcp, config)
    register_tools(mcp, config)

    return mcp


def main() -> None:
    """Console-script entrypoint."""
    build_app().run()


server = build_app()


if __name__ == "__main__":
    main()
