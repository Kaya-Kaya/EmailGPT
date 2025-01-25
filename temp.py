from flask import Flask, request, jsonify
from llm import ChatGPT

# Flask Application
app = Flask(__name__)

ai = ChatGPT()

def format(user_msg):
    return f"""
Content:\n{user_msg['content']}\n\n
Sender:\n{user_msg['sender'] if user_msg['sender'] is not None else "Use a placeholder"}\n\n
Recipient:\n{user_msg['recipient'] if user_msg['recipient'] is not None else "Use a placeholder"}\n\n
Tone:\n{user_msg['tone'] if user_msg['tone'] is not None else "Not specified"}\n\n
Target Audience:\n{user_msg['target_audience'] if user_msg['target_audience'] is not None else "Not specified"}\n\n
Additional Instructions:\n{user_msg['additional_instructions'] if user_msg['additional_instructions'] is not None else "None"}
"""

# This funtion describes the ChatGPT chat
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if user_message:
        formatted = format(user_message)
        formatted += "\n\n\nPlease write a subject for this email and enclose it in <subject> and </subject>."

        response = ai.respond(formatted)
        valid = False

        while(not valid):
            if "<subject>" in response:
                subject = response.split("<subject>")[1]
                if "</subject>" in subject:
                    subject = subject.split("</subject>")[0]
                    valid = True
            if not valid:
                ai.message("You must write a subject and enclose it in <subject> and </subject>")
                response = ai.respond(formatted)

        ai.message("Please write a body for this email and enclose it in <body> and </body>.")
        response = ai.respond(formatted)
        valid = False

        while(not valid):
            if "<body>" in response:
                body = response.split("<body>")[1]
                if "</body>" in body:
                    body = body.split("</body>")[0]
                    valid = True
            if not valid:
                ai.message("You must write the body of the email and enclose it in <body> and </body>")
                response = ai.respond(formatted) 

        return jsonify({"response": {"subject": subject, "body": body}})
    
    return jsonify({"response": "No message received"})

if __name__ == '__main__':
    app.run(debug=True)