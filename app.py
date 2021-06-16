from flask import Flask, jsonify, request, render_template
import json
import pyttsx3 #para poder hablar (en principio no se va a usar )
import webbrowser #libreria para abrir o buscar paginas 
from datetime import date, timedelta, datetime #mide el tiempo
import pyowm  # tiempo por localidad 
import operator  # matematicas
import random  #oeprador aleatorio
import os  #Interactuar con el directorio del pc 
from os import remove #borrar contenido de un fichero
from os import path
from re import split #dividir arrays
import wikipedia # libreria para conectar con wikipedia
import requests #libreria que se usa para el traductor 
import turtle #dibujar
#alarma
from time import localtime
from pygame import mixer
#radio
import internetradioplayer
#librerias parteBio
from pypdb import *

app = Flask(__name__)

@app.route('/')
def Alexis():
    return render_template('Alexis.html') 

@app.route('/ComoSeUsa')
def ComoSeUsa():
    return render_template('ComoSeUsa.html') 

@app.route('/BioAlexis')
def BioAlexis():
    return render_template('BioAlexis.html') 

@app.route('/BioComoSeUsa')
def BioComoSeUsa():
    return render_template('BioComoSeUsa.html')

@app.route('/getdataBio/<Bioindex_no>', methods=['GET','POST'])
def data_getBio(Bioindex_no):
    if request.method == 'GET':
        print("Comando enviado por metodo GET ") 
        comandoBio = str(Bioindex_no)
        return parteBio(comandoBio)
    else:
        print("Comando enviado por metodo POST ")
        comandoBio = str(Bioindex_no)
        return parteBio(comandoBio)

def parteBio(comandoBio):
    if "buscar proteínas por ID" in comandoBio:
        try:
            IDs = comandoBio[24::].replace(" ", "")
            busqueda = Query(int(IDs), "PubmedIdQuery").search()
            return str(busqueda)
        except ValueError:
            return "No se reconoce el comando"
    elif "busca artículos sobre" in comandoBio:
        try:
            articulo = comandoBio[22::]
            articulo_traducido = Traductor('es', 'en', articulo)
            buscar_articulos = find_papers(articulo_traducido, max_results=10)
            return "Esto es lo que he encontrado sobre '" + articulo + "': " + str(buscar_articulos)
        except KeyError:
            return "Sobre que quieres que busque?"
    elif "busca información sobre" in comandoBio:
       return buscarInfo(comandoBio)
    elif "recuperar campo" in comandoBio:
        try:
            campo = comandoBio[16::]
            campo_traducido = Traductor('es', 'en', campo)
            proteina = IDs_final
            data = get_info(str(proteina))
            if campo_traducido == "cell":
                return data["cell"]
            elif "author" in campo_traducido:
                return str(data["audit_author"])
            elif "ID" in campo_traducido or "Id" in campo_traducido:
                return data["rcsb_id"]
            elif campo_traducido == "entry":
                return data["entry"]
            elif campo_traducido == "structure":
                return data["struct"] 
            elif campo_traducido == "software":
                return str(data["software"])
            elif campo_traducido == "symmetry":
                return str(data["symmetry"])
        except NameError:
            return "¡ERROR!, Primero tienes que buscar la proteína para poder recuperar un campo. Para eso di: 'busca información sobre..'"
    elif "buscar proteínas de" in comandoBio:
        p = comandoBio[20::]
        p_traducido = Traductor('es', 'en', p)
        busqueda = Query(str(p_traducido)).search()
        return "Proteínas encontradas de " + p + ": " + str(busqueda[:6]) + "\n(Resultado filtrado a 6 IDs)"
    else: 
        return "Aún no estoy programado para hacer esto..."


def buscarInfo(comandoBio):
    try:
        IDs = comandoBio[24::]
        IDs_sinEspacio = IDs.replace(" ", "")
        global IDs_final 
        IDs_final = IDs_sinEspacio.upper()
        webbrowser.open("https://www.rcsb.org/structure/"+ format(IDs_final))
        info = get_info(IDs_final)
        return str(info.keys())
    except AttributeError:
        return "El comando no pertenece a un nombre de una proteïna"

@app.route('/getdata/<index_no>', methods=['GET','POST'])
def data_get(index_no):

    if request.method == 'GET':
        print("Comando enviado por metodo GET ")        
        comando = str(index_no)
        return menuComandos(comando)
    else:
        print("Comando enviado por metodo POST ")
        comando = str(index_no)
        return menuComandos(comando)



def abrirPaginas(comando):
    try:
        if comando == "abre YouTube" or comando == "abrir Youtube" or comando == " abre YouTube" or comando == " abrir Youtube":
            webbrowser.open_new_tab("https://www.youtube.com")
            return "Abriendo Youtube..."
        elif comando == "abre Google" or comando == "abrir Google" or comando == " abre Google" or comando == " abrir Google" :
            webbrowser.open_new_tab("https://www.google.com")
            return "Abriendo Google..."
        elif comando == "abre WhatsApp" or comando == "abrir WhatsApp" or comando == " abre WhatsApp" or comando == " abrir WhatsApp":
            webbrowser.open_new_tab("https://web.whatsapp.com/")
            return "Abriendo WhatsApp..."
        elif "abre explorador de archivos" in comando or "abrir explorador de archivos" in comando :
            os.startfile("C:/Users/Aleix")
            return "Abriendo explorador de archivos"
        else: 
            return "No estoy programado para hacer esto aún..."
    except TypeError:
        return ("Tienes un error tipografico, cuidado")
        pass
    
def wikipediaBuscar(comando):
    try:
        if "buscar en Wikipedia" in comando or "busca en Wikipedia" in comando:
            comando_busqueda = str(comando[19::])
            wikipedia_resultado = wikipedia.summary(comando_busqueda) 
            respuesta_traducida = Traductor("en", "es", wikipedia_resultado)
            return respuesta_traducida
        else:
            return "No estoy programado para hacer esto aún..."
    except wikipedia.exceptions.PageError:
        return "¡ERROR! El comando introducido no encuentra nada en la Wikipedia"
    except wikipedia.exceptions.DisambiguationError:
        return "¡ERROR! Especifica a que te refieres..."
    except wikipedia.exceptions.WikipediaException:
        return "¡ERROR! Dime que quieres que busque..."
    except ValueError:
        return "El comando no pertenece a esta sección.."

def buscarComando(comando):
    try:
        if "buscar en Google" in comando:
            comando_busqueda = str(comando[17::])
            webbrowser.open("https://www.google.com/search?q={}".format(comando_busqueda))
            return "Buscando '" + comando_busqueda + "' en Google"
        elif "busca en Google" in comando:
            comando_busqueda = str(comando[16::])
            webbrowser.open("https://www.google.com/search?q={}".format(comando_busqueda))
            return "Buscando '" + comando_busqueda + "' en Google"
        elif "pon la canción" in comando:
            comando_busqueda = str(comando[14::])
            webbrowser.open("https://www.youtube.com/search?q={}".format(comando_busqueda))
            return "Buscando '" + comando_busqueda + "' en Youtube "
        else:
            return "No estoy programado para hacer esto aún..."
    except ValueError:
        return "El comando no pertenece a esta sección.."

def calculadora(comando):
    if "cuál es la" in comando or "Cuanto es" in comando:
        return "'Cuál es la...' o 'Cuanto es' no se reconoce como comando de una calculadora"
    elif "suma" in comando: #"suma 2 + 2 "
        nums = split("\D+", comando)# nums = ["suma", "2", "+", "2"]
        resultado = int(nums[1]) + int(nums[2])
        return comando[5::] +" = "+str(resultado)
    elif " + " in comando:
        nums = split("\D+", comando)
        resultado = int(nums[0]) + int(nums[1])
        return comando+" = "+str(resultado)
    elif "menos" in comando:
        if "resta" in comando:
            nums = split("\D+", comando)
            resultado = int(nums[1]) - int(nums[2])
            resultado_replace = str(comando[5::]).replace("menos", "-")
            return resultado_replace +" = "+str(resultado)
        nums = split("\D+", comando)
        resultado = int(nums[0]) - int(nums[1])
        replace_comando = comando.replace("menos", "-")
        return replace_comando+" = "+str(resultado)
    elif "entre" in comando:
        if "divide" in comando:
            nums = split("\D+", comando)
            resultado = int(nums[1]) / int(nums[2])
            resultado_replace = str(comando[6::]).replace("entre", "/")
            return resultado_replace +" = "+str(resultado)
        nums = split("\D+", comando)
        resultado = int(nums[0]) / int(nums[1])
        replace_comando = comando.replace("entre", "/")
        return replace_comando+" = "+str(resultado)
    elif "por" in comando:
        if "multiplica" in comando:
            nums = split("\D+", comando)
            resultado = (float(nums[1]) * float(nums[2]))
            resultado_replace = str(comando[11::]).replace("por", "x")
            return resultado_replace +" = "+str(resultado)
        nums = split("\D+", comando)
        resultado = int(nums[0]) * int(nums[1])
        replace_comando = comando.replace("por", "x")
        return replace_comando+" = "+str(resultado)
    else: 
        return "No estoy programado para hacer esto aún..."

def menuComandos(comando):
    if comando == "hola" or comando ==  " hola":
        saludos = ["Hola!", "Saludos!", "Buenas...", "Hola, me alegra oirte"]
        random_saludos = random.choice(saludos)
        return random_saludos
    elif comando == "gracias":
        return "De nada :)"
    elif comando == " cómo estás" or comando == "cómo estás" or comando =="qué tal" or comando == " qué tal":
        estado = ["Estoy bien, gracias", "Podria estar mejor...", "Un poco cansado de tantas preguntas", "Muy bien!", "Listo para que me preguntes cualquier cosa"]
        random_estado = random.choice(estado)
        return random_estado
    elif "quién eres" in comando:
        return "Soy Alexis, un proyecto de DAW"
    elif "chiste" in comando:
        chistes = ["¿Cómo se llama el campeón de buceo japonés? \n Tokofondo. \n ¿Y el subcampeón? \n Kasitoko.", "- ¡Soldado López! \n ¡Sí, mi capitán! \n No lo vi ayer en la prueba de camuflaje \n ¡Gracias, mi capitán!",
        "Cariño, creo que estás obsesionado con el fútbol y me haces falta. \n ¡¿Qué falta?! ¡¿Qué falta?! ¡¡Si no te he tocado!!", "Van dos cieguitos por la calle pasando calor y dicen: \n Ojalá lloviera! \n ¡Ojalá yo también",
        "Si car es carro y men es hombre entonces Carmen es un transformer...", "Soy un tipo saludable \n Ah. ¿Comes sano y todo eso? \n No, la gente me saluda...", "¿Cómo se despiden los químicos? \n Ácido un placer...",
        "¿Cómo se dice escoba voladora en japonés? \n Simekaigo Memato.", "Como maldice un pollito a otro pollito? \n ¡Caldito seas!", " Mamá, mamá, el abuelo se cayó \n ¿Lo ayudaste hijo? \n No, se cayó solo."]
        random_chistes = random.choice(chistes)
        return random_chistes
    elif "malo" in comando:
        return "Perdón, no soy tan bueno como tú.."
    elif "menú" in comando or "que sabes hacer" in comando or "qué haces" in comando or "qué puedes hacer" in comando:
        return "Para saber lo que puedo hacer, selecciona la pestaña superior 'Como se Usa?' "
    elif "abre" in comando or "abrir" in comando:
        return abrirPaginas(comando)
    elif "busca en Wikipedia" in comando or "buscar en Wikipedia" in comando:
        return wikipediaBuscar(comando)
    elif "busca en Google" in comando or "buscar en Google" in comando or "pon la canción" in comando: 
        return buscarComando(comando)
    elif "suma" in comando or " + " in comando or "menos" in comando or "resta" in comando or "divide" in comando or "entre" in comando or "multiplica" in comando or "por" in comando:
        return calculadora(comando) 
    elif "tiempo" in comando:
        return tiempo(comando)
    elif "traduce del español" in comando:   
        try:
            comando_cc = str(comando[20::])
            respuesta_traducida = Traductor("es", "en", comando_cc)
            return respuesta_traducida
        except KeyError as e:
            return "Que quiere que traduzca?"
    elif "traduce del inglés" in comando:
        try:
            comando_cc = str(comando[19::])
            respuesta_traducida = Traductor("en", "es", comando_cc)
            return respuesta_traducida
        except KeyError as e:
            return "Que quieres que traduzca?"
    elif "alarma" in comando:
        Historial(comando)
        nums = split("\D+", comando)
        hora = nums[1]
        minut = nums[2]
        return alarma(hora, minut)
    elif "historial" in comando:
        if path.exists("D:\DAW2\PROJECTE\MPro\serving_static\historial.txt"):
            if "borrar" in comando or "borra" in comando or "elimina" in comando or "eliminar" in comando:
                return borrarHistorial()
            else:
                return leerHistorial()
        else:
            return "El historial está vacío"
    elif "dibuja" in comando or "dibujar" in comando:
        Historial(comando)
        return dibujaEspiral()
    elif "radio" in comando:
        radio = os.system("python internetradioplayer.py")
        return "Radio apagada"
    else:
        return "No estoy programado para hacer esto aún..."


if __name__ == "__main__":
    app.run(port=8080, debug=True)
