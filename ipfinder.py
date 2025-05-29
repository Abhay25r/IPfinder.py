import sys
import socket
import requests
import json
from typing import Dict, Optional, Union, List
from urllib.parse import urlparse
from functools import lru_cache

class IPFinderError(Exception):
    """Base exception for IPFinder errors"""
    pass

class InvalidDomainError(IPFinderError):
    """Raised when the domain name is invalid"""
    pass

class IPFinder:
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize IPFinder with API key for ipinfo.io service.
        
        Args:
            api_key (str, optional): API key for ipinfo.io service
        """
        self.api_key = api_key

    def get_domain_info(self, url: str) -> Dict[str, Union[str, List[str], Dict]]:
        """
        Get comprehensive information about a domain including IP and location.
        
        Args:
            url (str): The URL or domain name to look up
            
        Returns:
            dict: Dictionary containing domain information, IP addresses and location
            
        Raises:
            InvalidDomainError: If the domain name is invalid
            IPFinderError: If there's an error getting domain information
        """
        try:
            # Clean and parse the URL
            domain = self._extract_domain(url)
            self._validate_domain(domain)
            
            # Get IP addresses using socket
            ip = socket.gethostbyname(domain)
            
            result = {
                'domain': domain,
                'ips': [ip],
                'location': self._get_location(ip)
            }
            
            return result
            
        except socket.gaierror as e:
            raise InvalidDomainError(f"Invalid domain name: {url}") from e
        except Exception as e:
            raise IPFinderError(f"Error getting domain information: {str(e)}") from e

    def _extract_domain(self, url: str) -> str:
        """Extract the domain name from a URL."""
        if not url:
            raise InvalidDomainError("URL cannot be empty")
            
        if not any(url.startswith(prefix) for prefix in ('http://', 'https://', 'ftp://')):
            url = f'http://{url}'
            
        try:
            parsed_url = urlparse(url)
            domain = parsed_url.netloc or parsed_url.path
            return domain.split(':')[0].lower()  # Remove port if present and convert to lowercase
        except Exception as e:
            raise InvalidDomainError(f"Could not parse URL: {url}") from e

    def _validate_domain(self, domain: str) -> None:
        """Validate domain name format."""
        if not domain:
            raise InvalidDomainError("Domain cannot be empty")
            
        if len(domain) > 255:
            raise InvalidDomainError("Domain name is too long")
            
        allowed_chars = set("abcdefghijklmnopqrstuvwxyz0123456789-.")
        if not all(c in allowed_chars for c in domain.lower()):
            raise InvalidDomainError("Domain contains invalid characters")
            
        if domain.startswith('.') or domain.endswith('.'):
            raise InvalidDomainError("Domain cannot start or end with a dot")
            
        if '..' in domain:
            raise InvalidDomainError("Domain cannot contain consecutive dots")

    @lru_cache(maxsize=1000)
    def _get_location(self, ip: str) -> Optional[Dict]:
        """
        Get location information for an IP address using ipinfo.io.
        
        Args:
            ip (str): IP address to look up
            
        Returns:
            dict: Dictionary containing location information or None if lookup fails
        """
        try:
            # Check if we have an API key
            if not self.api_key:
                print("Warning: No API key provided. Using ipinfo.io without an API key will result in rate limiting.")
                print("To get accurate results, sign up for a free API key at https://ipinfo.io/signup")
                
            headers = {'Authorization': f'Bearer {self.api_key}'} if self.api_key else {}
            url = f'https://ipinfo.io/{ip}/json'
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 429:  # Rate limit exceeded
                raise IPFinderError(
                    "Rate limit exceeded. Please sign up for a free API key at https://ipinfo.io/signup"
                )
            elif response.status_code != 200:
                raise IPFinderError(f"API request failed with status code: {response.status_code}")
                
            data = response.json()
            
            # Check if we're getting the requesting IP's location instead of the target IP
            if data.get('ip') != ip and not self.api_key:
                raise IPFinderError(
                    "Rate limit reached. Getting accurate location requires an API key. "
                    "Please sign up for a free API key at https://ipinfo.io/signup"
                )
                
            loc = data.get('loc', '').split(',')
            
            return {
                'country': data.get('country'),
                'country_code': data.get('country'),  # ipinfo.io provides country code in 'country'
                'region': data.get('region'),
                'city': data.get('city'),
                'latitude': float(loc[0]) if len(loc) == 2 else None,
                'longitude': float(loc[1]) if len(loc) == 2 else None,
                'isp': data.get('org'),
                'timezone': data.get('timezone')
            }
        except requests.Timeout:
            raise IPFinderError("Timeout while getting location information")
        except requests.RequestException as e:
            raise IPFinderError(f"Error getting location information: {str(e)}")
        except (KeyError, ValueError, IndexError) as e:
            raise IPFinderError(f"Invalid API response format: {str(e)}")
        except Exception as e:
            raise IPFinderError(f"Unexpected error getting location: {str(e)}")
            
        return None