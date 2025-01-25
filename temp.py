from openai import OpenAI
from flask import Flask, request, jsonify

# Flask Application
app = Flask(__name__)

# OpenAI Client
client = OpenAI()

# message variable set to default first message
messages = [ {"role": "system", "content": 
    "You are a intelligent assistant."} ]

# This funtion describes the ChatGPT chat
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if user_message:
        messages.append(
            {"role": "user", "content": message},
            )
        response = client.chat.completions.create(
            model="gpt-4o-mini", messages=messages, 
            temperature=0, stream=True
            )
        full_response = ""
        for chunk in response:
            content = chunk.choices[0].delta.content
            if content is None:
                break
            full_response += content
            print(chunk.choices[0].delta.content, end="")
        return jsonify({"response": full_response})
    return jsonify({"response": "No message received"})
if __name__ == '__main__':
    app.run(debug=True)