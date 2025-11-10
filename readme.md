# FastMCP Modular Starter

This project follows the official [FastMCP docs](https://gofastmcp.com/getting-started/welcome)
and wires up a production-style server with tools, resources, prompts, and
structured logging. Use it as a reference when building Model Context Protocol
(MCP) servers with the `fastmcp` Python library.

## Project Layout

```
.
├─ app.py              # Builds the FastMCP instance and runs the server
├─ config.py           # Dataclass configuration used across modules
├─ logging_config.py   # Rich console + file logging setup
├─ tools/              # FastMCP @tool definitions (echo, city, prompt_runner)
├─ resources/          # FastMCP @resource definitions backed by JSON
├─ prompts/            # FastMCP @prompt templates (system + itinerary)
├─ fastmcp.json        # FastMCP CLI config (transport / host / port)
├─ pyproject.toml      # Declares the fastmcp dependency and console script
├─ requirements.txt
└─ README.md
```

## Prerequisites

- Python 3.10+ (this starter is currently developed and tested with **Python 3.14.0**)
- `pip install fastmcp` (the library automatically installs its CLI)
- Familiarity with the FastMCP quickstart: [gofastmcp.com/getting-started/welcome](https://gofastmcp.com/getting-started/welcome)

## Setup & Local Run

```powershell
python -m venv .venv
.\.venv\Scripts\activate   # Windows PowerShell activation
pip install -e ".[dev]"

# Option 1: use the fastmcp.json config (HTTP + SSE by default)
fastmcp dev

# Option 2: force STDIO for legacy clients
fastmcp run app.py --transport stdio

# Option 3: use the helper console script defined in pyproject.toml (STDIO)
fastmcp-run
```

If you're on macOS/Linux, activate the same virtual environment via:

```bash
source .venv/bin/activate
```

### Choosing a transport (STDIO / HTTP / SSE)

The repo includes a [`fastmcp.json`](./fastmcp.json) file. Running `fastmcp dev`
now auto-detects that configuration and starts the server with the specified
transport. The default is `streamable-http`, which exposes both HTTP JSON and
SSE streaming endpoints on `http://127.0.0.1:8000/`.

Edit the `deployment.transport` field in `fastmcp.json` to switch modes:

```jsonc
{
  "deployment": {
    "transport": "streamable-http", // stdio | http | sse | streamable-http
    "host": "127.0.0.1",
    "port": 8000
  }
}
```

- `streamable-http` – HTTP + SSE (default)
- `sse` – SSE-only channel (great for Claude Desktop)
- `http` – HTTP polling
- `stdio` – classic MCP STDIO transport

You can still override the transport ad hoc via CLI options
(`fastmcp run app.py --transport sse`), but checking the value into
`fastmcp.json` keeps the behavior consistent for everyone.

## Modules

- **Tools** (`tools/`)  
  - `echo.py`: echo + repeat helpers that log via `ctx.info`/`ctx.debug`.
  - `city.py`: reads the JSON resources using `ctx.read_resource`.
  - `prompt_runner.py`: renders the registered prompts through `mcp.prompts.render_prompt`.

- **Resources** (`resources/`)  
  `cities://default` and `cities://{city}/profile` come from `city_data.json`
  and demonstrate FastMCP's `@mcp.resource` decorator plus contextual logging.

- **Prompts** (`prompts/`)  
  Two prompt templates show how to keep your LLM system instructions in files
  and expose them through `@mcp.prompt`.

## Logging

- `logging_config.py` configures Rich console output and mirrors everything to
  `logs/fastmcp.log` for later inspection.
- Inside tools/resources we log to MCP clients with the `Context` helpers
  (`ctx.info`, `ctx.debug`, `ctx.error`) described in the docs.
  This matches the guidance under *“Context & Logging”* in the FastMCP welcome guide.

## Extending

1. Duplicate an existing module, add your FastMCP decorators, and call
   `module.register(mcp, config)` from `tools/__init__.py`, `resources/__init__.py`,
   or `prompts/__init__.py`.
2. Update `ProjectConfig` metadata (name, description, log level) or tweak
   `fastmcp.json` (transport / host / port) to suit your deployment.
3. Re-run `fastmcp-run` or `fastmcp run app.py` to expose the new
   functionality to your MCP client.

---

## 中文说明

### 项目简介
本示例遵循 [FastMCP 官方文档](https://gofastmcp.com/getting-started/welcome)，提供一个带有工具、资源、提示词以及结构化日志的标准 MCP 服务器骨架，可直接用于基于 `fastmcp` 库的生产级开发。

### 目录结构

```
.
├─ app.py              # 创建 FastMCP 实例并运行服务器
├─ config.py           # 项目级配置
├─ logging_config.py   # Rich 控制台 + 文件日志
├─ tools/              # @mcp.tool 定义（echo、city、prompt_runner）
├─ resources/          # @mcp.resource 定义（基于 city_data.json）
├─ prompts/            # @mcp.prompt 模板（system + itinerary）
├─ fastmcp.json        # CLI 配置（传输模式 / 主机 / 端口）
├─ pyproject.toml      # 依赖与控制台脚本
└─ README.md
```

### 环境要求

- Python 3.10+（当前使用 **Python 3.14.0** 开发与测试）
- `pip install fastmcp`（自动安装官方 CLI）
- 熟悉 FastMCP Quickstart（[链接](https://gofastmcp.com/getting-started/welcome)）

### 安装与运行

```powershell
python -m venv .venv
.\.venv\Scripts\activate   # Windows PowerShell 激活
pip install -e ".[dev]"
fastmcp dev                # 读取 fastmcp.json（默认 HTTP+SSE）
fastmcp run app.py --transport stdio
fastmcp-run                # 等价于 STDIO
```

macOS / Linux:

```bash
source .venv/bin/activate
pip install -e ".[dev]"
fastmcp dev
```

### 传输配置：STDIO / HTTP / SSE

仓库自带 `fastmcp.json`，运行 `fastmcp dev` 会自动读取文件里的 `deployment.transport` 设置。默认值是 `streamable-http`（HTTP JSON + SSE 流式接口，`http://127.0.0.1:8000/`）。

在 `fastmcp.json` 中修改即可切换：

```jsonc
"deployment": {
  "transport": "streamable-http", // 可改为 stdio | http | sse
  "host": "127.0.0.1",
  "port": 8000
}
```

- `streamable-http`：HTTP + SSE（默认）
- `sse`：仅 SSE，适合 Claude Desktop 等客户端
- `http`：HTTP 轮询
- `stdio`：传统 STDIO

需要临时切换时，可使用 `fastmcp run app.py --transport sse` 等 CLI 参数覆盖。

### 模块说明

- **Tools**：`echo.py` 负责回声类工具；`city.py` 通过 `ctx.read_resource` 提供城市概要；`prompt_runner.py` 演示 `mcp.prompts.render_prompt`。
- **Resources**：定义 `cities://default` 和 `cities://{city}/profile`，展示 `@mcp.resource` 及上下文日志用法。
- **Prompts**：`operating_context` 与 `itinerary_brief` 展示如何将系统提示词存放在文件并注册为 FastMCP 模板。

### 日志

- `logging_config.py` 使用 Rich 输出彩色终端日志并写入 `logs/fastmcp.log`。
- 工具/资源借助 `Context` (`ctx.info/debug/error`) 将运行信息同步至 MCP 客户端。

### 扩展步骤

1. 新增模块并在对应 `register_*` 函数中调用即可。
2. 按需更新 `ProjectConfig` 元数据或 `fastmcp.json`（传输、端口等）。
3. 重新运行 `fastmcp dev` / `fastmcp run` / `fastmcp-run`，让 MCP 客户端加载最新功能。