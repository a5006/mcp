"""Echo-focused tools."""

from __future__ import annotations

from fastmcp import Context, FastMCP

from config import ProjectConfig


def register(mcp: FastMCP, config: ProjectConfig) -> None:
    """Register echo-style helpers."""

    @mcp.tool
    async def echo(message: str, ctx: Context) -> str:
        """Return the supplied message verbatim."""
        await ctx.info(f"Echo request received: {message}")
        return message

    @mcp.tool
    async def repeat(message: str, times: int = 2, ctx: Context | None = None) -> str:
        """Repeat a message multiple times."""
        if times < 1:
            raise ValueError("times must be >= 1")
        if ctx:
            await ctx.debug(f"Repeating '{message}' {times} times")
        return " ".join(message for _ in range(times))
