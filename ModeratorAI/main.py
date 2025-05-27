from flask import Flask, request, jsonify
from connectors.chatgpt_connector.api_calls import check_batch
from connectors.chatgpt_connector.utils import rules_dict

app = Flask(__name__)

@app.route('/check-text', methods=['POST'])
def api_check_text():
    data = request.get_json()
    
    if not data or 'text' not in data:
        return jsonify({"error": "Missing 'text' in request"}), 400
    
    result = check_batch({'id':228, 'text': data['text']}, rules_dict)
    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True)