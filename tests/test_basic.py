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

    def test_create_receiver(self):
        ''' test stub the creation of a receiver object '''
        self.rcv = utils.Receiver('224.0.0.1', '2345')
        self.assertIsInstance(self.rcv, utils.Receiver)
        self.rcv.rsock.close()

    def test_create_sender(self):
        '''' test stub for creation of sender object '''
        self.sndr = utils.Sender('192.168.1.1', '1234')
        self.assertIsInstance(self.sndr, utils.Sender)
        self.sndr.ssock.close()

if __name__ == '__main__':
    unittest.main()
