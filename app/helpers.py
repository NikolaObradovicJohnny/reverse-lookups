from netaddr import *
import asyncio
import re
import socket

def get_ip_network(cidr):
    try:
        return IPNetwork(cidr)
    except:
        return None

async def reverse_lookups(pattern, ip_network):
    resolved = []
    for ip_address in ip_network:
        resolved.append(await check_matching(pattern, ip_address.reverse_dns, str(ip_address)))
        
    return resolved


async def reverse_lookups_socket(pattern, ip_network):
    resolved = []
    for ip_address in ip_network:
        try:
            ip_address_str = str(ip_address)
            hostname = socket.gethostbyaddr(ip_address_str)
            resolved.append(await check_matching(pattern, hostname[0], ip_address_str))
        except:
            pass
    return resolved

async def check_matching(pattern, hostname, ip_address):
    match_pattern = re.match(pattern, hostname)
    return {
        'hostname': hostname,
        'ip': ip_address,
        'match': not not match_pattern
    }
