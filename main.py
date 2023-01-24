from flask import Flask, render_template,request
import nltk, json,pickle
import numpy as np
import random
from nltk.stem import SnowballStemmer
from tensorflow.keras.models import load_model
stemmer = SnowballStemmer('spanish')


model=load_model("chatbot_model.h5")
intents= json.loads(open("intents.json").read())
words=pickle.load(open("words.pkl","rb"))
classes=pickle.load(open("classes.pkl","rb"))


def clean_up_sentence(sentence):
    
    sentence_words=nltk.word_tokenize(sentence) 
    sentence_words=[stemmer.stem(word.lower()) for word in sentence_words] 
    return sentence_words


def bow (sentence,words,show_details=True): 
    sentence_words=clean_up_sentence(sentence)
    
    bag=[0]*len(words)
    
    for i in sentence_words:
        for j,w in enumerate(words):
            if w==i:
                bag[j]=1
                if show_details:
                    print("encontrado en la bolsa: ",w)
    return (np.array(bag))



def predict_class(sentence,model):
    
    p = bow(sentence,words,show_details=False)
    
    res = model.predict(np.array([p]))[0] 
    
    
    ERROR_THRESHOLD=0.25 
    
    
   
    results= [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD] 
    
    
    
    
    
    results.sort(key=lambda x: x[1], reverse=True)  
    
    return_list = []    
    for r in results:   
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})   
    print("print de return list: ", return_list) 
    return return_list 


def get_response(ints,intents_json): 
    tag= ints[0]["intent"] 
    list_of_intents=intents_json["intents"] 
    for i  in list_of_intents: 
        if (i["tag"]==tag): 
            result= random.choice(i["responses"]) 
            break
    return result


app= Flask(__name__, instance_relative_config=True)
app.debug=False
@app.route('/chatbot',methods=['POST','GET'])
def chatbot_response():
    message=request.json["message"]
    print("Este es el mensaje"+message)
    ints=predict_class(message,model)
    response=get_response(ints,intents)
    print(response)
    return response


@app.route('/resp',methods=['POST','GET'])
def chatbot_mensaje():
    message=request.json["message"]
    print("Este es el mensaje"+message)
    return message


@app.route('/bot')
def index():
    return render_template('index.html')

@app.route('/')
def Welcome():
    return render_template('Welcome.html')

import intents_reference
import model_builder
if __name__=='__main__':
    
    app.run()
    
    