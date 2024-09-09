from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/forward', methods=['POST'])
def forward():
    content = request.get_json()
    target_url = 'http://example.com/target'  # Replace with the actual target URL
    response = requests.post(target_url, json=content)
    return response.text, response.status_code

if __name__ == '__main__':
    app.run(port=5000)
