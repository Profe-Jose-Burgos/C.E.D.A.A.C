from flask import Flask, render_template,request
import nltk, json,pickle
import numpy as np
import random
from intents_reference import start_intents
from model_builder import start_model
from nltk.stem import SnowballStemmer
from tensorflow.keras.models import load_model
import time
stemmer = SnowballStemmer('spanish')


model=load_model("chatbot_model.h5")#Cargamos el modelo
intents= json.loads(open("intents.json").read())#Cargamos el json | "base de datos"
words=pickle.load(open("words.pkl","rb"))#cargamos la biblioteca de las palabras
classes=pickle.load(open("classes.pkl","rb"))#cargamos la biblioteca de las clases
global date_time
global time_time
time_time=(time.strftime("%I:%M:%S"))#hora
date_time=(time.strftime("%d/%m/%y"))#fecha

def clean_up_sentence(sentence):
    
    sentence_words=nltk.word_tokenize(sentence) #tokenizamos las palabras
    sentence_words=[stemmer.stem(word.lower()) for word in sentence_words] #lematizamos las palabras
    return sentence_words


def bow (sentence,words,show_details=True): 
    sentence_words=clean_up_sentence(sentence)
    
    bag=[0]*len(words)
    
    for i in sentence_words:
        for j,w in enumerate(words):
            if w==i: #Asigna 1 si la palabra esta en la posicion de las palabras
                bag[j]=1
                if show_details:
                    print("encontrado en la bolsa: ",w)
    return (np.array(bag))



def predict_class(sentence,model):#Para predecir que tipo o clase de palabra es
    
    p = bow(sentence,words,show_details=False)
    
    res = model.predict(np.array([p]))[0] #retornamos lo eficiente del modelo
    
    
    ERROR_THRESHOLD=0.25 #Umbral de error
    
    
   
    results= [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD] 
    #si el umbral de error es mayor a r entonces lo toma
    
    
    
    
    
    results.sort(key=lambda x: x[1], reverse=True)  #Ordena el resultado de menor a mayor el resultado
    #                                                de las clases.
    global return_list #return list la hacemos global
    return_list = []    
    for r in results:   
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})   
    print("print de return list: ", return_list) #Imprime los datos del mensaje diciendome la clase y la probabilidad
    return return_list 


def get_response(ints,intents_json): #revisa la clase del "tag" y obtiene una respuesta aleatoria
    tag= ints[0]["intent"] 
    list_of_intents=intents_json["intents"] #sacamos el json las referencias para generar las respuestas
    for i  in list_of_intents: #i toma el valor de las referencias del json
        if (i["tag"]==tag): #Si i en la posicion de las clases es igual a la clase que ingreso el usuario
            result= random.choice(i["responses"]) #toma una respuesta aleatoria dentro de la propia clase de "i"
            break
    return result


app= Flask(__name__, instance_relative_config=True)# declaramos la app de flask
app.debug=False# para que se guarden los cambios al segundo | en este caso lo tenemos en False
@app.route('/chatbot',methods=['POST','GET'])#la ruta que se encarga de recibir el mensaje de la pagina web
def chatbot_response():
    try:
        message=request.json["message"]#obtiene el mensaje del formulario en la pagina web
        print("Este es el mensaje"+message)#impresion del mensaje del usuario
        ints=predict_class(message,model)#toma el mensaje y el modelo y predice en que clase está
        response=get_response(ints,intents)#va a la funcion get_response para obtener la respuesta
        print(response)
        txt = open ('log.txt','a',encoding='utf-8')#abrimos el txt
        txt.write("\nFecha:{}, Hora:{}".format(date_time,time_time))
        txt.write("\nmensaje del usuario: {}\n".format(message))
        txt.write("presicion: {}\n".format(return_list))
        txt.write("Respuesta del bot: {}\n".format(response))
        txt.close()#cerramos el txt
        return response# retorna la respuesta a la pagina web para que sea impreso
    except Exception as e:
        print("Error: ", e)
        txt = open ('log.txt','a',encoding='utf-8')#abrimos el txt
        txt.write("\nFecha:{}, Hora:{}".format(date_time,time_time))
        txt.write("\nERROR\n".format(message))
        txt.write("mensaje del usuario: {}\n".format(message))
        txt.write("presicion: {}\n".format(return_list))
        txt.write("Lo siento, no pude entender tu mensaje.\n")
        txt.close()#cerramos el txt
        return "Lo siento, no pude entender tu mensaje."



@app.route('/resp',methods=['POST','GET'])
def chatbot_mensaje():
    message=request.json["message"]
    print("Este es el mensaje"+message)
    return message


@app.route('/bot')#ruta de la pagina web donde se encuentra el chatbot
def index():# esta funcion toma la pagina para hacer la conexion http
    return render_template('index.html')#retornamos la pagina web para que este en la ruta /bot

@app.route('/')#ruta principal de la pagina web donde se muestra la bienvenida.
def Welcome():
    return render_template('Welcome.html')#Retornamos la pagina web para que este en la ruta principal




    
    
if __name__=='__main__':
    #start_intents()
    #start_model()
    
    app.run()
