from flask import Flask
import uuid
import os
app = Flask(__name__)

@app.route(f'/message')
def run():
    return f'Hello world'

if __name__ == "__main__":
    app.run()