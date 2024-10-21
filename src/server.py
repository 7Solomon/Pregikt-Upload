from flask import Flask, request, jsonify
from src.upload.youtube import get_last_livestream_data

app = Flask(__name__)

# Route for handling POST requests
@app.route('/post', methods=['POST'])
def handle_post():
    data = request.get_json()  # Get JSON data from the request
    response = {
        "message": "Data received",
        "received_data": data
    }
    return jsonify(response), 200  # Return a JSON response with HTTP status code 200


# Youtube data
@app.route('/get_latest_streams_data', methods=['GET'])
def handle_get():
    latest = get_last_livestream_data()
    return jsonify({"data": latest}), 200#

# Youtube data
