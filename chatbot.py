
import json
with open("intents.json") as file:
    data = json.load(file)

import nltk
from keras.models import Sequential
#nltk.download('punkt')
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

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
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])
    
        if intent["tag"] not in labels:
            labels.append(intent["tag"])
    
    
    words = [stemmer.stem(w.lower()) for w in words if w != "?"]    
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
    
    # with open("data.pickle", "wb") as f:
    #     pickle.dump((words, labels, training, output), f)
    
try:
    model.load("model.tflearn")
except:
    model = Sequential()
    model.add(layers.Dense(10, activation='relu'))
    model.add(layers.Dense(10, activation='relu'))
    #model.add(layers.Dense(10, activation='relu'))
    model.add(layers.Dense(len(output[0]), activation='sigmoid'))
    
    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])
    model.fit(array(training), array(output), batch_size=8, epochs = 1000,verbose = 0)
    # model.save("model.tflearn")

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

        inp = user_input
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
        if tag is not "greeting" and tag is not "goodbye" and len(inp.split()) == 0:
            return "Please elaborate your sentence."
            
        print("tag = ",tag," prediction = ",max_)
        print("reponse",random.choice(responses))
        return random.choice(responses)+ " p=" + str(max_)

    
#if __name__ == '__main__':
 #   app.run(debug=True, port = 5050)
