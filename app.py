import os
from flask import Flask, request, make_response
import logging
import spotbot as sb
from tables import HamAlertMySqlTable
from discord_http import DiscordHttp

app = Flask(__name__)
endpoint = os.environ.get('SECRET_ENDPOINT')

@app.route(f'/{endpoint}', methods=["POST"])
def run():
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