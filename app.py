from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os

# API Key must be a string
GOOGLE_API_KEY = "AIzaSyD2NTjy6U39uo8LcT1eZoRGh0xYAVWTK8g"
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')
chat = model.start_chat(history=[])

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat_response():
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    try:
        ai_response = chat.send_message(user_input).text
   
        if '\n' in ai_response:
            lines = ai_response.split('\n')
            html_response = "<ul>"
            for line in lines:
               if line.strip():
                  if ':' in line:
                     heading, detail = line.split(':', 1)
                     html_response += f"<li><b>{heading.strip()}:</b>{detail.strip()}</li>"
                  else:
                     html_response += f"<li>{line.strip()}</li>"
            html_response += "</ul>"
        else:
         html_response = ai_response

        return jsonify({"response": html_response})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

