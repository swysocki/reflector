""" Basic reflector tests

"""
import unittest
import unittest.mock
import os
import sys
import io
sys.path.insert(0, os.path.abspath('..'))
from reflector import utils 


class TestReflectorUtils(unittest.TestCase):
    def setUp(self):
        self.ip_addr = '192.168.101.99'

    @unittest.mock.patch.object(os, 'popen', autospec=True)
    def test_get_ip_addr(self, mock_popen):
        ''' test output is string '''
        mock_popen.return_value = io.StringIO(self.ip_addr)
        output_ip = utils.get_ip_addr()
        self.assertIsInstance(output_ip, str)
        self.assertEqual(output_ip, self.ip_addr)

if __name__ == '__main__':
    unittest.main()
