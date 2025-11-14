import os
from flask import Flask, request, make_response
import logging
import spotbot as sb
from tables import HamAlertMySqlTable
from discord_http import DiscordHttp

app = Flask(__name__)
endpoint = os.environ.get('SECRET_ENDPOINT')
allowed_ips_str = os.environ.get('ALLOWED_IPS', '')
allowed_ips = [ip.strip() for ip in allowed_ips_str.split(',') if ip.strip()] if allowed_ips_str else []

def is_ip_allowed(client_ip):
    """Check if the client IP is in the allowed list. If no list is configured, allow all."""
    if not allowed_ips:
        return True
    return client_ip in allowed_ips

@app.route(f'/{endpoint}', methods=["POST"])
def run():
    client_ip = request.headers.get('X-Real-IP', request.remote_addr)

    if not is_ip_allowed(client_ip):
        logging.warning(f"Access denied for IP: {client_ip}")
        return make_response("Forbidden", 403)

    try:
        sb.SpotBot(request, HamAlertMySqlTable(), DiscordHttp()).process()
    except Exception as _excpt:
        logging.error(f"Exception occurred: {_excpt}")
        return make_response(f"Error", 500)
    else:
        return make_response("Accepted", 202)

'''
Empty endpoint used for checking that site is up
'''
@app.route('/', methods=["GET"])
def always_on():
    return make_response("OK", 200)

if __name__ == "__main__":
    app.run()