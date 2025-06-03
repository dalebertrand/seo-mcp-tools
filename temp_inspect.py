import advertools
import sys

print('=== advertools ===')
print(dir(advertools))

print('\n=== advertools.sitemaps ===')
try:
    import advertools.sitemaps
    print(dir(advertools.sitemaps))
except ImportError as e:
    print(f"Failed to import advertools.sitemaps: {e}", file=sys.stderr)

print('\n=== advertools.robotstxt ===')
try:
    import advertools.robotstxt
    print(dir(advertools.robotstxt))
except ImportError as e:
    print(f"Failed to import advertools.robotstxt: {e}", file=sys.stderr)

print('\n=== try: from advertools import sitemap_variants ===')
try:
    from advertools import sitemap_variants
    print('Successfully imported sitemap_variants from advertools')
    print(type(sitemap_variants))
except ImportError as e:
    print(f'Failed to import sitemap_variants from advertools: {e}', file=sys.stderr)

print('\n=== try: from advertools.sitemaps import sitemap_variants ===')
try:
    from advertools.sitemaps import sitemap_variants
    print('Successfully imported sitemap_variants from advertools.sitemaps')
    print(type(sitemap_variants))
except ImportError as e:
    print(f'Failed to import sitemap_variants from advertools.sitemaps: {e}', file=sys.stderr)

print('\n=== try: from advertools.robotstxt import sitemap_variants ===')
try:
    from advertools.robotstxt import sitemap_variants
    print('Successfully imported sitemap_variants from advertools.robotstxt')
    print(type(sitemap_variants))
except ImportError as e:
    print(f'Failed to import sitemap_variants from advertools.robotstxt: {e}', file=sys.stderr)

# A common pattern for utility functions in advertools is that they are often in a utils.py
# but might be exposed at a higher level. Let's check advertools.utils explicitly if it exists
print('\n=== advertools.utils ===')
try:
    import advertools.utils
    print(dir(advertools.utils))
    if 'sitemap_variants' in dir(advertools.utils):
        print("Found sitemap_variants in advertools.utils!")
        from advertools.utils import sitemap_variants
        print(type(sitemap_variants))
except ImportError as e:
    print(f"Failed to import advertools.utils: {e}", file=sys.stderr)
