import os
from flask import Flask, request, make_response
import logging
import spotbot as sb
import tables
import discord_http
from azure.monitor.opentelemetry import configure_azure_monitor
app = Flask(__name__)
configure_azure_monitor(logger_name="spotbot")
logger = logging.getLogger("spotbot")
endpoint = os.environ.get('SECRET_ENDPOINT')

@app.route(f'/{endpoint}', methods=["POST"])
def run():
    try:
        sb.SpotBot(request, tables.HamAlertTable(), discord_http.DiscordHttp()).process()
    except Exception as _excpt:
        logger.error(f"Exception occurred: {_excpt}")
        return make_response(f"Exception occurred: {_excpt}", 500)
    else:
        return make_response("Accepted", 202)

'''
Empty endpoint used for keeping the container on and loaded
'''
@app.route('/', methods=["GET"])
def always_on():
    return make_response("OK", 200)

if __name__ == "__main__":
    app.run()