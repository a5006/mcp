"""Configuration helpers for the FastMCP starter project."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import List
from urllib.parse import urljoin


@dataclass(slots=True)
class ProjectConfig:
    name: str = "Sangfor CMDB Assistant"
    instructions: str = (
        "You expose Sangfor CMDB lookups and mutations. "
        "Always rely on the provided cmdb tools/resources for product lines, "
        "user directories, and domain management."
    )
    version: str = "0.1.0"
    log_level: str = "INFO"
    resource_dir: Path = Path("resources")
    cmdb_base_url: str = "https://rudder.sangfor.com/cmdb/api/v1"
    cmdb_cookie: str = field(default_factory=lambda: os.getenv("CMDB_COOKIE", ""))

    def _zeus_base_url(self) -> str:
        base = self.cmdb_base_url.rstrip("/")
        if "/cmdb/api/v1" in base:
            return base.replace("/cmdb/api/v1", "/zeus/api/v1")
        return base

    @property
    def product_lines_url(self) -> str:
        """Zeus product catalog endpoint derived from cmdb_base_url."""
        return urljoin(self._zeus_base_url().rstrip("/") + "/", "common/product/search/")

    @property
    def user_directory_url(self) -> str:
        """Zeus user search endpoint derived from cmdb_base_url."""
        return urljoin(self._zeus_base_url().rstrip("/") + "/", "manage/user/search")

    @property
    def post_domain_url(self) -> str:
        """CMDB domain creation endpoint derived from cmdb_base_url."""
        return urljoin(self.cmdb_base_url.rstrip("/") + "/", "deploy/domain")

    @property
    def list_children_url(self) -> str:
        """CMDB children listing endpoint derived from cmdb_base_url."""
        return urljoin(
            self.cmdb_base_url.rstrip("/") + "/", "deploy/tree/root/children/list"
        )
