from openai import OpenAI
from flask import Flask, request, jsonify
from flask_cors import CORS

# Flask Application
app = Flask(__name__)
CORS(app)
# OpenAI Client
client = OpenAI()

# message variable set to default first message
messages = [ {"role": "system", "content": 
    "You are a intelligent assistant."} ]

# This funtion describes the ChatGPT chat
@app.route('/chat', methods=['POST'])
def chat():
    print("chat")
    data = request.json
    content = data.get('content')
    from_who = data.get('from')
    to_who = data.get('to')
    style = data.get('style')
    target = data.get('target')
    additional = data.get('additional')
    
    if content:
        messages.append({"role": "user", "content": f"Content: {content}"})
        messages.append({"role": "user", "content": f"From: {from_who}"})
        messages.append({"role": "user", "content": f"To: {to_who}"})
        messages.append({"role": "user", "content": f"Style: {style}"})
        messages.append({"role": "user", "content": f"Target: {target}"})
        messages.append({"role": "user", "content": f"Additional: {additional}"})
        
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
    return jsonify({"response": "Incomplete message received"})
if __name__ == '__main__':
    app.run()