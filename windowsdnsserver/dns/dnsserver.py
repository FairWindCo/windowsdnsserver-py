import json
import logging
import platform
from typing import List

from windowsdnsserver.command_runner.powershell_runner import PowerShellCommand, PowerShellRunner
from windowsdnsserver.command_runner.runner import Command, CommandRunner
from .base import DNSService
from .record import RecordType, Record
from ..util import dns_server_utils


class DnsServerModule(DNSService):
    """
        Wrapper of Windows-DnsServer powershell module

        https://docs.microsoft.com/en-us/powershell/module/dnsserver/?view=win10-ps
    """

    def __init__(self, runner: CommandRunner = None, logger=None, server=None):
        super().__init__()

        assert platform.system() == 'Windows', "DnsServerModule can run only on a Windows Server"
        if server:
            self.server = server
        else:
            self.server = platform.node()

        if logger is None:
            self.logger = logger.create_logger("DnsServer")
        else:
            self.logger = logger

        self.runner = runner
        if runner is None:
            self.runner = PowerShellRunner(logger=logger)

    def get_dns_records(self, zone: str, name: str = None, record_type: RecordType = None) -> List[Record]:
        """ uses Get-DnsServerResourceRecord cmdlet to get records in a zone """

        args = {
            'ZoneName': zone,
            'Computer': self.server
        }

        if name:
            args['Name'] = name
        if record_type:
            args['RRType'] = record_type.value

        command = PowerShellCommand('Get-DnsServerResourceRecord', **args)
        result = self.run(command)
        if result.success:
            json_result = json.loads(result.out)
            return dns_server_utils.transform_dns_server_result(zone, json_result)
        else:
            return []

    def add_a_record(self, zone: str, name: str, ip: str, ttl: str = None) -> bool:
        """ uses Add-DnsServerResourceRecordA cmdlet to add a resource in a zone """
        args = {
            'ZoneName': zone,
            'Name': name,
            'IPv4Address': ip,
            'Computer': self.server,
        }

        if ttl:
            args['TimeToLive'] = dns_server_utils.format_ttl(ttl)

        command = PowerShellCommand(
            'Add-DnsServerResourceRecordA',
            'AllowUpdateAny',
            to_json_convert=False,
            *args
        )

        result = self.run(command)
        return result.success

    def remove_a_record(self, zone: str, name: str) -> bool:
        """ uses Remove-DnsServerResourceRecord cmdlet to remove a record in a zone """

        args = {
            'ZoneName': zone,
            'RRType': 'A',
            'Computer': self.server,
        }
        if name:
            args['Name'] = name

        flags = ['Force']

        command = PowerShellCommand('Remove-DnsServerResourceRecord', *flags, to_json_convert=False, **args)
        result = self.run(command)

        return result.success

    def add_cname_record(self, zone: str, alias_name: str, server_name: str, ttl: str = None) -> bool:
        """ uses Add-DnsServerResourceRecordA cmdlet to add a resource in a zone """
        args = {
            'ZoneName': zone,
            'Name': alias_name,
            'HostNameAlias': f'"{server_name}"',
            'Computer': self.server,
        }
        if ttl:
            args['TimeToLive'] = dns_server_utils.format_ttl(ttl)

        command = PowerShellCommand(
            'Add-DnsServerResourceRecordCName',
            # 'AllowUpdateAny',
            to_json_convert=False,
            **args
        )

        result = self.run(command)
        if not result.success:
            logging.error(result.out)
            logging.error(result.err)
        return result.success

    def remove_cname_record(self, zone: str, alias_name: str) -> bool:
        """ uses Remove-DnsServerResourceRecord cmdlet to remove a record in a zone """

        args = {
            'ZoneName': zone,
            'RRType': 'CNAME',
            'Computer': self.server,
        }
        if alias_name:
            args['Name'] = alias_name

        flags = ['Force']

        command = PowerShellCommand('Remove-DnsServerResourceRecord', *flags, to_json_convert=False, **args)
        result = self.run(command)

        return result.success

    # ---

    def add_txt_record(self, zone: str, name: str, content, ttl: str = '1h') -> bool:
        """ uses Add-DnsServerResourceRecord cmdlet to add txt resource in a zone """

        command = PowerShellCommand(
            'Add-DnsServerResourceRecord',
            'AllowUpdateAny',
            'Txt',
            to_json_convert=False,
            ZoneName=zone,
            Name=name,
            DescriptiveText=content,
            TimeToLive=dns_server_utils.format_ttl(ttl)
        )

        result = self.run(command)

        return result.success

    def remove_txt_record(self, zone: str, name: str, record_data: str = None) -> bool:
        """ uses Remove-DnsServerResourceRecord cmdlet to remove txt record in a zone """

        args = {
            'ZoneName': zone,
            'RRType': 'Txt',
            'Computer': self.server,
        }
        if name:
            args['Name'] = name

        if record_data:
            args['RecordData'] = '"%s"' % record_data

        flags = ['Force']

        command = PowerShellCommand('Remove-DnsServerResourceRecord', *flags, **args)
        result = self.run(command)

        return result.success

    # --

    def is_dns_server_module_installed(self):
        command = PowerShellCommand('Get-Module DNSServer', 'ListAvailable')
        result = self.run(command)

        return result.success and len(result.out) > 0

    def run(self, command: Command):
        result = self.runner.run(command)

        if not result.success:
            self.logger.error("Command failed [%s]" % command.build())

        return result
