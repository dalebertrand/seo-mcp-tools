"""
Test script for the SEO Tools MCP server.
This script uses advertools to fetch real robots.txt files and tests our parsing functions.
"""

import sys
import os
import pandas as pd
import advertools as adv

# Add the parent directory to sys.path to allow importing mcp_server
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the functions from mcp_server
from mcp_server import (
    get_sitemap_url_from_robots_txt,
    get_all_sitemap_urls_from_robots_txt
)

# Sample test websites
TEST_WEBSITES = [
    "https://www.google.com",
    "https://www.amazon.com",
    "https://www.github.com",
    "https://www.wikipedia.org"
]

def fetch_robots_txt(website_url):
    """Fetch the robots.txt file from a website using advertools"""
    print(f"\nFetching robots.txt from {website_url}...")
    
    try:
        robots_url = f"{website_url}/robots.txt"
        robots_df = adv.robotstxt_to_df(robots_url)
        
        if 'errors' in robots_df.columns and not pd.isna(robots_df['errors'].iloc[0]):
            print(f"Error fetching robots.txt: {robots_df['errors'].iloc[0]}")
            return None
            
        # Extract raw content for our parser
        import requests
        response = requests.get(robots_url, timeout=5)
        if response.status_code != 200:
            print(f"Error: HTTP {response.status_code} when fetching {robots_url}")
            return None
            
        robots_content = response.text
        print(f"Successfully fetched robots.txt ({len(robots_content)} bytes)")
        return robots_content
        
    except Exception as e:
        print(f"Exception when fetching robots.txt: {e}")
        return None

def test_with_real_websites():
    """Test our robots.txt parser with real websites"""
    for website in TEST_WEBSITES:
        robots_content = fetch_robots_txt(website)
        if not robots_content:
            continue
            
        print(f"\n--- Testing MCP tools with {website} robots.txt ---")
        
        # Test get_sitemap_url_from_robots_txt
        first_sitemap = get_sitemap_url_from_robots_txt(robots_content)
        print(f"First sitemap URL: {first_sitemap}")
        
        # Test get_all_sitemap_urls_from_robots_txt
        all_sitemaps = get_all_sitemap_urls_from_robots_txt(robots_content)
        print(f"All sitemap URLs ({len(all_sitemaps)}):")
        for sitemap in all_sitemaps:
            print(f"  - {sitemap}")
        
        # Test analyze_robots_txt removed

def test_with_sample_content():
    """Test with a known sample robots.txt content"""
    print("\n--- Testing with sample robots.txt content ---")
    
    # We can't directly test with a sample content string since our tools now expect URLs
    # Let's test with real website robots.txt files instead
    print("Using real websites for testing instead of sample content...")
    
    # Let's test with WordPress.org which has confirmed sitemap entries
    test_url = "https://wordpress.org/robots.txt"
    print(f"Testing with {test_url}")
    
    first_sitemap = get_sitemap_url_from_robots_txt(test_url)
    print(f"First sitemap URL: {first_sitemap}")
    
    all_sitemaps = get_all_sitemap_urls_from_robots_txt(test_url)
    print(f"All sitemap URLs count: {len(all_sitemaps)}")
    
    # analyze_robots_txt test removed
        
    # Assert tests for the real website
    assert first_sitemap is not None, "First sitemap URL extraction failed"
    assert len(all_sitemaps) > 0, "No sitemaps found"
    
    print("All sample tests passed!")

if __name__ == "__main__":
    print("Starting tests for the SEO Tools MCP server robots.txt parser...")
    
    # Run the sample test first
    test_with_sample_content()
    
    # Then test with real websites
    test_with_real_websites()
    
    print("\nAll tests completed!")
