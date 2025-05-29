# IPfinder Tool

IPfinder is a Python tool that provides comprehensive information about websites, including IP addresses (both IPv4 and IPv6) and detailed geographical location data. The tool is designed with performance, reliability, and ease of use in mind.

## Features

- Retrieve both IPv4 and IPv6 addresses for any domain
- Get detailed geographical location information including:
  - Country and country code
  - Region and city
  - Exact coordinates (latitude/longitude)
  - ISP information
  - Timezone
- Smart caching system for improved performance
- Rate limiting to respect API usage limits
- Comprehensive input validation and error handling
- Support for various URL formats

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ipfinder.git
cd ipfinder
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```python
from src.ipfinder import IPFinder

# Create an instance of IPFinder
finder = IPFinder()

try:
    # Get information for a domain
    info = finder.get_domain_info('python.org')
    
    # Print domain information
    print(f"Domain: {info['domain']}")
    print(f"IP Addresses: {', '.join(info['ips'])}")
    
    # Print location information
    if info['location']:
        loc = info['location']
        print(f"Location: {loc['city']}, {loc['region']}, {loc['country']}")
        print(f"Coordinates: {loc['latitude']}, {loc['longitude']}")
        print(f"ISP: {loc['isp']}")
        print(f"Timezone: {loc['timezone']}")
except Exception as e:
    print(f"Error: {str(e)}")
```

### Advanced Usage

```python
# Create an instance with custom cache timeout (in seconds)
finder = IPFinder(cache_timeout=7200)  # 2 hours cache

# The tool handles various URL formats
urls = [
    'python.org',              # Simple domain
    'http://python.org',       # HTTP URL
    'https://python.org/docs', # HTTPS URL with path
    'python.org:443'          # Domain with port
]

for url in urls:
    info = finder.get_domain_info(url)
    # Process the information...
```

## Running Tests

To run the unit tests:

```bash
# Run all tests
python -m unittest discover tests

# Run tests with verbose output
python -m unittest tests/test_ipfinder.py -v

# Run a specific test
python -m unittest tests.test_ipfinder.TestIPFinder.test_get_domain_info_success
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.