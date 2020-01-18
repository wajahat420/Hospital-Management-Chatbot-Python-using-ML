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
    return  render_template('chatbot.html')

@app.route('/doctors', methods=["GET"])
def doctors():
    return  render_template('doctors.html')

@app.route('/lab', methods=["GET"])
def lab():
    return  render_template('laboratory.html')

@app.route('/instructions', methods=["GET"])
def instructions():
    return  render_template('instructions.html')

   
    
if __name__ == '__main__':
    app.run(debug=True, port = 5050)
