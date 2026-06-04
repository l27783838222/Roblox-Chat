from flask import Flask, request, jsonify

app = Flask(__name__)

chat_history = []

@app.route('/')
def home():
    return "سيرفر شات روبلوكس شغال بنجاح على Railway! 🚀"

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    if data and 'username' in data and 'message' in data:
        full_message = f"{data['username']}: {data['message']}"
        chat_history.append(full_message)
        if len(chat_history) > 50:
            chat_history.pop(0)
        return jsonify({"status": "success"}), 200
    return jsonify({"status": "error"}), 400

@app.route('/get_chat', methods=['GET'])
def get_chat():
    return jsonify({"messages": chat_history}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
  
