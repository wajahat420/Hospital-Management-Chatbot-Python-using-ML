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
confirm_words = ["ok","done","yes","confirm"]
confirm = False
recent_doctor = ""
doctors = {
    "psychiatrist" : {
    "timings" : "Mon-Fri 2pm-4pm",
    "appointments" : [],
    },
    "neurologist" : {
    "timings" : "4pm-8pm",
    "appointments" : [],
    },
    "general physician" : {
    "timings" : "4pm-9pm",
    "appointments" : [],
    }
}


with open("intents.json") as file:
    data = json.load(file)


try:    
    with open("data.pickle", "rb") as f:
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
    json_file = open('model.json', 'r')
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
    bag = array([bag_of_words(user_input, words)])
    check_bag = len(list(set(bag[0])))
    results = model.predict(bag)
    results_index = numpy.argmax(results)
    tag = labels[results_index]
    max_ = max(results[0])

    inp = [i.lower() for i in user_input.split()]
    append_tag = False

    for i in inp:
        if i in words:
            append_tag = True
    if append_tag or max_ >50:
        tags_history.append(tag)

    for tg in data["intents"]:
        if tg['tag'] == tag:
            responses = tg['responses']

    print("\ntag = ",tag," prediction = ",max_)
    print("tags_history",tags_history)
    global confirm
    global recent_doctor

    split_for_name = user_input.split(":")
    string = " "
    join_string =  string.join(split_for_name[1:]).strip().lower()
    if len(tags_history) < 1:
        pass
    elif tags_history[len(tags_history) - 1] == "doctor_appointment_asking":
        for key,value in doctors.items():
            if key in user_input:
                recent_doctor = key
                tags_history.append("doctor_appointment_asking")
                return "Ok Sir, Tell me Your name i this manner. </br> name : wajahat"

        if "name" in user_input and len(split_for_name) >= 2 and join_string not in  doctors[recent_doctor]["appointments"] :
            doctors[recent_doctor]["appointments"].append(join_string)
            return "Your Appointment is confirmed"
        elif "name" in user_input and len(split_for_name) >= 2 and join_string in  doctors[recent_doctor]["appointments"] :
            return "You have already taken an appointmnt"
        # print("join_string",join_string)


    if tag == "doctor_appointment_reject":  # reject appointment if there exist otherwise print msg that that apoointment not exist
        return "Specify your name please in this manner </br> name : Anas"
    elif "name" in user_input and len(split_for_name) >= 2  and tags_history[len(tags_history) - 1] == "doctor_appointment_reject": # rejects an ppointment or show msg 
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
    print("doctors",doctors)

    if max_ * 100 < 50:
        return( "i am unable to answer it, Please ask something else" + str(max_))

    elif tag == "asking_doctor_and_timings":
        if "general" in inp or "physician" in inp:
            return("General phyhician Timings :  {}".format(doctors["general physician"]["timings"]))
        elif "neurologist" in inp:
            return("Neurologist Timings {}".format(doctors["neurologist"]["timings"]))
        elif "psychiatrist" in inp:
            return("psychiatrist timings {}".format(doctors["psychiatrist"]["timings"]))
    
    return(random.choice(responses)+ " p=" + str(max_))


#if __name__ == '__main__':
 #   app.run(debug=True, port = 5050)
