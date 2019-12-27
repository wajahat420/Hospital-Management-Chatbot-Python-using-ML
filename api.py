from flask import Flask, request, render_template,jsonify
app = Flask(__name__)

def do_something(text1,text2):
   print("hello")
   text1 = text1.upper()
   text2 = text2.upper()
   combine = text1 + text2
   return combine
@app.route("/send_and_receive", methods=["POST"])
def send_answer():
    question = request.form['text']
    answer = chat(question)
    
    return answer
@app.route('/')
def home():
    print("working")
    return  render_template('chatbot.html')
@app.route('/join', methods=['GET','POST'])
def my_form_post():
    print("jajajajajaja")
    text1 = request.form['text1']
    #word = request.args.get('text1')
    text2 = request.form['text2']
    combine = do_something(text1,text2)
    result = {
        "output": combine
        
    }
    print("text1",text1,"text2",text2)
    print("output",result)
    result = {str(key): value for key, value in result.items()}
    return jsonify(result=result)



data =  {"intents" :  [
                {"tag": "greeting",
                "patterns": ["Hi", "How are you", "Is anyone there?","assalam-o-alaikum","salam", "Hello", "Good day", "Whats up"],
                 "pattern2" : ["what's your name?","assalam-o-alaikum"],
                "responses": ["Hello!", "Good to see you again!", "Hi there, how can I help?"]
                },
                {"tag": "goodbye",
                "patterns": ["cya", "See you later", "Goodbye", "I am Leaving", "Have a Good day","allahafiz","allah hafiz","khuda hafiz","khudahafiz","Ok, talk to you later"],
                 "pattern2"  :["ok now i have to leave","will talk you soon","will see you later"],
                "responses": ["Sad to see you go :(", "Talk to you later", "Goodbye!"]
                },
                {"tag": "name",
                "patterns": ["what is your name", "what should I call you", "whats your name?","what is your good name"],
                 "pattern2" : ["what is your name buddy?","i want to know your name"],
                "responses": ["You can call me SAW", "I'm SAW", "I'm SAW"]
                },
                {"tag": "closing",
                "patterns": ["what is the closing timing of hospital?","at what time it will closed?"],
                 "pattern2" : ["what is the time at which the hospital is closed?","what's the closing timing of a hospital?","please tell me the off time of hospital?"],
                 "responses": ["It's open 24 hours.","It's open 24/7","It's open every time"]
                },
                {
                "tag" : "opening",
                "patterns" : ["at what time the hospital will open?","what is the opening time of hospital?","is is open 24/7?","is it open day and night?","is it open in late night?","is it open after 12?","what is the opening timing of a hospital?","when will it be open?"],
                 "responses": ["It's open 24 hours.","It's open 24/7","It's open every time"]
                },
                {"tag": "doctor_asking_timings",
                 "patterns" : ["timing for doctor?","sitting of doctor?","doctor sit in the evening?","doctor sit in the afternoon?","doctor sit in the night?","doctor sit in the morning?","when will doctor will come?","is there any doctor who sit in the timings of night?"],
                "responses": ["Doctor is available 7am-4pm Monday-Friday!"]
                },
                {"tag": "doctor_type",
                 "patterns" : ["is here any general physician sit?","psychologist?","neuro sergion?"],
                "responses": ["Yes, he is available here","Yes, he is"]
                },
                {
                "tag" : "doctor_appointment",
                "patterns" : ["i want to take an appointment.","i want to take timings.","i want to book timings","i want to reserve slot","i want to book appointment","i want to take appointment please guide","please book my slot"],
                 "responses" : ["Appointment timings are 4pm-9pm","The available timings are 4pm-9pm"]
                },
                {
                "tag" : "meet_patient",
                "patterns" : ["i want to meet","i want to meet my uncle","what is the timings for meeting patient","what is the timings for visiting patient?","what is the meeting time for the patient","when we can meet patient?","i want to meet my mother"],
                "responses" : ["You may meet from 12pm-4pm","Yes, you can meet him from 12pm-4pm"]
                },
                {
                "tag" : "patient_room",
                "patterns" : ["tell me his room?","on which floor?","left or right?","room number?","room no?","which corridor?"],
                "pattern2" : ["guide me the way to the room","where my patient is now"],
                "responses" : ["Yes you may meet him upstairs 2nd floor 3rd room to the left"]
                },
             

              ]
        }



import nltk
from keras.models import Sequential
#nltk.download('punkt')
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

import random
from numpy import array
import numpy

from keras import layers


words = []
labels = []
docs_x = []
docs_y = []

for intent in data["intents"]:
    for pattern in intent["patterns"]:
        wrds = nltk.word_tokenize(pattern)
        words.extend(wrds)
        docs_x.append(wrds)
        docs_y.append(intent["tag"])

    if intent["tag"] not in labels:
        labels.append(intent["tag"])


words = [stemmer.stem(w.lower()) for w in words if w != "?"]
#words = sorted(list(set(words)))

labels = sorted(labels)

training = []
output = []

out_empty = [0 for _ in range(len(labels))]

# for training and output
for x,doc in enumerate(docs_x):
    bag = [0 for _ in range(len(words))]
    wrds = [stemmer.stem(w.lower()) for w in doc]
    for word in wrds:
      if word in words:
        bag[words.index(word)] += 1

    training.append(bag)
    output_row = out_empty[:]
    output_row[labels.index(docs_y[x])] = 1
    output.append(output_row)




training = numpy.array(training)
output = numpy.array(output)




model = Sequential()
model.add(layers.Dense(10, activation='relu'))
model.add(layers.Dense(10, activation='relu'))
#model.add(layers.Dense(10, activation='relu'))
model.add(layers.Dense(len(output[0]), activation='sigmoid'))

model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])
model.fit(array(training), array(output), batch_size=4, epochs = 200,verbose = 0)
#loss, accuracy =  model.evaluate(x=val_training, y = val_output,  batch_size=10)
#print("accuracy",accuracy)



def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for word in s_words:
      if word in words:
        bag[words.index(word)] += 1
   # print("bag",bag)
    return numpy.array(bag)


def chat(user_input):

        results = model.predict(array([bag_of_words(user_input, words)]))
        results_index = numpy.argmax(results)
        tag = labels[results_index]
        max_ = max(results[0])
        if max_ * 100 < 50:
            return "i am unable to answer it, Please ask something else" + str(max_)
        for tg in data["intents"]:
            if tg['tag'] == tag:
                responses = tg['responses']
        #print("labels",labels)
        #print("results",results)
        print("tag = ",tag," prediction = ",max_)
        print("reponse",random.choice(responses))
        return random.choice(responses)

    
if __name__ == '__main__':
    app.run(debug=True)
