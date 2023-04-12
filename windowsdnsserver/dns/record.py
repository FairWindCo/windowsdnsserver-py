from enum import Enum


class RecordType(Enum):
    A = 'A'
    TXT = 'Txt'
    CNAME = 'cname'

    @staticmethod
    def list():
        return [t.value for t in RecordType]

    @staticmethod
    def value_of(value):
        return next((t for t in RecordType if t.value == value))


class Record(object):

    def __init__(self, zone: str, name: str, record_type: RecordType, content: str, ttl: str = '1h'):
        self.zone = zone
        self.name = name
        self.type = record_type
        self.content = content
        self.ttl = ttl

    def __repr__(self):
        return '[%s] record - zone: [%s], name: [%s]' % (self.type, self.zone, self.name)
