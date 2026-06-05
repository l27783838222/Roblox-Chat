import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# قائمة لحفظ الرسائل داخل ذاكرة السيرفر بشكل مؤقت وسريع
chat_history = []
MAX_HISTORY = 100  # حفظ آخر 100 رسالة فقط ليبقى السيرفر خفيفاً وسريعاً جداً

@app.route('/')
def home():
    return jsonify({"status": "Server is running perfectly!"})

@app.route('/send_message', methods=['POST'])
def send_message():
    try:
        data = request.get_json()
        if not data or "username" not in data or "message" not in data:
            return jsonify({"error": "Invalid data format"}), 400
        
        username = data["username"]
        message = data["message"]
        
        # تنسيق شكل الرسالة النهائي ليظهر داخل اللعبة
        formatted_message = f"[{username}]: {message}"
        chat_history.append(formatted_message)
        
        # تنظيف الذاكرة تلقائياً لمنع امتلاء الرام
        if len(chat_history) > MAX_HISTORY:
            chat_history.pop(0)
            
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_chat', methods=['GET'])
def get_chat():
    return jsonify({"messages": chat_history}), 200

if __name__ == '__main__':
    # جلب منفذ البورت الخاص بـ Railway بشكل تلقائي وصحيح
    port = int(os.environ.get("PORT", 8080))
    # تشغيل السيرفر مع تفعيل الـ Multithreading لإنهاء مشكلة التوقف تماماً!
    app.run(host='0.0.0.0', port=port, threaded=True, debug=False)
