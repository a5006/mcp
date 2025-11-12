"""Tools that integrate with the Sangfor CMDB domain APIs."""

from __future__ import annotations

import httpx
from fastmcp import Context, FastMCP

from config import ProjectConfig


async def _fetch_children(
    *,
    url: str,
    cookie: str,
    params: dict[str, str | int],
) -> dict:
    headers = {
        "Accept": "application/json",
        "Cookie": cookie,
    }
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(
            url,
            params=params,
            headers=headers,
        )
        response.raise_for_status()
        return response.json()


async def _create_domain(
    *,
    url: str,
    cookie: str,
    payload: dict[str, str | int | bool],
) -> dict:
    headers = {
        "Accept": "application/json",
        "Cookie": cookie,
        "Content-Type": "application/json",
    }
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            url,
            json=payload,
            headers=headers,
        )
        response.raise_for_status()
        return response.json()


def register(mcp: FastMCP, config: ProjectConfig) -> None:
    """Register CMDB-related tools."""

    @mcp.tool(name="exist_cmdb_domain_list")
    async def exist_cmdb_domain_list(
        ctx: Context,
        *,
        page: int = 1,
        rows: int = 10000,
        product_id: str = "",
        children_type: int = 3,
    ) -> dict:
        """
        Return existing CMDB domain records (deployDomain) with configurable filters.

        Response payload:
        - `query`: the exact params sent upstream.
        - `total`: total record count returned by CMDB.
        - `domains`: list of domain objects. Important fields include
          - `addr`: unique domain/addr string (使用该字段作为主键).
          - `domainId`/`id`: numeric identifiers.
          - `domainType` + `domainTypeName`: 内网/外网等分类信息.
          - `serveType`, `recordType`, `reflectAddr`, `regionId`/`regionName`.
          - ownership metadata such as `productId`, `productName`, `teamId`, `teamName`,
            `devBy`, `opsBy`, `useBy`, timestamps (`createdAt`, `updatedAt`).
        - `raw`: untouched response for debugging.

        LLM callers should treat `addr` as the canonical key when matching or deduplicating domain data.
        """
        if not config.cmdb_cookie:
            raise ValueError(
                "CMDB cookie is not configured. Set ProjectConfig.cmdb_cookie or CMDB_COOKIE env."
            )

        params = {
            "page": page,
            "rows": rows,
            "productId": product_id,
            "childrenType": children_type,
        }

        await ctx.info(
            f"Requesting CMDB domain list with rows={rows}, page={page}, productId='{product_id}'"
        )
        payload = await _fetch_children(
            url=config.list_children_url,
            cookie=config.cmdb_cookie,
            params=params,
        )

        data = payload.get("data", {})
        domain_list = (data.get("list") or {}).get("deployDomain") or []
        return {
            "query": params,
            "total": data.get("cnt", len(domain_list)),
            "domains": domain_list,
            "raw": payload,
        }

    @mcp.tool(name="create_cmdb_domain")
    async def create_cmdb_domain(
        ctx: Context,
        *,
        addr: str,
        product_id: int,
        team_id: int,
        use_describe: str,
        dev_by: str,
        ops_by: str,
        use_by: str,
        serve_type: str = "http",
        domain_type: int = 2,
        status: int = 2,
        region_id: int = 1,
        is_detection: bool = False,
    ) -> dict:
        """
        Create a new CMDB domain entry via /deploy/domain.

        Args:
            addr: 域名地址（“域名地址�?）.
            product_id: 产品线 ID（“产品线�?下拉框的值）.
            team_id: 开发团队 ID（“开发团队�?）.
            use_describe: 使用描述（“使用描述�?）.
            dev_by: 开发负责人（“开发负责人�?）.
            ops_by: 运维负责人（“运维负责人�?）.
            use_by: 使用人（“使用人�?）.
            serve_type: 协议/协议类型，https 或 http（“协议�?单选）.
            domain_type: 域名类型，1=内网域名，2=外网域名（“域名类型�?）.
            status: 状态，1=下线，2=上线（“状态�?单选）.
            region_id: 区域，1=国内，2=海外（“区域�?单选）.
            is_detection: 是否启用摸测，True=启用，False=禁用（“是否启用摸测�?）.
        """
        if not config.cmdb_cookie:
            raise ValueError(
                "CMDB cookie is not configured. Set ProjectConfig.cmdb_cookie or CMDB_COOKIE env."
            )

        payload = {
            "useDescribe": use_describe,
            "isDetection": is_detection,
            "serveType": serve_type,
            "domainType": domain_type,
            "status": status,
            "regionId": region_id,
            "addr": addr,
            "teamId": team_id,
            "devBy": dev_by,
            "opsBy": ops_by,
            "useBy": use_by,
            "productId": product_id,
        }

        await ctx.info(f"Creating CMDB domain '{addr}' for product {product_id}")
        response = await _create_domain(
            url=config.post_domain_url,
            cookie=config.cmdb_cookie,
            payload=payload,
        )
        return {
            "request": payload,
            "result": response,
        }
