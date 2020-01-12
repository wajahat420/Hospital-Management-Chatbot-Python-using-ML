from flask import Flask, request, render_template
app = Flask(__name__)

from chatbot import *

@app.route("/send_and_receive", methods=["POST"])
def send_answer():
    question = request.form['text']
    answer = chat(question)
    
    return answer
@app.route('/')
def home():
    print("working")
    return  render_template('chatbot.html')

    
if __name__ == '__main__':
    app.run(debug=True, port = 5050)
