# SEO MCP Tools

A Model Context Protocol (MCP) server that provides SEO tools for analyzing robots.txt files. This server implements a set of specialized tools that help extract and analyze sitemap information from robots.txt files across the web.

## Features

The SEO MCP Tools server provides tools for interacting with and analyzing website SEO components like `robots.txt` and sitemaps. See the "Available Tools" section for a detailed list and descriptions.

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

## Available Tools

This server provides the following tools:

### 1. `get_sitemap_url_from_robots_txt`

*   **Description**: Extracts the first sitemap URL found in a given `robots.txt` file URL.
*   **Parameters**:
    *   `robots_txt_url: str`: The URL of the `robots.txt` file (e.g., `'https://example.com/robots.txt'`).
*   **Returns**: `Optional[str]`
    *   The first sitemap URL found, or `None` if no sitemap is specified or an error occurs.
*   **Example Return**:
    ```
    "https://example.com/sitemap.xml"
    ```
    ```
    None
    ```

### 2. `get_all_sitemap_urls_from_robots_txt`

*   **Description**: Extracts all sitemap URLs found in a given `robots.txt` file URL.
*   **Parameters**:
    *   `robots_txt_url: str`: The URL of the `robots.txt` file (e.g., `'https://example.com/robots.txt'`).
*   **Returns**: `List[str]`
    *   A list of all sitemap URLs found. Returns an empty list if no sitemaps are found or an error occurs.
*   **Example Return**:
    ```
    ["https://example.com/sitemap1.xml", "https://example.com/sitemap2.xml"]
    ```
    ```
    []
    ```

### 3. `get_sitemap_content`

*   **Description**: Fetches and parses a sitemap URL, returning its content as a list of dictionaries.
*   **Parameters**:
    *   `sitemap_url: str`: The URL of the sitemap (e.g., `'https://example.com/sitemap.xml'`).
*   **Returns**: `List[Dict[str, Any]]`
    *   A list of dictionaries representing the sitemap content. Each dictionary typically contains keys like `'loc'`, `'lastmod'`, etc. Returns an empty list if the sitemap is empty, an error occurs during fetching/parsing, or the sitemap itself reports errors.
*   **Example Return**:
    ```json
    [
      {"loc": "https://example.com/page1", "lastmod": "2023-01-01"},
      {"loc": "https://example.com/page2", "lastmod": "2023-01-02", "changefreq": "weekly"}
    ]
    ```
    ```json
    []
    ```

### 4. `analyze_urls`

*   **Description**: Parses a list of URLs and extracts their components (scheme, netloc, path, query, fragment, etc.).
*   **Parameters**:
    *   `urls: List[str]`: A list of URLs to analyze (e.g., `['https://example.com/path?query=1#frag', 'http://another.org/different_path']`).
*   **Returns**: `List[Dict[str, Any]]`
    *   A list of dictionaries, where each dictionary contains the parsed components of a URL. Returns an empty list if the input list is empty or an error occurs during parsing.
*   **Example Return**:
    ```json
    [
      {
        "url": "https://example.com/path?query=1#frag",
        "scheme": "https",
        "netloc": "example.com",
        "path": "/path",
        "query": "query=1",
        "fragment": "frag",
        "dir_1": "path",
        "last_dir": "path"
      },
      {
        "url": "http://another.org/different_path",
        "scheme": "http",
        "netloc": "another.org",
        "path": "/different_path",
        "query": "",
        "fragment": "",
        "dir_1": "different_path",
        "last_dir": "different_path"
      }
    ]
    ```
    ```json
    []
    ```

### 5. `discover_sitemap_locations`

*   **Description**: Helps find *potential* sitemap URLs for a given domain by checking against a predefined list of common sitemap path patterns.
*   **Parameters**:
    *   `base_url: str`: The base URL of the website (e.g., `"https://www.example.com"`).
*   **Returns**: `List[str]`
    *   A list of potential sitemap URLs.
*   **How and When to Use It**:
    *   This tool is useful when you don't know the exact URL of a website's sitemap.
    *   It generates these URLs based on a **predefined list of common patterns** and **does not crawl or check if these URLs actually exist or point to valid sitemaps.**
    *   The output is a list of *suggestions*.
    *   You should then take these suggested URLs and verify them, for example, by:
        *   Using the `get_sitemap_content` tool to try and parse them.
        *   Manually trying to open them in a browser.
        *   Using other SEO tools to check their validity.
    *   This tool *only suggests possible locations* and does not perform any validation or parsing of the sitemaps themselves.
*   **Example Return Value**:
    ```json
    [
      "https://www.example.com/sitemap.xml",
      "https://www.example.com/sitemap_index.xml",
      "https://www.example.com/post-sitemap.xml",
      "https://www.example.com/sitemap.txt"
    ]
    ```
    *(Note: The actual list returned will be more comprehensive based on the predefined patterns in the function.)*

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

Examples of how to call these tools using an MCP client:

#### `get_sitemap_url_from_robots_txt`

```python
from mcp_client import MCP_Client  # Assuming you're using an MCP client

client = MCP_Client("http://localhost:8000")

# Extract the first sitemap URL from a robots.txt file
first_sitemap = client.call("get_sitemap_url_from_robots_txt", {
    "robots_txt_url": "https://example.com/robots.txt"
})
print(f"First sitemap URL: {first_sitemap}")
```

#### `get_all_sitemap_urls_from_robots_txt`

```python
# Extract all sitemap URLs from a robots.txt file
all_sitemaps = client.call("get_all_sitemap_urls_from_robots_txt", {
    "robots_txt_url": "https://example.com/robots.txt"
})
print(f"All sitemap URLs: {all_sitemaps}")
```

#### `get_sitemap_content`

```python
# Fetch and parse a sitemap
sitemap_data = client.call("get_sitemap_content", {
    "sitemap_url": "https://example.com/sitemap.xml"
})
if sitemap_data:
    for item in sitemap_data:
        print(f"URL: {item.get('loc')}, Last Modified: {item.get('lastmod')}")
else:
    print("Sitemap is empty or could not be parsed.")
```

#### `analyze_urls`

```python
# Analyze a list of URLs
url_analysis_results = client.call("analyze_urls", {
    "urls": ["https://example.com/path?query=1#frag", "http://another.org/page"]
})
if url_analysis_results:
    for result in url_analysis_results:
        print(f"URL: {result.get('url')}, Domain: {result.get('netloc')}, Path: {result.get('path')}")
else:
    print("URL analysis failed or returned no data.")
```

#### `discover_sitemap_locations`

```python
# Discover potential sitemap locations for a website
try:
    potential_sitemaps = client.call("discover_sitemap_locations", { # Assuming client.call for consistency
        "base_url": "https://www.example.com"
    })
    if potential_sitemaps:
        print(f"Potential sitemap locations for https://www.example.com:")
        for url in potential_sitemaps:
            print(f"- {url}")
    else:
        print("No potential sitemap locations generated, or an error occurred (e.g., invalid base_url).")
except Exception as e:
    print(f"Error calling discover_sitemap_locations: {e}")

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
           "path": "/path/to/python",
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
