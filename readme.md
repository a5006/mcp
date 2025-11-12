# FastMCP CMDB Assistant

Minimal FastMCP server dedicated to Sangfor CMDB workflows. It exposes only the
domain lookup / creation tools plus supporting resources (product lines, Zeus
user directory) so LLM clients can reason about CMDB data without any demo
features like city prompts or echo helpers.

## Project Layout

```
.
├─ app.py              # Builds the FastMCP instance and runs the server
├─ config.py           # ProjectConfig with CMDB + Zeus endpoint helpers
├─ logging_config.py   # Rich console + file logging setup
├─ resources/          # CMDB product lines + Zeus users @resource definitions
├─ tools/              # CMDB domain tools (list + create)
├─ fastmcp.json        # FastMCP CLI config (transport / host / port)
├─ pyproject.toml
├─ requirements.txt
└─ README.md
```

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -e ".[dev]"
fastmcp dev                # uses fastmcp.json (HTTP + SSE)
```

Set `CMDB_COOKIE` in your shell or `.env` so both tools and resources can call
the Sangfor endpoints.

## Configuration

`ProjectConfig` defines:

- `cmdb_base_url`: defaults to `https://rudder.sangfor.com/cmdb/api/v1`.
- `cmdb_cookie`: pulled from `CMDB_COOKIE`.
- `product_lines_url`, `user_directory_url`, `list_children_url`,
  `post_domain_url`: derived helpers so every module uses consistent URLs.

## Tools (`tools/cmdb.py`)

- **exist_cmdb_domain_list** – GET `/deploy/tree/root/children/list`
  - Params: `page`, `rows` (default 10000), `productId`, `childrenType`.
  - Returns `{ query, total, domains[], raw }`.
  - `domains[]` fields include:
    - `addr`: unique domain/addr string (主键，用于匹配/去重).
    - `domainId`/`id`, `productId`, `productName`, `teamId`, `teamName`.
    - Contacts: `devBy`, `opsBy`, `useBy`.
    - Network metadata: `domainType`, `domainTypeName`, `serveType`,
      `recordType`, `reflectAddr`, `regionId`, `regionName`.
    - Audit info: `createdAt`, `updatedAt`, `createBy`, `updateBy`.
- **create_cmdb_domain** – POST `/deploy/domain`
  - Payload mirrors the CMDB UI fields (`addr`, `productId`, `teamId`,
    `serveType`, `domainType`, `status`, `regionId`, contacts, description).
  - Response returns `{ request, result }` for traceability.

Both tools validate that `cmdb_cookie` is set before making requests.

## Resources (`resources/__init__.py`)

- **`cmdb://product-lines`**
  - Calls `product_lines_url`.
  - Response: `{ rows: 1000, products[], raw }`.
  - `products[]` fields: `product_id`, `product_name`, `business_id`,
    `business_dept`. Display `product_name`, but send `product_id` to CMDB APIs.
- **`zeus://users{?rows}`**
  - Calls `user_directory_url` with configurable `rows` (default 1000).
  - Response: `{ rows, users[], raw }`.
  - `users[]` fields: `id`, `name` (account), `display_name`, `full_name`
    (优先使用), `group`, `role`.

## Logging

`logging_config.py` routes Rich logs to the console and `logs/fastmcp.log`.
Within tools/resources, use `ctx.info`/`ctx.error` so MCP clients receive
progress updates while operations run.

## 中文速览

- 该项目仅保留 CMDB 相关能力：`exist_cmdb_domain_list` / `create_cmdb_domain`
  工具，以及 `cmdb://product-lines`、`zeus://users` 资源。
- `addr` 是域名查询结果的唯一键，LLM 去重或匹配时务必按 `addr` 判断。
- `product_name` 适合给用户展示，但在 POST/GET 参数中必须传 `product_id`。
- `full_name`（姓名+工号）是 Zeus 用户目录的首选匹配字段。
- 启动前在环境变量或 `.env` 中设置 `CMDB_COOKIE`，再运行 `fastmcp dev`
  即可通过 MCP 客户端调用以上能力。
