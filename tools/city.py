"""Tools that interact with the city resources."""

from __future__ import annotations

from fastmcp import Context, FastMCP

from config import ProjectConfig


def register(mcp: FastMCP, config: ProjectConfig) -> None:
    """Register tools that read from the resource layer."""

    @mcp.tool(name="city_insights")
    async def city_insights(city: str, ctx: Context) -> dict:
        """Return a structured summary for a city."""
        await ctx.info(f"Building insight for {city}")
        profile = await ctx.read_resource(f"cities://{city}/profile")
        snippet = f"{profile['name']} in {profile['country']} ({profile['timezone']})"
        notes = profile.get("notes", "")
        return {
            "summary": snippet,
            "population_millions": profile.get("population_millions"),
            "notes": notes,
        }

    @mcp.tool
    async def default_city(ctx: Context) -> dict:
        """Return the default city profile."""
        await ctx.debug("Loading default city profile from resources")
        profile = await ctx.read_resource("cities://default")
        return profile
