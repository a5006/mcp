"""FastMCP resource registrations."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from fastmcp import Context, FastMCP

from config import ProjectConfig


def _load_city_data(base_dir: Path) -> Dict[str, Any]:
    path = base_dir / "city_data.json"
    if not path.exists():
        raise FileNotFoundError(f"Missing resource file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def _city_index(records: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    return {entry["name"].lower(): entry for entry in records}


def register_resources(mcp: FastMCP, config: ProjectConfig) -> None:
    """Register sample resources backed by static JSON."""
    data = _load_city_data(config.resource_dir)
    cities = data.get("cities", [])
    city_lookup = _city_index(cities)

    @mcp.resource("cities://default")
    def default_city() -> Dict[str, Any]:
        """Return the default city metadata."""
        default_name = data.get("default_city", "")
        return city_lookup.get(default_name.lower(), {"name": default_name})

    @mcp.resource("cities://{city}/profile")
    async def city_profile(city: str, ctx: Context) -> Dict[str, Any]:
        """Return metadata for a single city and log the access."""
        record = city_lookup.get(city.lower())
        if not record:
            await ctx.error(f"Unknown city requested: {city}")
            raise ValueError(f"City '{city}' is not available.")
        await ctx.info(f"Loaded city profile for {record['name']}")
        return record
