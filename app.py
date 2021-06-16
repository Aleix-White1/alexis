from flask import Flask, jsonify, request, render_template
import json
import random # libreria para operar con aleatorio
import webbrowser #libreria para abrir paginas

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
    elif "abre" in comando or "abrir" in comando:
        return abrirPaginas(comando)
    else:
        return "No estoy programado para hacer esto aún..."


if __name__ == "__main__":
    app.run(port=8080, debug=True)
