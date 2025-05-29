import unittest
from unittest.mock import patch, Mock
import socket
from src.ipfinder import IPFinder, InvalidDomainError, IPFinderError

class TestIPFinder(unittest.TestCase):
    def setUp(self):
        self.api_key = "test_api_key"
        self.finder = IPFinder(self.api_key)
        self.finder_no_key = IPFinder()

    @patch('socket.gethostbyname')
    @patch('requests.get')
    def test_get_domain_info_success(self, mock_requests, mock_socket):
        # Mock socket resolution
        mock_socket.return_value = "1.2.3.4"
        
        # Mock ipinfo.io response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'ip': '1.2.3.4',
            'city': 'San Francisco',
            'region': 'California',
            'country': 'US',
            'loc': '37.7749,-122.4194',
            'org': 'Test ISP',
            'timezone': 'America/Los_Angeles'
        }
        mock_requests.return_value = mock_response

        # Test with a known domain
        result = self.finder.get_domain_info('python.org')
        
        # Verify API call was made with correct headers
        mock_requests.assert_called_once_with(
            'https://ipinfo.io/1.2.3.4/json',
            headers={'Authorization': 'Bearer test_api_key'},
            timeout=10
        )
        
        # Basic structure checks
        self.assertIsInstance(result, dict)
        self.assertIn('domain', result)
        self.assertIn('ips', result)
        self.assertIn('location', result)
        
        # Domain check
        self.assertEqual(result['domain'], 'python.org')
        
        # IP addresses check
        self.assertIsInstance(result['ips'], list)
        self.assertEqual(result['ips'], ['1.2.3.4'])
        
        # Location check
        self.assertIsInstance(result['location'], dict)
        required_location_fields = [
            'country', 'country_code', 'region', 'city',
            'latitude', 'longitude', 'isp', 'timezone'
        ]
        for field in required_location_fields:
            self.assertIn(field, result['location'])
            
        # Check specific location values
        loc = result['location']
        self.assertEqual(loc['city'], 'San Francisco')
        self.assertEqual(loc['region'], 'California')
        self.assertEqual(loc['country'], 'US')
        self.assertEqual(loc['country_code'], 'US')
        self.assertEqual(loc['latitude'], 37.7749)
        self.assertEqual(loc['longitude'], -122.4194)
        self.assertEqual(loc['isp'], 'Test ISP')
        self.assertEqual(loc['timezone'], 'America/Los_Angeles')

    def test_invalid_domain(self):
        invalid_domains = [
            ('', "URL cannot be empty"),
            ('not_a_real_domain', "Domain contains invalid characters"),
            ('test..com', "Domain cannot contain consecutive dots"),
            ('.test.com', "Domain cannot start or end with a dot"),
            ('test.com.', "Domain cannot start or end with a dot"),
            ('a' * 256, "Domain name is too long"),
            ('test@domain.com', "Domain contains invalid characters"),
        ]
        
        for domain, expected_error in invalid_domains:
            with self.subTest(domain=domain):
                with self.assertRaises(IPFinderError) as context:
                    self.finder.get_domain_info(domain)
                self.assertIn(expected_error, str(context.exception))

    def test_url_parsing(self):
        test_cases = [
            ('http://python.org', 'python.org'),
            ('https://python.org', 'python.org'),
            ('python.org', 'python.org'),
            ('https://python.org:443', 'python.org'),
            ('http://python.org/path', 'python.org'),
        ]
        
        with patch('socket.gethostbyname') as mock_socket, \
             patch('requests.get') as mock_requests:
            
            # Mock socket and API responses
            mock_socket.return_value = "1.2.3.4"
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'ip': '1.2.3.4',
                'city': 'Test City',
                'region': 'Test Region',
                'country': 'TC',
                'loc': '0,0',
                'org': 'Test ISP',
                'timezone': 'UTC'
            }
            mock_requests.return_value = mock_response
            
            for url, expected_domain in test_cases:
                with self.subTest(url=url):
                    result = self.finder.get_domain_info(url)
                    self.assertEqual(result['domain'], expected_domain)

    @patch('socket.gethostbyname')
    @patch('requests.get')
    def test_location_api_error(self, mock_requests, mock_socket):
        # Mock socket resolution
        mock_socket.return_value = "1.2.3.4"
        
        # Mock API error response
        mock_response = Mock()
        mock_response.status_code = 429
        mock_requests.return_value = mock_response
        
        with self.assertRaises(IPFinderError) as context:
            self.finder.get_domain_info('python.org')
        self.assertIn("API request failed with status code: 429", str(context.exception))

    @patch('socket.gethostbyname')
    @patch('requests.get')
    def test_no_api_key(self, mock_requests, mock_socket):
        # Mock socket resolution
        mock_socket.return_value = "1.2.3.4"
        
        # Mock successful API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'ip': '1.2.3.4',
            'city': 'Test City',
            'region': 'Test Region',
            'country': 'TC',
            'loc': '0,0',
            'org': 'Test ISP',
            'timezone': 'UTC'
        }
        mock_requests.return_value = mock_response
        
        # Test with no API key
        self.finder_no_key.get_domain_info('python.org')
        
        # Verify API call was made without authorization header
        mock_requests.assert_called_once_with(
            'https://ipinfo.io/1.2.3.4/json',
            headers={},
            timeout=10
        )

    def test_cache_behavior(self):
        with patch('socket.gethostbyname') as mock_socket, \
             patch('requests.get') as mock_requests:
            
            # Mock socket and API responses
            mock_socket.return_value = "1.2.3.4"
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'ip': '1.2.3.4',
                'city': 'Test City',
                'region': 'Test Region',
                'country': 'TC',
                'loc': '0,0',
                'org': 'Test ISP',
                'timezone': 'UTC'
            }
            mock_requests.return_value = mock_response
            
            # First call
            result1 = self.finder.get_domain_info('python.org')
            
            # Second call should use cache
            result2 = self.finder.get_domain_info('python.org')
            
            # Results should be identical
            self.assertEqual(result1, result2)
            
            # Verify that the API was only called once
            self.assertEqual(mock_requests.call_count, 1)

if __name__ == '__main__':
    unittest.main()