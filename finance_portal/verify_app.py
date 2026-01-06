import unittest
import os
import shutil
import tempfile
from unittest.mock import patch, MagicMock
import sys

# Ensure we can import finance_app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import finance_app

class FinanceAppTestCase(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()
        self.log_file = os.path.join(self.test_dir, 'app.log')
        self.status_file = os.path.join(self.test_dir, 'status.txt')
        self.token_file = os.path.join(self.test_dir, 'token')

        # Create dummy status and token files
        with open(self.status_file, 'w') as f:
            f.write("System OK")
        with open(self.token_file, 'w') as f:
            f.write("fake-token")

        # Patch the paths in the app module
        self.patcher1 = patch('finance_app.LOG_FILE_PATH', self.log_file)
        self.patcher2 = patch('finance_app.STATUS_FILE_PATH', self.status_file)
        self.patcher3 = patch('finance_app.K8S_TOKEN_PATH', self.token_file)
        
        self.patcher1.start()
        self.patcher2.start()
        self.patcher3.start()

        finance_app.app.testing = True
        self.client = finance_app.app.test_client()

    def tearDown(self):
        self.patcher1.stop()
        self.patcher2.stop()
        self.patcher3.stop()
        shutil.rmtree(self.test_dir)

    def test_welcome(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to Finance Portal', response.data)

    def test_health(self):
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"status": "UP"})

    def test_write_and_read(self):
        # Test Write
        response_write = self.client.get('/write')
        self.assertEqual(response_write.status_code, 200)
        self.assertIn(b'Appended', response_write.data)
        
        # Verify file exists and has content
        self.assertTrue(os.path.exists(self.log_file))
        
        # Test Read
        response_read = self.client.get('/read')
        self.assertEqual(response_read.status_code, 200)
        self.assertNotEqual(response_read.data, b'Log file empty or does not exist.')

    @patch('requests.get')
    def test_whoami_success(self, mock_get):
        # Mock the K8s API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "items": [{}, {}, {}] # 3 fake pods
        }
        mock_get.return_value = mock_response

        response = self.client.get('/whoami')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Pod count in namespace 'dubeyhari76-dev': 3", response.data)
        
        # Verify header usage
        args, kwargs = mock_get.call_args
        self.assertEqual(kwargs['headers']['Authorization'], 'Bearer fake-token')

    def test_whoami_no_token(self):
        # Unpatch temporarily to test missing token logic if we were testing that path,
        # but here we mocked the path to a file that EXISTS. 
        # So we test what happens if file is gone:
        os.remove(self.token_file)
        response = self.client.get('/whoami')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
