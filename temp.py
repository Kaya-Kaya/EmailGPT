from flask import Flask, request, jsonify
from llm import ChatGPT
from flask_cors import CORS
# Flask Application
app = Flask(__name__)
CORS(app)
ai = ChatGPT()

def format(user_msg):
    return f"""
Content:\n{user_msg['content']}\n\n
Sender:\n{user_msg['from'] if user_msg['from'] is not None else "Use a placeholder"}\n\n
Recipient:\n{user_msg['to'] if user_msg['to'] is not None else "Use a placeholder"}\n\n
Tone:\n{user_msg['style'] if user_msg['style'] is not None else "Not specified"}\n\n
Target Audience:\n{user_msg['target'] if user_msg['target'] is not None else "Not specified"}\n\n
Additional Instructions:\n{user_msg['additional'] if user_msg['additional'] is not None else "None"}
"""

# This funtion describes the ChatGPT chat
@app.route('/chat', methods=['POST'])
def chat():
    print("sometnoing")
    data = request.json
    if data:
        formatted = format(data)
        formatted += "\n\n\nPlease write a subject for this email and enclose it in <subject> and </subject>."

        response = ai.respond(formatted)
        valid = False

        while(not valid):
            print(response)
            if "<subject>" in response:
                subject = response.split("<subject>")[1]
                if "</subject>" in subject:
                    subject = subject.split("</subject>")[0]
                    valid = True
            if not valid:
                ai.message("user", "You must write a subject and enclose it in <subject> and </subject>")
                response = ai.respond(formatted)

        ai.message("user", "Please write a body for this email and enclose it in <body> and </body>.")
        response = ai.respond(formatted)
        valid = False

        while(not valid):
            print(response)
            if "<body>" in response:
                body = response.split("<body>")[1]
                if "</body>" in body:
                    body = body.split("</body>")[0]
                    valid = True
            if not valid:
                ai.message("user", "You must write the body of the email and enclose it in <body> and </body>")
                response = ai.respond(formatted) 

        return jsonify({"response": {"subject": subject, "body": body}})
    
    return jsonify({"response": "No message received"})

if __name__ == '__main__':
    app.run(debug=True)