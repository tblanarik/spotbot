from flask import Flask, request, make_response
import logging
import spotbot as sb
import tables
import discord_http
app = Flask(__name__)

@app.route(f'/message', methods=["POST"])
def run():
    try:
        sb.SpotBot(request, tables.HamAlertTable(), discord_http.DiscordHttp()).process()
    except Exception as _excpt:
        logging.error(f"Exception occurred: {_excpt}")
        return make_response(f"Exception occurred: {_excpt}", 500)
    else:
        return make_response("Accepted", 202)

if __name__ == "__main__":
    app.run()