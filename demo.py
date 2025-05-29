#!/usr/bin/env python3
"""
IPFinder Demo Script
This script demonstrates the main features of the IPFinder tool.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ipfinder import IPFinder
from typing import List

def print_domain_info(domain: str, finder: IPFinder) -> None:
    """Print comprehensive information about a domain."""
    try:
        print(f"\n{'='*50}")
        print(f"Looking up information for: {domain}")
        print(f"{'='*50}")
        
        info = finder.get_domain_info(domain)
        
        print(f"\nDomain: {info['domain']}")
        print(f"IP Addresses ({len(info['ips'])} found):")
        for ip in info['ips']:
            print(f"  - {ip}")
        
        if info['location']:
            loc = info['location']
            print("\nLocation Information:")
            print(f"  City: {loc['city']}")
            print(f"  Region: {loc['region']}")
            print(f"  Country: {loc['country']} ({loc['country_code']})")
            print(f"  Coordinates: {loc['latitude']}, {loc['longitude']}")
            print(f"  ISP: {loc['isp']}")
            print(f"  Timezone: {loc['timezone']}")
        else:
            print("\nLocation information not available")
            
    except Exception as e:
        print(f"\nError processing {domain}: {str(e)}")

def main():
    # Create an IPFinder instance
    finder = IPFinder()
    
    # List of domains to test
    test_domains: List[str] = [
        'python.org',              # Programming language website
        'github.com',              # Development platform
        'openai.com',             # AI company
        'wikipedia.org',          # Knowledge base
        'cloudflare.com'          # CDN provider
    ]
    
    # Process each domain
    for domain in test_domains:
        print_domain_info(domain, finder)
        print("\n" + "-"*50)  # Separator between domains

if __name__ == "__main__":
    main()
