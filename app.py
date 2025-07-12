import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS # Để cho phép frontend gọi API
from dotenv import load_dotenv

# Tải biến môi trường từ file .env (chứa API key)
load_dotenv()

app = Flask(__name__)
CORS(app) # Kích hoạt CORS cho ứng dụng Flask

# Cấu hình Gemini API
try:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
    print("Gemini API configured successfully.")
except Exception as e:
    print(f"Error configuring Gemini API: {e}")
    model = None

@app.route('/ask', methods=['POST'])
def ask_gemini():
    if not model:
        return jsonify({"error": "Gemini model is not configured"}), 500

    data = request.get_json()
    if not data or 'prompt' not in data:
        return jsonify({"error": "Invalid request. 'prompt' is required."}), 400

    user_prompt = data['prompt']

    try:
        response = model.generate_content(user_prompt)
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)