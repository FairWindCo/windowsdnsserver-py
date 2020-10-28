import unittest


from microsoftdnsserver.dns.dnsserver import DnsServerModule
from microsoftdnsserver.dns.record import RecordType


class TestDnsServer(unittest.TestCase):

    def setUp(self):
        self.dns = DnsServerModule()

        self.test_dns_zone = "myzone.com"
        self.test_dns_name = "www"

    def test_get_dns_records(self):
        success = self.dns.addARecord(self.test_dns_zone, self.test_dns_name, "100.100.100.100")
        self.assertTrue(success, "failed while adding test record")

        records = self.dns.getDNSRecords(self.test_dns_zone, self.test_dns_name, RecordType.A)
        self.assertGreater(len(records), 0)

        for record in records:
            self.assertEqual(record.type, RecordType.A)

        self.dns.removeARecord(self.test_dns_zone, self.test_dns_name)

    def test_add_record_a(self):
        ip_addr = "10.0.0.99"

        success = self.dns.addARecord(self.test_dns_zone, self.test_dns_name, ip_addr)
        self.assertTrue(success)

    def test_add_record_txt(self):
        txt = "my test record"

        success = self.dns.addTxtRecord(self.test_dns_zone, self.test_dns_name, txt)
        self.assertTrue(success)


if __name__ == '__main__':
    unittest.main()