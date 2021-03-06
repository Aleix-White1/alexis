from flask import Flask, jsonify, request, render_template
import json
import random # libreria para operar con aleatorio
import webbrowser #libreria para abrir paginas
from selenium import webdriver

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
            webbrowser.open_new("https://www.youtube.com")
            return "Abriendo Youtube..."
        elif comando == "abre Google" or comando == "abrir Google" or comando == " abre Google" or comando == " abrir Google" :
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            browser = webdriver.Chrome(options=chrome_options)
            browser.open("https://www.google.com")
            return "Abriendo Google..."
        elif comando == "abre WhatsApp" or comando == "abrir WhatsApp" or comando == " abre WhatsApp" or comando == " abrir WhatsApp":
            webbrowser.open_new_tab("https://web.whatsapp.com/")
            return "Abriendo WhatsApp..."
        elif "abre explorador de archivos" in comando or "abrir explorador de archivos" in comando :
            os.startfile("C:/Users/Aleix")
            return "Abriendo explorador de archivos"
        else: 
            return "No estoy programado para hacer esto a??n..."
    except TypeError:
        return ("Tienes un error tipografico, cuidado")

def menuComandos(comando):
    if comando == "hola" or comando ==  " hola":
        saludos = ["Hola!", "Saludos!", "Buenas...", "Hola, me alegra oirte"]
        random_saludos = random.choice(saludos)
        return random_saludos
    elif comando == "gracias":
        return "De nada :)"
    elif comando == " c??mo est??s" or comando == "c??mo est??s" or comando =="qu?? tal" or comando == " qu?? tal":
        estado = ["Estoy bien, gracias", "Podria estar mejor...", "Un poco cansado de tantas preguntas", "Muy bien!", "Listo para que me preguntes cualquier cosa"]
        random_estado = random.choice(estado)
        return random_estado
    elif "qui??n eres" in comando:
        return "Soy Alexis, un proyecto de DAW"
    elif "chiste" in comando:
        chistes = ["??C??mo se llama el campe??n de buceo japon??s? \n Tokofondo. \n ??Y el subcampe??n? \n Kasitoko.", "- ??Soldado L??pez! \n ??S??, mi capit??n! \n No lo vi ayer en la prueba de camuflaje \n ??Gracias, mi capit??n!",
        "Cari??o, creo que est??s obsesionado con el f??tbol y me haces falta. \n ????Qu?? falta?! ????Qu?? falta?! ????Si no te he tocado!!", "Van dos cieguitos por la calle pasando calor y dicen: \n Ojal?? lloviera! \n ??Ojal?? yo tambi??n",
        "Si car es carro y men es hombre entonces Carmen es un transformer...", "Soy un tipo saludable \n Ah. ??Comes sano y todo eso? \n No, la gente me saluda...", "??C??mo se despiden los qu??micos? \n ??cido un placer...",
        "??C??mo se dice escoba voladora en japon??s? \n Simekaigo Memato.", "Como maldice un pollito a otro pollito? \n ??Caldito seas!", " Mam??, mam??, el abuelo se cay?? \n ??Lo ayudaste hijo? \n No, se cay?? solo."]
        random_chistes = random.choice(chistes)
        return random_chistes
    elif "abre" in comando or "abrir" in comando:
        return abrirPaginas(comando)
    else:
        return "No estoy programado para hacer esto a??n..."


if __name__ == "__main__":
    app.run(port=8080, debug=True)
