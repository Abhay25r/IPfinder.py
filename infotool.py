#!/usr/bin/env python3
import sys
import os
import json

# Automatically add the src directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src') if os.path.exists(os.path.join(current_dir, 'src')) else os.path.join(os.path.dirname(current_dir), 'src')
sys.path.insert(0, os.path.dirname(src_dir))bin/env python3
import sys
import os
import json

# Add the parent directory to the Python path so we can import the IPFinder package
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import directly from the file since we've added the parent directory to sys.path
from src.ipfinder import IPFinder, IPFinderError, InvalidDomainError

def main():
    if len(sys.argv) != 2:
        print("Error: Please provide a website URL")
        print("Usage: python infotool.py <website_url>")
        sys.exit(1)

    website_url = sys.argv[1]
    
    # Initialize IPFinder (you can set IPFINDER_API_KEY environment variable for authenticated requests)
    api_key = os.environ.get('IPFINDER_API_KEY')
    
    if not api_key:
        print("\nNote: No API key found in IPFINDER_API_KEY environment variable.")
        print("For accurate results, get a free API key from https://ipinfo.io/signup")
        print("Then run: export IPFINDER_API_KEY=your_api_key\n")
    
    finder = IPFinder(api_key)
    
    try:
        info = finder.get_domain_info(website_url)
        
        # Print the results in a nice format
        print("\n=== Domain Information ===")
        print(f"Domain: {info['domain']}")
        print(f"IP Address: {info['ips'][0]}")  # We show the first IP since we're using socket.gethostbyname
        
        if info['location']:
            loc = info['location']
            print("\n=== Location Information ===")
            print(f"City: {loc['city']}")
            print(f"Region: {loc['region']}")
            print(f"Country: {loc['country']}")
            print(f"Coordinates: {loc['latitude']}, {loc['longitude']}")
            print(f"ISP: {loc['isp']}")
            print(f"Timezone: {loc['timezone']}")
            
    except (InvalidDomainError, IPFinderError) as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
