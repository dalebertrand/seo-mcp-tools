# SEO MCP Tools

A Model Context Protocol (MCP) server that provides SEO tools for analyzing robots.txt files. This server implements a set of specialized tools that help extract and analyze sitemap information from robots.txt files across the web.

## Features

The SEO MCP Tools server provides two primary tools:

1. **Get First Sitemap URL**: Extract the first sitemap URL from a robots.txt file.
2. **Get All Sitemap URLs**: Extract all sitemap URLs from a robots.txt file.

## Requirements

- Python 3.8+
- FastMCP
- advertools
- requests
- pandas

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/seo-mcp-tools.git
   cd seo-mcp-tools
   ```

2. Install the required dependencies:
   ```bash
   pip install fastmcp advertools requests pandas
   ```

## Usage

### Running the Server

Start the MCP server with:

```bash
python mcp_server.py
```

Alternatively, use the FastMCP development tools for an interactive testing environment:

```bash
fastmcp dev mcp_server.py
```

### MCP Tool Calls

#### Get First Sitemap URL

```python
from mcp_client import MCP_Client  # Assuming you're using an MCP client

client = MCP_Client("http://localhost:8000")

# Extract the first sitemap URL from a robots.txt file
first_sitemap = client.call("get_sitemap_url_from_robots_txt", {
    "robots_txt_url": "https://example.com/robots.txt"
})
print(f"First sitemap URL: {first_sitemap}")
```

#### Get All Sitemap URLs

```python
# Extract all sitemap URLs from a robots.txt file
all_sitemaps = client.call("get_all_sitemap_urls_from_robots_txt", {
    "robots_txt_url": "https://example.com/robots.txt"
})
print(f"All sitemap URLs: {all_sitemaps}")
```

## Claude Desktop Integration

1. Create a minimal MCP configuration file:
   ```json
   {
     "version": "v1",
     "endpoints": [{
       "name": "SEO Tools",
       "transport": {
         "type": "stdio",
         "command": {
           "path": "python",
           "args": ["/path/to/mcp_server.py"]
         }
       },
       "input_format": "json",
       "output_format": "json"
     }]
   }
   ```

2. Install in Claude Desktop:
   ```bash
   fastmcp install mcp_server.py
   ```

For development/testing mode, use: `fastmcp dev mcp_server.py`

## Testing

Run the tests to verify server functionality:

```bash
pytests
```

The test suite includes validation against real websites' robots.txt files to ensure the tools work correctly with various robots.txt structures.

## How It Works

The server uses direct HTTP requests to fetch robots.txt files from URLs, then applies regular expression patterns to extract relevant directives. This approach ensures reliable parsing of robots.txt files from various websites, regardless of formatting differences.

## License

MIT
