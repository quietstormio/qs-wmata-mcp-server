# qs-wmata-mcp-server
MCP Server for WMATA (https://wmata.com) stations. Not official 

This MCP server provides a way to interface with the WMATA API with natural language.

First get an WMATA API key here: https://www.wmata.com/about/developers/
Do not share your WMATA API key

Then configure your LLM, I'm using Claude Desktop:

```
"qs-wmata-mcp-server":{
   "command":"/path/to/uv",
   "args":[
      "--directory",
      "/path/to/cloned/qs-wmata-mcp-server",
      "run",
      "wmata.py"
   ]
}
```
