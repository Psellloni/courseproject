from flask import Flask, request, jsonify
from connectors.chatgpt_connector.api_calls import check_batch
from connectors.chatgpt_connector.utils import rules_dict

app = Flask(__name__)

@app.route('/check-text', methods=['POST'])
def api_check_text():
    data = request.get_json()
    
    if not data or 'text' not in data:
        return jsonify({"error": "Missing 'text' in request"}), 400
    
    for i in list(rules_dict.keys()):
        if not data['rules'][i]:
            del rules_dict[i]
    
    result = check_batch({'id':data['id'], 'text': data['text']}, data['rules'])
    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True)