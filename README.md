# Nf-core tools MCP (Unofficial)
A repo to experiment with MCP capabilities for nf-core tools functions.

## Overview

This MCP provides a suite of tools for accessing nf-core tools for pipelines and modules:
- Create a pipeline using the nf-core template
- List nf-core modules
- Create a module using the nf-core modules template
- Install existing nf-core modules into your pipeline or modules repo

For testing purposes, tools were implemented from the command line (cli) and directly from the python package (python). Two different MCP server files exist for these two implementations:
1) nf-core.test-server.cli.py
2) nf-core.test-server.python.py

## Installation

- [Claude Desktop App](https://claude.ai/download)
- [Uv](https://pypi.org/project/uv/)
- [nf-core tools](https://github.com/nf-core/tools)

### Installing with FastMCP to use in Claude Desktop

1) Create a venv with uv: 
```bash
uv venv
```

2) Activate the environment:
```bash
source .venv/bin/activate
```
3) Add required packages:
```bash
uv add "mcp[cli]" nf-core
```
4) Install the server
```bash
fastmcp install nf-core.test-server.cli.py ## CLI server
fastmcp install nf-core.test-server.python.py ## Python based server

```

### Adding server to Cursor
```bash
{
  "mcpServers": {
    "mix_server": {
      "command": "uv",
      "args": [
        "--directory",
        "[Full path to the server directory (this repo folder)]]",
        "run",
        "server.py"
      ]
    }
  }
}
```