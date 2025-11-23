import os
from flask import Flask, request, make_response, jsonify
import logging
import spotbot as sb
from tables import HamAlertMySqlTable
from discord_http import DiscordHttp
from hamalert_api import HamAlertAPI

# Configure logging
log_level = os.environ.get('LOG_LEVEL', 'INFO')
logging.basicConfig(
    level=getattr(logging, log_level.upper(), logging.INFO),
    format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    handlers=[logging.StreamHandler()]
)

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

'''
Fetch all configured triggers from HamAlert
'''
@app.route('/hamalert/triggers', methods=["GET"])
def get_hamalert_triggers():
    try:
        api = HamAlertAPI()
        triggers = api.get_triggers()

        if triggers is not None:
            return jsonify(triggers), 200
        else:
            return make_response("Failed to fetch triggers", 500)

    except ValueError as ve:
        logging.error(f"Configuration error: {ve}")
        return make_response("Server configuration error", 500)
    except Exception as e:
        logging.error(f"Error fetching HamAlert triggers: {e}")
        return make_response("Error", 500)

'''
Add a new trigger to HamAlert
Expected JSON body:
{
    "conditions": {"<condition_type>": "<value>"},
    "comment": "optional comment"
}
'''
@app.route('/hamalert/triggers', methods=["POST"])
def add_hamalert_trigger():
    try:
        data = request.get_json(force=True)

        if not data:
            return make_response("Invalid JSON body", 400)

        conditions = data.get('conditions')
        comment = data.get('comment', '')

        if not conditions:
            return make_response("Missing required fields: conditions", 400)

        if not isinstance(conditions, dict):
            return make_response("conditions must be a dictionary", 400)

        api = HamAlertAPI()
        result = api.add_trigger(conditions, comment)

        if result is not None:
            return jsonify(result), 200
        else:
            return make_response("Failed to add trigger", 500)

    except ValueError as ve:
        logging.error(f"Configuration error: {ve}")
        return make_response("Server configuration error", 500)
    except Exception as e:
        logging.error(f"Error adding HamAlert trigger: {e}")
        return make_response("Error", 500)

if __name__ == "__main__":
    app.run()
