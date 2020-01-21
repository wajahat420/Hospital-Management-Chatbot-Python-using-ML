from numpy import array
import pickle
import nltk
import numpy
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
import random
import json
from keras.models import Sequential
from nltk.corpus import stopwords 
from keras import layers
from keras.models import model_from_json

from functions import *

tags_history = []
appointment = ["You may take appointment from 2pm-4pm Do you want to confirm ?","You may take appointment from 2pm-4pm, confirm it please."]
available_tests = ["blood","hepatitis","hemoglobin"]
confirm_words = ["ok","done","yes","confirm"]
confirm = False
recent_doctor = ""

doctors = {
    "psychiatrist" : {
    "timings" : "Mon-Fri 2pm-4pm",
    "appointments" : [],
    },
    "neurologist" : {
    "timings" : "Wed-Fri 4pm-8pm",
    "appointments" : [],
    },
    "general physician" : {
    "timings" : "Sat and Sun     3pm-9pm",
    "appointments" : [],
    }
}


with open("intents.json") as file:
    data = json.load(file)


try:    
    with open("dataa.pickle", "rb") as f:
        words, labels, training, output = pickle.load(f)
    print("try")
        
except:  
    print("except")
    words = []
    labels = []
    docs_x = []
    docs_y = []

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            
            pattern = pattern.replace("?","")
            pattern = pattern.replace(".","")
            # stop_words = set(stopwords.words('english')) 
            wrds = nltk.word_tokenize(pattern)
            wrds  = remove_stopwords(wrds)
            # wrds = [w for w in wrds if w not in stop_words] 
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])

        if intent["tag"] not in labels:
            labels.append(intent["tag"])
    
    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = list(set(words))
    words = remove_stopwords(words)

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

    with open("data.pickle", "wb") as f:
        pickle.dump((words, labels, training, output), f)
    
try:
    print("try-2")
    # load json and create model
    json_file = open('modell.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    # load weights into new model 
    model.load_weights("model.h5")
except:
    print("except-2")
    model = Sequential()
    model.add(layers.Dense(len(training[0])))
    model.add(layers.Dense(10))
    # model.add(layers.Dense(8, activation='relu'))
    model.add(layers.Dense(len(output[0]), activation='sigmoid'))
    
    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])
    model.fit(array(training), array(output), batch_size=8, epochs = 300,verbose = 0)

    model_json = model.to_json()
    with open("model.json", "w") as json_file:
        json_file.write(model_json)
    model.save_weights("model.h5")
    print("Saved model to disk")

def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]
    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]
    for word in s_words:
      if word in words:
        bag[words.index(word)] += 1
    return numpy.array(bag)

def chat(user_input):
    user_input = user_input.replace(".","")
    user_input = user_input.replace("?","")
    user_input = user_input.replace(",","")
    bag = array([bag_of_words(user_input, words)])
    check_bag = len(list(set(bag[0])))
    results = model.predict(bag)
    results_index = numpy.argmax(results)
    tag = labels[results_index]
    max_ = max(results[0])

    user_input = user_input.lower()
    inp = user_input.split()
    
    print("\ntag = ",tag," prediction = ",max_)
    print("tags_history",tags_history)
    print("doctors",doctors)

    if tag == "name" and max_ * 100 > 70:
        tags_history.append("")

    if ( len(tags_history) >= 1):
        if tag == "name" and tags_history[len(tags_history) - 1] == "doctor_appointment_reject" and ":" not in user_input:
            return "You have given a wrong response. Please, follow the instructions."
        if tags_history[len(tags_history) - 1] == "doctor_appointment_asking" and tags_history[len(tags_history) - 2] == "doctor_appointment_asking":
            if "name" in user_input and ":" not in user_input:
                return "Please use colon(:) in your answer."
    if ((tag == "doctor_appointment_asking" or tag == "doctor_appointment_reject") or tag == "asking_doctor_and_timings"):
        tags_history.append(tag)

    for tg in data["intents"]:
        if tg['tag'] == tag:
            responses = tg['responses']


    global confirm
    global recent_doctor

    split_for_name = user_input.split(":")
    string = " "
    join_string =  string.join(split_for_name[1:]).strip().lower()
    if len(tags_history) >= 1:

        if tags_history[len(tags_history) - 1] == "doctor_appointment_asking":
            for key,value in doctors.items():
                if key in user_input:
                    recent_doctor = key
                    tags_history.append("doctor_appointment_asking")
                    return "Ok Sir, Tell me Your name in this manner. </br> name : wajahat"

            if "name" in user_input and len(split_for_name) >= 2 and join_string not in  doctors[recent_doctor]["appointments"] :
                doctors[recent_doctor]["appointments"].append(join_string)
                return "Your Appointment is confirmed, Appoinment number = 150 </br> To take another appointment follow above instructions to write name." 
            elif "name" in user_input and len(split_for_name) >= 2 and join_string in  doctors[recent_doctor]["appointments"] :
                return "You have already taken an appointmnt please use another name to book your appointment."
        
        # reject appointment or show msg    
        if "name" in user_input and len(split_for_name) >= 2 and tags_history[len(tags_history) - 1] == "doctor_appointment_reject": 
            found_name = False
            for key,value in doctors.items():
                if join_string in  value["appointments"]:
                    found_name = True
                    value["appointments"].remove(join_string)
                    for tg in data["intents"]:
                        if tg['tag'] == "doctor_appointment_reject":
                            responses = tg['responses']
                            return (random.choice(responses))
            if not found_name:
                return "Your appointment is already not in the list."
        elif tag == "doctor_appointment_reject":
            return "Specify your name please in this manner </br> name : Anas"


    # if tag == "asking_doctor_and_timings":
    if "general" in inp or "physician" in inp:
        return("General phyhician Timings :  {}".format(doctors["general physician"]["timings"]))
    elif "neurologist" in inp:
        return("Neurologist Timings {}".format(doctors["neurologist"]["timings"]))
    elif "psychiatrist" in inp:
        return("psychiatrist timings {}".format(doctors["psychiatrist"]["timings"]))

    if max_ * 100 < 60:
        return( "Please talk about the relevant topics otherwise you must check your spellings once.!")

    if tag == "asking_doctor_and_timings":
        return (random.choice(responses).format(doctors["general physician"]["timings"],doctors["neurologist"]["timings"],doctors["psychiatrist"]["timings"]))
    return(random.choice(responses))

