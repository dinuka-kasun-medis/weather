#!/usr/bin/env python3
"""Simple test client for the weather MCP server."""

import asyncio
import subprocess
import json
import sys
from typing import Any


async def send_request(request: dict[str, Any]) -> dict[str, Any] | None:
    """Send a JSON-RPC request to the weather server."""
    try:
        # Start the server process
        process = await asyncio.create_subprocess_exec(
            "uv", "run", "weather.py",
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd="/Users/dinukakasun/Documents/MCP/weather"
        )
        
        # Send the request
        request_json = json.dumps(request) + "\n"
        stdout, stderr = await asyncio.wait_for(
            process.communicate(request_json.encode()),
            timeout=5.0
        )
        
        if stdout:
            response = json.loads(stdout.decode().strip().split("\n")[0])
            print("✅ Server responded successfully!")
            print(f"Response: {json.dumps(response, indent=2)}")
            return response
        else:
            print("❌ No response from server")
            if stderr:
                print(f"Error: {stderr.decode()}")
            return None
            
    except asyncio.TimeoutError:
        print("❌ Server timeout")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


async def main():
    """Test the server with a simple request."""
    # Test with a simple initialization request
    test_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "test-client",
                "version": "1.0.0"
            }
        }
    }
    
    await send_request(test_request)


if __name__ == "__main__":
    asyncio.run(main())
