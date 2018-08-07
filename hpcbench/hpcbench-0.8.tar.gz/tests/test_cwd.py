import socket
import unittest

from hpcbench.campaign import ReportNode
from . import DriverTestCase


class CwdTest(DriverTestCase, unittest.TestCase):
    def test(self):
        host = socket.gethostname()
        path = '/tmp/hpcbench-ut/test_cwd/' + host + '/*'
        report = ReportNode(CwdTest.CAMPAIGN_PATH)
        count = 0
        for metrics in report.collect('metrics'):
            self.assertEqual(metrics[0]['measurement']['path'], path)
            count += 1
        self.assertEqual(count, 3)
