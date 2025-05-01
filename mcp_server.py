"""
MCP Server for SEO tools focusing on robots.txt and sitemap analysis.

This server provides tools to extract sitemap URLs from robots.txt files
using advertools library.
"""

from fastmcp import FastMCP
import advertools as adv  # Keep for compatibility with original requirement
import pandas as pd
import re
import requests
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
        # Fetch robots.txt content directly using requests
        response = requests.get(robots_txt_url, timeout=10)
        
        # Check if the request was successful
        if response.status_code != 200:
            print(f"Error fetching robots.txt: HTTP status {response.status_code}")
            return None
            
        # Get the robots.txt content
        robots_txt_content = response.text
        
        # Use regex to extract sitemap URLs
        sitemap_matches = re.findall(r'(?i)^\s*sitemap:\s*(\S+)', robots_txt_content, re.MULTILINE)
        
        # Return the first sitemap URL if available
        if sitemap_matches:
            return sitemap_matches[0]
        return None
    except Exception as e:
        print(f"Error fetching/parsing robots.txt: {e}")
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
        # Fetch robots.txt content directly using requests
        response = requests.get(robots_txt_url, timeout=10)
        
        # Check if the request was successful
        if response.status_code != 200:
            print(f"Error fetching robots.txt: HTTP status {response.status_code}")
            return []
            
        # Get the robots.txt content
        robots_txt_content = response.text
        
        # Use regex to extract all sitemap URLs
        sitemap_matches = re.findall(r'(?i)^\s*sitemap:\s*(\S+)', robots_txt_content, re.MULTILINE)
        
        return sitemap_matches
    except Exception as e:
        print(f"Error fetching/parsing robots.txt: {e}")
        return []

@mcp.tool()
def analyze_robots_txt(robots_txt_url: str) -> dict:
    """
    Analyze a robots.txt file and return structured information about its directives.
    
    Args:
        robots_txt_url: The URL of the robots.txt file (e.g., 'https://example.com/robots.txt')
        
    Returns:
        A dictionary containing information about the robots.txt file:
        - user_agents: List of user agents mentioned
        - sitemaps: List of sitemap URLs
        - disallowed_paths: List of disallowed paths
        - allowed_paths: List of explicitly allowed paths
    """
    try:
        # Fetch robots.txt content directly using requests
        response = requests.get(robots_txt_url, timeout=10)
        
        # Check if the request was successful
        if response.status_code != 200:
            print(f"Error fetching robots.txt: HTTP status {response.status_code}")
            return {
                "user_agents": [],
                "sitemaps": [],
                "disallowed_paths": [],
                "allowed_paths": []
            }
            
        # Get the robots.txt content
        robots_txt_content = response.text
        
        # Extract user agents
        user_agents = re.findall(r'(?i)^\s*user-agent:\s*([^\n]+)', robots_txt_content, re.MULTILINE)
        
        # Extract sitemaps
        sitemaps = re.findall(r'(?i)^\s*sitemap:\s*(\S+)', robots_txt_content, re.MULTILINE)
        
        # Extract disallowed paths
        disallowed_paths = re.findall(r'(?i)^\s*disallow:\s*([^\n]+)', robots_txt_content, re.MULTILINE)
        
        # Extract allowed paths
        allowed_paths = re.findall(r'(?i)^\s*allow:\s*([^\n]+)', robots_txt_content, re.MULTILINE)
        
        return {
            "user_agents": user_agents,
            "sitemaps": sitemaps,
            "disallowed_paths": disallowed_paths,
            "allowed_paths": allowed_paths
        }
    except Exception as e:
        print(f"Error analyzing robots.txt: {e}")
        return {
            "user_agents": [],
            "sitemaps": [],
            "disallowed_paths": [],
            "allowed_paths": []
        }

# If running directly, this will start the server in development mode
if __name__ == "__main__":
    mcp.run()
