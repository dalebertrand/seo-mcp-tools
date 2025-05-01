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

# If running directly, this will start the server in development mode
if __name__ == "__main__":
    mcp.run()
