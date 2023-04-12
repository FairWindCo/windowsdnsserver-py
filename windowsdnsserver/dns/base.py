from typing import List

from windowsdnsserver.dns.record import Record, RecordType
from windowsdnsserver.exception.exception_common import MethodNotImplementedError


class DNSService(object):

    def __init__(self):
        pass

    def get_dns_records(self, zone: str, name: str, record_type: RecordType) -> List[Record]:
        raise MethodNotImplementedError()

    def add_a_record(self, zone: str, name: str, ip: str, ttl: str) -> bool:
        raise MethodNotImplementedError()

    def remove_a_record(self, zone: str, name: str) -> bool:
        raise MethodNotImplementedError()

    def add_cname_record(self, zone: str, alias_name: str, server_name: str, ttl: str) -> bool:
        raise MethodNotImplementedError()

    def remove_cname_record(self, zone: str, alias_name: str) -> bool:
        raise MethodNotImplementedError()


    def add_txt_record(self, zone: str, name: str, content, ttl: str) -> bool:
        raise MethodNotImplementedError()

    def remove_txt_record(self, zone: str, name: str, record_data: str) -> bool:
        raise MethodNotImplementedError()
