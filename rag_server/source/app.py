from flask import Flask, jsonify, request
from flask_cors import CORS
from logger_debug import logger
from orchestrator import handle_user_query

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/check')
def hello():
    logger.debug('Received GET request')
    return "Hello from the flask endpoint."

@app.route('/send-chat', methods=['POST'])
def handle_post_request():
    try:
        logger.debug('Received POST request')

        data = request.get_json()
        user_input = data.get('user_input')

        if user_input:
            logger.debug(f"Received user input: {user_input}")  # Log to console

            genai_response = handle_user_query(user_input)
            return jsonify({"message": genai_response}), 200

        else:
            return jsonify({"error": "Missing 'user_input' in JSON payload"}), 400

    except Exception as e:
        logger.error(f"Error processing request: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    logger.debug(f'** Flask Initialization: Complete **')
    app.run(host='0.0.0.0', port=5000, debug=True)