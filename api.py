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
    # print("home")
    # pg = request.form['page']
    return  render_template('chatbot.html',page=True)

@app.route('/doctors', methods=["GET"])
def doctors():
    print("doctors")
    return  render_template('doctors.html')

@app.route('/lab', methods=["GET"])
def lab():
    print("lab")
    return  render_template('laboratory.html')

    
if __name__ == '__main__':
    app.run(debug=True, port = 5050)
