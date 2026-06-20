# Weather MCP Server for Claude

This repository implements a Model Context Protocol (MCP) server for Claude. It exposes weather-related tools via `FastMCP` over `stdio`, using the National Weather Service (NWS) API for data.

## Project Structure

```text
weather/
├── clients/
│   ├── __init__.py
│   └── nws_client.py
├── formatters/
│   ├── __init__.py
│   └── alert_formatter.py
├── services/
│   ├── __init__.py
│   └── weather_service.py
├── tools/
│   ├── __init__.py
│   └── weather_tools.py
├── models/
│   ├── __init__.py
│   └── responses.py
├── config.py
├── logging_config.py
├── main.py
├── pyproject.toml
└── README.md
```

## Features

- MCP server for Claude using `FastMCP`
- `get_alerts(state)` tool for active weather alerts
- `get_forecast(latitude, longitude)` tool for forecast data
- Simple, maintainable service and client separation

## Requirements

- Python 3.10 or higher
- `uv` installed and available at the full path used by Claude
- `mcp` and `httpx` dependencies installed in the Python environment

## Running the Server Locally

From the repository root:

```bash
cd /Users/dinukakasun/Documents/MCP/weather
/Users/dinukakasun/.local/bin/uv --directory /Users/dinukakasun/Documents/MCP/weather run main.py
```

or using the virtual environment Python if preferred:

```bash
/Users/dinukakasun/Documents/MCP/weather/.venv/bin/python main.py
```

The server should start and expose MCP tools on `stdio`.

## Claude Desktop MCP Configuration

Update `~/Library/Application Support/Claude/claude_desktop_config.json` so Claude launches this server with the correct executable path and working directory.

Example configuration:

```json
{
  "mcpServers": {
    "weather": {
      "command": "/Users/dinukakasun/.local/bin/uv",
      "args": [
        "--directory",
        "/Users/dinukakasun/Documents/MCP/weather",
        "run",
        "main.py"
      ]
    }
  }
}
```

### Why absolute paths matter

Claude desktop may not inherit your interactive shell `PATH`. Using the absolute `uv` path avoids startup failures caused by missing commands.

## Example Claude Questions

Use these example prompts to exercise the MCP server:

- `Get the current weather alerts for CA using get_alerts.`
- `Call get_forecast with latitude 37.7749 and longitude -122.4194.`
- `What are active alerts for NY?`
- `Provide a 5-period weather forecast for 40.7128, -74.0060.`

## Local Test Client

You can verify the MCP tools locally with a small Python client that starts the server and sends a request over stdio.

```python
import asyncio
import json
import subprocess

async def run_request():
    proc = await asyncio.create_subprocess_exec(
        "/Users/dinukakasun/.local/bin/uv",
        "--directory",
        "/Users/dinukakasun/Documents/MCP/weather",
        "run",
        "main.py",
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "local-test", "version": "1.0.0"}
        }
    }

    stdout, stderr = await proc.communicate((json.dumps(request) + "\n").encode())
    print(stdout.decode())
    print(stderr.decode())

asyncio.run(run_request())
```

This confirms the server accepts MCP requests. For tool-specific tests, replace `method` with a valid tool name and pass `params` matching the tool signature.

## Verifying the MCP Server

1. Start the server manually.
2. Confirm the process is running:

```bash
ps aux | grep "main.py" | grep -v grep
```

3. Confirm Claude is configured to use the same command and working directory.
4. If Claude still does not connect, use the absolute `uv` path in `claude_desktop_config.json`.

## Notes

- The MCP server uses `stdio` transport, not a network HTTP endpoint.
- The entrypoint is `main.py`, not `weather.py`.
- The tools are registered in `tools/weather_tools.py`.

## Reference

- Model Context Protocol Python server docs: https://modelcontextprotocol.io/docs/develop/build-server#python