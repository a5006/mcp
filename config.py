"""Configuration helpers for the FastMCP starter project."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import List


@dataclass(slots=True)
class ProjectConfig:
    name: str = "FastMCP Demo Server"
    instructions: str = "Modular FastMCP starter with tools, resources, and prompts."
    version: str = "0.1.0"
    log_level: str = "INFO"
    resource_dir: Path = Path("resources")
    prompt_dir: Path = Path("prompts")
