
import json
with open("intents.json") as file:
    data = json.load(file)

import nltk
from keras.models import Sequential
#nltk.download('punkt')
# nltk.download('stopwords')
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
from nltk.corpus import stopwords 

import random
from numpy import array
import numpy
import pickle
from keras import layers

model = Sequential()

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
            # wrds = [w for w in wrds if w not in stop_words] 
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])

        if intent["tag"] not in labels:
            labels.append(intent["tag"])
    
    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = set(words)
    words = list(words)
    # print(words)
    # print("length == ",len(words))
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
    model.load("model.tflearn")
except:
    print("except-2")
    model = Sequential()
    model.add(layers.Dense(10, activation='relu'))
    model.add(layers.Dense(10, activation='relu'))
    # model.add(layers.Dense(8, activation='relu'))
    model.add(layers.Dense(len(output[0]), activation=''))
    
    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])
    model.fit(array(training), array(output), batch_size=8, epochs = 400,verbose = 1)
    model.save("model.tflearn")
    print("training",len(training[0]),len(words))

def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for word in s_words:
      if word in words:
        bag[words.index(word)] += 1

    # print("bag",set(bag))

    return numpy.array(bag)


def chat(user_input):

    inp = user_input
    bag = array([bag_of_words(user_input, words)])
    check_bag = len(list(set(bag[0])))

    # print("bag",bag)
    results = model.predict(bag)
    results_index = numpy.argmax(results)
    tag = labels[results_index]
    max_ = max(results[0])

    if check_bag == 1:
         return "Please Right Correctly"
    elif max_ * 100 < 30:
        return "i am unable to answer it, Please ask something else" + str(max_)
    
    for tg in data["intents"]:
        if tg['tag'] == tag:
            responses = tg['responses']
            print("inside for",responses)

    print("tag = ",tag," prediction = ",max_)
    print("responses",responses)

    if (not tag ==  "greeting-1") and (not tag ==  "greeting-2") and (not tag == "goodbye") and (len(inp.split()) == 1):
        return "Please elaborate your sentence."

    elif tag == "doctor_appointment":
        sentence_ = [w.lower() for w in inp.split()]
        # print("sentence",sentence_)
        if "appointment" not in sentence_:
            return "If you are talking about to take an appointment then please use 'Appointment' keyword in your sentence"    
        
    return random.choice(responses)+ " p=" + str(max_)

    
#if __name__ == '__main__':
 #   app.run(debug=True, port = 5050)
