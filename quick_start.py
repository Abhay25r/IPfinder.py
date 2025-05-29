#!/usr/bin/env python3
"""
Quick Start Example for IPFinder
This script shows the basic usage of the IPFinder tool.
"""

from src.ipfinder import IPFinder

def lookup_domain(domain):
    """Look up information for a single domain."""
    # Create an instance of IPFinder
    finder = IPFinder()
    
    try:
        # Get domain information
        print(f"\nLooking up: {domain}")
        print("-" * 40)
        
        info = finder.get_domain_info(domain)
        
        # Print domain and IPs
        print(f"Domain: {info['domain']}")
        print("\nIP Addresses:")
        for ip in info['ips']:
            print(f"  {ip}")
        
        # Print location information
        if info['location']:
            loc = info['location']
            print("\nLocation Details:")
            print(f"  City: {loc['city']}")
            print(f"  Region: {loc['region']}")
            print(f"  Country: {loc['country']} ({loc['country_code']})")
            print(f"  Coordinates: {loc['latitude']}, {loc['longitude']}")
            print(f"  ISP: {loc['isp']}")
            print(f"  Timezone: {loc['timezone']}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    # Example: Look up a domain
    domain = input("Enter a domain to look up (e.g., google.com): ")
    lookup_domain(domain)
