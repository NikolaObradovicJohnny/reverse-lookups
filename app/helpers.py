from netaddr import *
import asyncio
import concurrent.futures
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

def reverse_lookups_socket_async(pattern, ip_network):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        resolved = []
        for ip_address in ip_network:
            futures.append(executor.submit(check_ip_address, ip_address=str(ip_address), pattern=pattern))
        for future in concurrent.futures.as_completed(futures):
            future_result = future.result()
            if future_result is not None:
                resolved.append(future_result)
    return resolved

def check_ip_address(ip_address, pattern):
    try:
        hostname = socket.gethostbyaddr(ip_address)
        return check_matching_async(pattern, hostname[0], ip_address)
    except:
        pass

def check_matching_async(pattern, hostname, ip_address):
    match_pattern = re.match(pattern, hostname)
    return {
        'hostname': hostname,
        'ip': ip_address,
        'match': not not match_pattern
    }
