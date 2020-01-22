from flask import Flask, request, render_template
app = Flask(__name__)

from chatbot import *
# import speech_recognition as sr
import pyttsx3


reports = [
    {
    "name" : "anas",
    "report-type":"blood"
    } ,
        {
    "name" : "saad",
    "report-type":"blood"
    } ,
        {
    "name" : "wajahat",
    "report-type":"blood"
    } 
]
textAns = ""


# def speechh():     
#     r = sr.Recognizer()

#     with sr.Microphone() as source:
#         # print("Speak Anything :")
#         audio = r.listen(source)
#         try:
#             text = r.recognize_google(audio)
#             return text
#         except:
#             return "Sorry could not recognize what you said"

# @app.route("/speechToText",methods = ["GET"])
# def speechToText():
#     # try :
#     print("req method",request.method)
#     question = speechh()

#     getAnswer = chat(question)

#     engine = pyttsx3.init() 
#     engine.say(str(getAnswer))
#     engine.runAndWait()

#     global textAns
#     textAns = getAnswer

#     return {"ques":question,"ans":getAnswer}
    # except:
    #     print("not working properly")
    #     return "not working properly"


@app.route("/textTospeech", methods=["POST"])
def textTospeech():
    # print("req method",request.method)
    print("textTospeech")

    question = request.form['text']

    getAnswer = chat(question)

    engine = pyttsx3.init() 
    engine.say(str(getAnswer))
    engine.runAndWait()

    # global textAns
    # textAns = getAnswer

    return getAnswer
    # engine = pyttsx3.init() 
    # engine.say(str(question))
    # engine.runAndWait()


@app.route("/speak", methods=["GET"])
def speak():
    global textAns
    print("speak")
    engine = pyttsx3.init() 
    engine.say(str(textAns))
    engine.runAndWait()
    textAns = ""
    return "hey"

@app.route("/get_report", methods=["GET"])
def confirm():
    # question = request.form['text']
    # answer = chat(question)
    return {"reports" : reports}


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
