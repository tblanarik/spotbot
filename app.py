import os
from flask import Flask, request, make_response
import logging
import spotbot as sb
import tables
import discord_http
app = Flask(__name__)
endpoint = os.environ.get('SECRET_ENDPOINT')

@app.route(f'/{endpoint}', methods=["POST"])
def run():
    try:
        sb.SpotBot(request, tables.create_table_client(), discord_http.DiscordHttp()).process()
    except Exception as _excpt:
        logging.error(f"Exception occurred: {_excpt}")
        return make_response(f"Error", 500)
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