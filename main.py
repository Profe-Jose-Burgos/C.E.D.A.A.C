from flask import Flask, render_template, request
import nltk, json, pickle
import numpy as np
import random
from intents_reference import start_intents
from model_builder import start_model
from nltk.stem import SnowballStemmer
from tensorflow.keras.models import load_model
stemmer=SnowballStemmer

model=load_model("chatbot_model.h5")#cargamos el modelo
intents=json.loads(open("intents.json").read())#cargamos el json
words=pickle.load(open("words.pkl","rb"))#cargamos la biblioteca de palabras
classes=pickle.load(open("classes.pkl","rb"))#cargamos la biblioteca de las clases

def clean_up_sentence(sentence):# con esto tokenizamos y lematizamos
    sentence_words=nltk.word_tokenize(sentence)#primero se tokeniza
    sentence_words=[stemmer.stem(word.lower()) for word in sentence_words]#aqui se lematiza
    return sentence_words


def bow(sentence,words,show_details=True):
    sentence_words=clean_up_sentence(sentence)

    bag=[0]*len(words) #bag == bolsa de valores
    for i in sentence_words:
        for j,w in enumerate(words):
            if w==i: #asigna 1 si la palabra en la posicion del vocabulario
                bag[j]=1
                if show_details:
                    print("Está en la bolsa 👍",w)
    return (np.array(bag))


def predict_class(sentence, model): #aqui se toma la palabra y el modelo para decidir que clase es
    #                                es decir clasifica el mensaje del usuario para saber como responder.
    p=bow(sentence, words,show_details=False)

    res=model.predict(np.array([p]))[0]
    #con "res" lo que hacemos es predecir la eficacia


    ERROR_THRESHOLD=0.25 #Umbral de error 

    results=[[i,r] for i,r in enumerate(res) if r > ERROR_THRESHOLD] 
    # hacemos que ennumere solamente el resultado que sea mayor al 25%

    results.sort(key=lambda x: x[1], reverse=True)
    #en results.sort --- Lo sorteamos en longitudes, es decir de mayor a menor

    return_list=[]
    for r in results:   
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})   
    print("print de return list: ", return_list)  ##  me dice de que tipo es y cual es la probabilidad de que sea correcto
    return return_list 
def get_response(ints,intents_json):
    tag= ints[0]["intent"]
    list_of_intents=intents_json["intents"]
    for i in list_of_intents:
        if (i["tag"]==tag):
            result=random.choice(i["responses"])
            break
        return result

app=Flask(__name__, instance_relative_config=True)
app.debug=False
@app.route('/chatbot',methods=['POST'])
def chatbot_response():
    message=request.json["message"]
    print("Mensaje del usuario: "+message)
    ints=predict_class(message,model)
    response=get_response(ints,intents)
    print("Esta es la respuesta del bot: "+response)
    return response


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':

    #start_intents()
    #start_model()
    app.run()
    