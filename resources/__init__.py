"""CMDB-focused resource registrations."""

from __future__ import annotations

from typing import Any, Dict

import httpx
from fastmcp import Context, FastMCP

from config import ProjectConfig


async def _fetch_product_lines(
    *, cookie: str, url: str, rows: int
) -> Dict[str, Any]:
    headers = {
        "Accept": "application/json",
        "Cookie": cookie,
    }
    params = {"rows": rows}
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()


async def _fetch_user_directory(*, cookie: str, url: str, rows: int) -> Dict[str, Any]:
    headers = {
        "Accept": "application/json",
        "Cookie": cookie,
    }
    params = {"rows": rows}
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()


def register_resources(mcp: FastMCP, config: ProjectConfig) -> None:
    """Expose CMDB-adjacent resources (product lines, Zeus users)."""

    @mcp.resource("cmdb://product-lines{?rows}")
    async def cmdb_product_lines(
        ctx: Context,
        *,
        rows: int = 1000,
    ) -> Dict[str, Any]:
        """
        Return the CMDB product line catalog (产品线列表).

        Response structure:
        - `rows`: fixed value (1000) mirroring the query size.
        - `products`: list of product-line entries:
          - `product_id`: numeric identifier, use this value when calling POST/GET CMDB APIs.
          - `product_name`: human-friendly label; prefer this for UI display.
          - `business_id`: owning business unit ID.
          - `business_dept`: owning business department name (例如“威胁情报能力部”).
        - `raw`: untouched Zeus API payload.
        """
        if not config.cmdb_cookie:
            raise ValueError(
                "CMDB cookie is not configured. Set ProjectConfig.cmdb_cookie or CMDB_COOKIE env."
            )

        await ctx.info(f"Fetching CMDB product lines (rows={rows})")
        payload = await _fetch_product_lines(
            cookie=config.cmdb_cookie,
            url=config.product_lines_url,
            rows=rows,
        )
        return {
            "rows": rows,
            "products": payload.get("data", []),
            "raw": payload,
        }

    @mcp.resource("zeus://users{?rows}")
    async def zeus_user_directory(
        ctx: Context,
        *,
        rows: int = 1000,
    ) -> Dict[str, Any]:
        """
        Return the Zeus user directory listing.

        Response structure:
        - `rows`: integer echo of the requested page size.
        - `users`: list of user objects with fields
          - `id`: numeric user ID.
          - `name`: short account/username (工号).
          - `display_name`: preferred UI label.
          - `full_name`: canonical “姓名+账号” 字段，优先用于精确匹配。
          - `group`: organizational path such as `/司舵`.
          - `role`: textual role description (e.g., “普通人员”).
        - `raw`: untouched Zeus API payload for troubleshooting.
        """
        if not config.cmdb_cookie:
            raise ValueError(
                "CMDB cookie is not configured. Set ProjectConfig.cmdb_cookie or CMDB_COOKIE env."
            )

        await ctx.info(f"Fetching Zeus user directory (rows={rows})")
        payload = await _fetch_user_directory(
            cookie=config.cmdb_cookie,
            url=config.user_directory_url,
            rows=rows,
        )
        return {
            "rows": rows,
            "users": payload.get("data", []),
            "raw": payload,
        }
