from app import app
from app.helpers import get_ip_network, reverse_lookups, reverse_lookups_socket, reverse_lookups_socket_async
from flask import request, jsonify
import asyncio


loop = asyncio.get_event_loop()

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

@app.route("/reverse-lookups")
def get_reverse_lookups():
    cidr = request.args.get("cidr")
    pattern = request.args.get("search") or ""
    
    ip_network = get_ip_network(cidr)
    if ip_network is None:
        return jsonify({"error": "CIDR is not in valid format."})
    
    resolved = loop.run_until_complete(reverse_lookups(pattern, ip_network))

    response = {
        "ip_addresses": resolved,
        "totalResolved": len(resolved),
        "totalMatched": len(list(filter(lambda x: x['match'], resolved))),
        "total": len(ip_network)
    }
    return jsonify(response)

@app.route("/reverse-lookups/second")
def get_reverse_lookups_with_socket():
    cidr = request.args.get("cidr")
    pattern = request.args.get("search") or ""
    
    ip_network = get_ip_network(cidr)
    if ip_network is None:
        return jsonify({"error": "CIDR is not in valid format."})
    
    resolved = loop.run_until_complete(reverse_lookups_socket(pattern, ip_network))

    response = {
        "ip_addresses": resolved,
        "totalResolved": len(resolved),
        "totalMatched": len(list(filter(lambda x: x['match'], resolved))),
        "total": len(ip_network)
    }
    return jsonify(response)

@app.route("/reverse-lookups/async")
def get_reverse_lookups_with_socket_async():
    cidr = request.args.get("cidr")
    pattern = request.args.get("search") or ""
    
    ip_network = get_ip_network(cidr)
    if ip_network is None:
        return jsonify({"error": "CIDR is not in valid format."})
    
    resolved = reverse_lookups_socket_async(pattern, ip_network)

    response = {
        "ip_addresses": resolved,
        "totalResolved": len(resolved),
        "totalMatched": len(list(filter(lambda x: x['match'], resolved))),
        "total": len(ip_network)
    }
    return jsonify(response)
