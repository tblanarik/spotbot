from flask import Flask, request
import requests
import os

app = Flask(__name__)

@app.route('/forward', methods=['POST'])
def forward():
    content = request.get_json()
    target_url = os.getenv('TARGET_URL')  # Replace with the actual target URL
    if not target_url:
        return "Error: TARGET_URL environment variable is not set.", 500
    response = requests.post(target_url, json=content)
    return response.text, response.status_code

if __name__ == '__main__':
    app.run(port=os.getenv('DESTINATION_URL', 5000))
