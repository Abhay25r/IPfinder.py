#!/usr/bin/env python3
"""
Website Search Tool
Allows users to search for IP and location information of any website.
"""

from src.ipfinder import IPFinder, IPFinderError

def format_location(location):
    """Format location information in a readable way."""
    if not location:
        return "Location information not available"
    
    return f"""
    🌍 Location Details:
    🏙️  City: {location['city']}
    🏘️  Region: {location['region']}
    🗺️  Country: {location['country']} ({location['country_code']})
    📍 Coordinates: {location['latitude']}, {location['longitude']}
    🏢 ISP: {location['isp']}
    🕒 Timezone: {location['timezone']}
    """

def search_website():
    """Main function to search website information."""
    finder = IPFinder()
    
    while True:
        print("\n" + "="*60)
        print("🔍 Website IP and Location Finder")
        print("="*60)
        
        # Get user input
        website = input("\nEnter a website (e.g., google.com) or 'quit' to exit: ").strip()
        
        if website.lower() in ['quit', 'exit', 'q']:
            print("\nThank you for using the Website Finder! Goodbye! 👋\n")
            break
            
        if not website:
            print("\n❌ Error: Please enter a website address")
            continue
            
        try:
            print(f"\n🔍 Searching information for: {website}")
            print("-"*60)
            
            # Get website information
            info = finder.get_domain_info(website)
            
            # Display results
            print(f"\n🌐 Domain: {info['domain']}")
            
            # Display IP addresses
            print("\n📡 IP Addresses:")
            for ip in info['ips']:
                print(f"    ▶ {ip}")
            
            # Display location information
            print(format_location(info['location']))
            
        except IPFinderError as e:
            print(f"\n❌ Error: {str(e)}")
        except Exception as e:
            print(f"\n❌ An unexpected error occurred: {str(e)}")
        
        input("\nPress Enter to search another website...")

if __name__ == "__main__":
    try:
        search_website()
    except KeyboardInterrupt:
        print("\n\nSearch cancelled by user. Goodbye! 👋\n")
