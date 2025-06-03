"""
MCP Server for SEO tools focusing on robots.txt and sitemap analysis.

This server provides tools to extract sitemap URLs from robots.txt files
using advertools library.
"""

from fastmcp import FastMCP
import advertools as adv
import pandas as pd
import sys
from typing import List, Optional, Dict, Any

# Create an MCP server
mcp = FastMCP("SEO Tools")

@mcp.tool()
def get_sitemap_url_from_robots_txt(robots_txt_url: str) -> Optional[str]:
    """
    Extract the first sitemap URL from a robots.txt file URL.
    
    Args:
        robots_txt_url: The URL of the robots.txt file (e.g., 'https://example.com/robots.txt')
        
    Returns:
        The first sitemap URL found in the robots.txt file, or None if no sitemap is specified
    """
    try:
        robots_df = adv.robotstxt_to_df(robots_txt_url)
        
        # Check for errors
        if 'errors' in robots_df.columns and not pd.isna(robots_df['errors'].iloc[0]):
            print(f"Error fetching robots.txt: {robots_df['errors'].iloc[0]}", file=sys.stderr)
            return None
            
        # Extract sitemap rows directly from the dataframe - case insensitive match
        # Some robots.txt files use 'Sitemap', others use 'sitemap' - advertools preserves case
        sitemap_rows = robots_df[robots_df['directive'].str.lower() == 'sitemap']
        if not sitemap_rows.empty:
            return sitemap_rows['content'].iloc[0]
            
        # No sitemaps found
        return None
    except Exception as e:
        print(f"Error fetching/parsing robots.txt: {e}", file=sys.stderr)
        return None

@mcp.tool()
def get_all_sitemap_urls_from_robots_txt(robots_txt_url: str) -> List[str]:
    """
    Extract all sitemap URLs from a robots.txt file URL.
    
    Args:
        robots_txt_url: The URL of the robots.txt file (e.g., 'https://example.com/robots.txt')
        
    Returns:
        A list of all sitemap URLs found in the robots.txt file
    """
    try:
        robots_df = adv.robotstxt_to_df(robots_txt_url)
        
        # Check for errors
        if 'errors' in robots_df.columns and not pd.isna(robots_df['errors'].iloc[0]):
            print(f"Error fetching robots.txt: {robots_df['errors'].iloc[0]}", file=sys.stderr)
            return []
            
        # Extract sitemap rows directly from the dataframe - case insensitive match
        sitemap_rows = robots_df[robots_df['directive'].str.lower() == 'sitemap']
        if not sitemap_rows.empty:
            return sitemap_rows['content'].tolist()
            
        # No sitemaps found
        return []
    except Exception as e:
        print(f"Error fetching/parsing robots.txt: {e}", file=sys.stderr)
        return []

@mcp.tool()
def get_sitemap_content(sitemap_url: str) -> List[Dict[str, Any]]:
    """
    Fetches and parses a sitemap URL, returning its content as a list of dictionaries.

    Args:
        sitemap_url: The URL of the sitemap (e.g., 'https://example.com/sitemap.xml').

    Returns:
        A list of dictionaries representing the sitemap content, or an empty list if
        the sitemap is empty, an error occurs, or the sitemap contains errors.
    """
    try:
        sitemap_df = adv.sitemap_to_df(sitemap_url)

        if sitemap_df.empty:
            print(f"Sitemap at {sitemap_url} is empty.", file=sys.stderr)
            return []

        # Check for errors column and if it has actual error messages
        if 'errors' in sitemap_df.columns and sitemap_df['errors'].notna().any():
            print(f"Errors found in sitemap {sitemap_url}:", file=sys.stderr)
            for error in sitemap_df['errors'][sitemap_df['errors'].notna()]:
                print(f"- {error}", file=sys.stderr)
            return []

        return sitemap_df.to_dict(orient='records')
    except Exception as e:
        print(f"Error processing sitemap {sitemap_url}: {e}", file=sys.stderr)
        return []

@mcp.tool()
def analyze_urls(urls: List[str]) -> List[Dict[str, Any]]:
    """
    Parses a list of URLs and extracts components from them.

    Args:
        urls: A list of URLs to analyze (e.g., ['https://example.com/path?query=1', 'http://another.org/different_path']).

    Returns:
        A list of dictionaries, where each dictionary contains the parsed components of a URL.
        Returns an empty list if an error occurs or if the input list is empty.
    """
    if not urls:
        return []
    try:
        url_df = adv.url_to_df(urls)

        if url_df.empty:
            print("URL analysis resulted in an empty DataFrame.", file=sys.stderr)
            return []

        # advertools url_to_df does not typically add an 'errors' column in the same way sitemap_to_df does.
        # It might raise exceptions for fundamentally malformed URLs or return NaNs for parts it cannot parse.
        # We rely on the try-except block for major errors and return the df as is, assuming partial data is acceptable.

        return url_df.to_dict(orient='records')
    except Exception as e:
        print(f"Error analyzing URLs: {e}", file=sys.stderr)
        return []

@mcp.tool()
def discover_sitemap_locations(base_url: str) -> List[str]:
    """
    Generates a list of potential sitemap locations for a given base URL.

    This function constructs common sitemap URLs based on a predefined list of
    suffixes (e.g., /sitemap.xml, /sitemap_index.xml).
    These are potential locations and should be verified (e.g., by trying to fetch them).
    It no longer uses an advertools function for this specific task.

    Args:
        base_url: The base URL of the website (e.g., 'https://example.com').
                  Should be a non-empty string.

    Returns:
        A list of potential sitemap URLs. Returns an empty list if the input
        is invalid.
    """
    if not base_url or not isinstance(base_url, str):
        print("Error: base_url must be a non-empty string.", file=sys.stderr)
        return []

    # Normalize base_url by removing any trailing slash
    normalized_base_url = base_url.rstrip('/')

    sitemap_suffixes = [
        "/sitemap.xml",
        "/sitemap.xml.gz",
        "/sitemap_index.xml",
        "/sitemap-index.xml",
        "/sitemap_index.xml.gz",
        # "/sitemap-index.xml.gz", # Duplicate, removing one
        "/sitemap.php",
        "/sitemap1.xml",
        "/sitemap.txt",
        "/post-sitemap.xml",
        "/page-sitemap.xml",
        "/category-sitemap.xml",
        "/news-sitemap.xml",
        "/video-sitemap.xml",
        # Some other common patterns often found
        "/sitemap/",
        "/sitemaps.xml", # Plural
        "/sitemapindex.xml", # No underscore/hyphen
        "/sitemap/index.xml",
        "/sitemap/sitemap.xml",
        "/gss/sitemap.xml", # Google Site Search (less common now)
        "/feeds/posts/default?sitemap", # Blogger/Blogspot pattern
        "/atom.xml?redirect=false&start-index=1&max-results=500", # Older Blogger
        "/robots.txt" # Not a sitemap, but people sometimes check it via this type of tool
    ]

    potential_sitemap_urls = []
    for suffix in sitemap_suffixes:
        potential_sitemap_urls.append(normalized_base_url + suffix)

    return potential_sitemap_urls

# If running directly, this will start the server in development mode
if __name__ == "__main__":
    mcp.run()
