##################################################################################################
#                         Código del servidor de Lumière 
#  Hecho por: Sandra Susana Pérez Gutiérrez, Brandon Silva Barrera, Troncoso Moreno Javier Adan
#             y	García Barriga Marco Antonio
#                Materia: Sistemas Embebidos
##################################################################################################
# Generalidades:
# Este código nos sirve para manejar de manera óptima los eventos y métodos de una aplicación web.
# Para ello se usó flask, el cual es una librería de python que hace el trabajo de un servidor web
# como xampp, etc. Se hizo así para poder tener más olgura al implementarlo, pues si diseñamos una 
# aplicación perse, corremos el riesgo de que no sea compatible con el sistema operativo; en cambio,
# si las funcionales son cubiertas como servicios web, pueden ser despachados desde el servidor y
# de tal manera que hacemos uso de la web para ejecutar el centro y en consecuencia cualquier cliente 
# que haga sus peticiones, podrá tener cobertura de las mismas sin probema de la arquitectura.
##################################################################################################


##################################################################################################
#Librerías usadas
##################################################################################################

from flask import Flask, render_template,send_file,request,url_for  #servidor, carga html, envía documentos y carga imagenes desde carpeta static
import datetime														#sirve para enviar mensajes de la fecha y saber cuándo fue la úlrima actualización o petición que recibió el servidor
import cv2                            								#sirve para la función de tomar fotos con la webcam
import pywhatkit as rep   											#sirve para abrir youtube
import numpy as np                                                  #nos ayuda con los filtros de la cámara al tomar fotitus
import os   														#sirve para guardar archivos y abrir directorios  														#
import shutil                                                       #ayuda a operar archivos
from spotipy.oauth2 import SpotifyClientCredentials                 #funciones para reproducir spotify 
import spotipy														#funciones para reproducir spotify 
from selenium import webdriver										#funciones que nos ayudan a automatizar procesos, en este caso para abrir netflix y buscar en google
import time                                                         #ayuda a parar al bot
import webbrowser as web                                            #ayuda a abrir páginas web                                       #ayuda a conectarnos a internet
import usb_access																		
import subprocess

##################################################################################################
# credenciales de cliente spotify 
##################################################################################################

client_id='452f261bc9294074a5e903e660097890'
client_secret = '08a43171753b48fc97c5725d435a7ab4'

server = Flask(__name__) #instanciamos un objeto tipo flask

##################################################################################################
#  Funciones
##################################################################################################

def is_empty(dato):  #verifica si hay contenido existente en lo que retona (nos sirve para verificar si el vaor tomado de la página web por método get contiene rubro y si no se envía un mensaje 
	                 #donde dice que repita el llenado del formulario)
    if dato:
        return False
    else:
        return True

def createNewConnection(SSID, password):    #conecta a web haciendo uso de la biblioteca wireless, los valores que se operan son los obtenidos por el formulario y metodo get
	wireless = Wireless()
	wireless.connect(ssid=str(SSID), password=str(password))  #
	return "conectado"
 


def html(content):  # nos ayuda a traducir un mensaje del servidor a html rederizando la página con el formato que ya estamos manejando :)
   return '<!doctype html><html><head><link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous"><title>{% block title %}{% endblock %}</title></head><body style="background-color:#e19cd3;"><nav class="navbar navbar-expand-lg navbar-light bg-light"><a class="navbar-brand" href="#">Lumière</a><button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation"><span class="navbar-toggler-icon"></span></button><div class="collapse navbar-collapse" id="navbarNav"><ul class="navbar-nav"><li class="nav-item active"><a class="nav-link" href="/">Home <span class="sr-only">(current)</span></a></li><li class="nav-item"><a class="nav-link" href="'+chr(92)+'red">Red</a></li><li class="nav-item"><a class="nav-link" href="'+chr(92)+'funcionalidades">Funcionalidades</a></li><li class="nav-item"><a class="nav-link" href="'+chr(92)+'tutorial">Tutorial</a></li><li class="nav-item"><a class="nav-link" href="'+chr(92)+'recom">Recomendaciones</a></li></ul></div></nav> <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script> <center>' + content + '</center></body></html>'

######################################################################################################
#  Rutas del servido nos ayudan a manejar eventos como botones, rederizar páginas, cargar documentos
#  y manejar peticiones al servidor, ya sea para operaciones de automatización, reproducción de música
# ,ect. Todo lo que po
######################################################################################################
# Renderización de htmls
######################################################################################################
@server.route('/') #nuestro "main" de html, redneriza el index que a su vez da formato de flask y llama a renderizar el base.html. DE tal manera que el index nos funciona como plantilla del contenido de la página
def home():
   today = datetime.datetime.now()
   print("Bienvenido al servidor. Fecha actual: "+str(today))
   return render_template('index.html')

@server.route('/tutorial')  #renderiza página de tutorial
def tuto():
   today = datetime.datetime.now()
   print("Bienvenido al servidor. Fecha actual: "+str(today))
   return render_template('tutorial.html')

@server.route('/usb')  #renderiza página de usb
def usb():
   today = datetime.datetime.now()
   print("Bienvenido al servidor. Fecha actual: "+str(today))
   return render_template('usb.html')

@server.route('/recom')    #renderiza página de recomendaciones
def recom():
   today = datetime.datetime.now()
   print("Bienvenido al servidor. Fecha actual: "+str(today))
   return render_template('recomendaciones.html')

@server.route('/you')      #renderiza página para buscar en youtube donde tiene el formulario para solicitar los datos
def you():
   today = datetime.datetime.now()
   print("Bienvenido al servidor. Fecha actual: "+str(today))
   return render_template('youtube.html')

@server.route('/spoti')   #rederiza página de spotify donde tiene el formulario para solicitar los datos
def spoti():
   today = datetime.datetime.now()
   print("Bienvenido al servidor. Fecha actual: "+str(today))
   return render_template('spotify.html')

@server.route('/red')     #rederiza página de red donde tiene el formulario para solicitar los datos
def red():
   today = datetime.datetime.now()
   print("Bienvenido al servidor. Fecha actual: "+str(today))
   
   return render_template('red.html')

@server.route('/camara')   #rederiza página para tomar foto
def camara():
	return render_template('camara.html')

@server.route('/libros_desc') #rederiza página para abrir libros digitales
def libros_desc():
	return render_template('libros.html')

@server.route('/netflix')    #rederiza página para abrir formulario para netflix
def netflix():
	return render_template('netflix.html')

@server.route('/google')	 #rederiza página para abrir formulario para google
def google():
   today = datetime.datetime.now()
   print("Bienvenido al servidor. Fecha actual: "+str(today))
   return render_template('google.html')


@server.route('/funcionalidades')    #rederiza página para abrir menu con funcionalidades
def funcionali():
   today = datetime.datetime.now()
   print("Bienvenido al servidor. Fecha actual: "+str(today))
   return render_template('funcionalidades.html')


######################################################################################################
# abre desde los archivos del servidor en la carpeta static y envía el doc al cliente
######################################################################################################

@server.route('/yo_robot')
def yo_robot():
	return send_file('static/libros/Yo, robot - Isaac Asimov.pdf') #es una función de flask que nos permite enviar documentos desde el servidor hasta el cliente

@server.route('/quijote')
def quijote():
	return send_file('static/libros/donquijote.pdf')

@server.route('/diablo')
def diablo():
	return send_file('static/libros/El diablo de los numeros - Hans Magnus Enzensberger.pdf')

@server.route('/miserables')
def miserables():
	return send_file('static/libros/Víctor Hugo - Los miserables.pdf')

@server.route('/lenguas')
def lenguas():
	return send_file('static/libros/1 Veinte mil leguas de viaje submarino autor Julio Verne.pdf')

@server.route('/viaje')
def viaje():
	return send_file('static/libros/2 Viaje al centro de la Tierra autor Julio Verne.pdf')

@server.route('/luna')
def luna():
	return send_file('static/libros/5 De la Tierra a la Luna autor Julio Verne.pdf')

@server.route('/fe')
def fe():
	return send_file('static/libros/Fe y Razón.pdf')

@server.route('/antro')
def antro():
	return send_file('static/libros/Antropologia-Teologica-Juan-Luis-Lorda.pdf')

@server.route('/pneu')
def pneu():
	return send_file('static/libros/Pneumatología.pdf')

@server.route('/pneum')
def pneum():
	return send_file('static/libros/pneu.pdf')

@server.route('/bibli')
def bibli():
	return send_file('static/libros/Teología Bíblica.pdf')

@server.route('/sein')
def sein():
	return send_file('static/libros/sein_und_zeit.pdf')

@server.route('/ser')
def ser():
	return send_file('static/libros/ser y nada.pdf')

@server.route('/critica')
def critica():
	return send_file('static/libros/critica.pdf')

@server.route('/bana')
def bana():
	return send_file('static/libros/eichmann.pdf')

######################################################################################################
# Funcionalidades que son ejecutadas por el servidor y entrega un resultado en html. Hace uso del 
# método get para recibir datos del formulario
######################################################################################################

@server.route('/usb_access')      #método que permite inicializar la interfaz para abrir archivos de la usb
def usb_access():
	nombre = request.args.get('nom') 
	try:
		print(["python3", "prueba.py", nombre])
		result = subprocess.run(["python3", "prueba.py", nombre])    #ejecuta el código que llama a las funciones que manejan la memoria usb
		output="Conexión a la memoria USB"
		return render_template('funcionalidades.html')
	except Exception as e:
		print(e)
		output="Ocurrió una falla al tratar de conectarse a la memoria USB, intente nuevamente por favor. "+ "/media/sandra/"+nombre+"/ "
		return html('<div class="message"><p> '+output+' </p><i class="message-close-btn">&times;</i></div>')


@server.route('/busc_youtube',methods=['GET'])   # método get recibimos los valores
def busc_youtube():
	video = request.args.get('nom')   # se cachan en variables del request con tal nombre
	if(is_empty(video)):
		output="No se llenó el rubro solicitado. Favor de introducir la información solicitada."
		return html('<div class="message"><p> '+output+' </p><i class="message-close-btn">&times;</i></div>')
	rep.playonyt(video)                         # reproduce video de youtube siguiendo la funcionalidad de la biblioteca pywhatkit
	output="El video " +video +" está siendo reproducido."
	return html('<div class="message"><p> '+output+' </p><i class="message-close-btn">&times;</i></div>')

@server.route('/busc_spotify',methods=['GET'])   # método get recibimos los valores
def busc_spotify():
	cancion = request.args.get('nom')     # se cachan en variables del request con tal nombre
	if(is_empty(cancion)):
		output="No se llenó el rubro solicitado. Favor de introducir la información solicitada."
		return html('<div class="message"><p> '+output+' </p><i class="message-close-btn">&times;</i></div>')
	sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id,client_secret))
	result = sp.search(cancion)
	for i in range(0, len(result["tracks"]["items"])):
          web.open(result["tracks"]["items"][i]["external_urls"]["spotify"])
	output="Se abrieron las mejores coincidencias con la canción " +cancion +" en spotify."
	return html('<div class="message"><p> '+output+' </p><i class="message-close-btn">&times;</i></div>')

@server.route('/busc_netflix',methods=['GET'])    # método get recibimos los valores
def busc_netflix():
	cuenta = request.args.get('cuenta_netflix')  # se cachan en variables del request con tal nombre
	contras = request.args.get('contra_netflix')
	peli= request.args.get('pelicula_netflix')
	if(is_empty(cuenta) or is_empty(contras)):
		output="No se llenó bien los rubros solicitados. Favor de introducir la información solicitada."
		return html('<div class="message"><p> '+output+str(peli)+' </p><i class="message-close-btn">&times;</i></div>')

	path='chromedriver'      # dirección del driver de chrome

	driver=webdriver.Chrome(path)              #inicializa el webdriver de chrome con la dirección personal de donde se encuentra el driver
	driver.get('https://netflix.com')
	time.sleep(2)
	try:
		if(driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div/div[2]/div[1]/div[2]/form/div/div/button')):   #verifico si el ambiente que abre de netflix es el indicado para realizar las acciones
			print('no se ha iniciado sesión')
			email=driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div/div[2]/div[1]/div[2]/form/div/ul/li/div/div/label/input') #busco donde llenar el espacio siguiendo su dirección con xfullpath
			email.send_keys(cuenta)   #paso el dato que se recibió con el get
			signin=driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div/div[2]/div[1]/div[2]/form/div/div/button').click()  #se envía el formulario oprimiendo el boton
			time.sleep(2)
			if(driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/div/div/div[1]/form/div[2]')):    #veo si se inició bien sesión y si es así ya nada más es una serie de clicks siguiendo direeciones de xfullpath
				contra=driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/div/div/div[1]/form/div[2]/div[1]/div/label/input')
				contra.send_keys(contras)
				entrar=driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/div/div/div[1]/form/button').click()
				time.sleep(2)
				if(driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div[1]/div[2]/div/span')):
					perfil=driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div[1]/div[2]/div/div/ul/li[3]/div/a').click()
					time.sleep(2)
					if(is_empty(peli) and len(peli)>0):   #veo si recibí una pelicula en especifico para buscar, si es así la busca siguiendo mecanismo de clicks e introducir valores
						output='Netflix abierto'
						html('<div class="message"><p> '+output+' </p><i class="message-close-btn">&times;</i></div>')
						time.sleep(300000)
						return render_template('funcionalidades.html')
					else:
						lupa=driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div[1]/div[1]/div/div/div/div[1]/div').click()
						buscador=driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div[1]/div[1]/div/div/div/div[1]/div/div/input')
						buscador.send_keys(peli)					
						output='Películas que tienen coincidencias con el título '+str(peli)
						html('<div class="message"><p> '+output+' </p><i class="message-close-btn">&times;</i></div>')
						time.sleep(300000)
						return render_template('funcionalidades.html')
				else:
					output='La cuenta no es correcta'
					
					return html('<div class="message"><p> '+output+' </p><i class="message-close-btn">&times;</i></div>')

			else:
				output='El correo introducido es incorrecto'
				return html('<div class="message"><p> '+output+' </p><i class="message-close-btn">&times;</i></div>')
	except:
		return html('<div class="message"><p> Hubo un problema con el servidor </p><i class="message-close-btn">&times;</i></div>')


@server.route('/tomar_fotos',methods=['GET'])   # método get recibimos los valores
def tomar_fotos():
	url = request.args.get('url')  # se cachan en variables del request con tal nombre
	cap = cv2.VideoCapture(0)
	direc=os.getcwd()+"/static/imagenes"  #directorio donde el servidor guardará las imagenes filtradas y la original
	filtro = np.ones((5,5),np.float32)/25 #declaro un flitro que suavice la imagen
	# Trabajamos frame a frame
	while(cap.isOpened()):
		ret, frame = cap.read()   
		cv2.imshow('frame',frame)
		time=0
		for i in range(10000):
			time=time+1
		if(time==10000):
			print('Guardando la foto')
			cv2.imwrite('img.png',frame) #guado la imagen 
			img_to_yuv = cv2.cvtColor(frame,cv2.COLOR_BGR2YUV) #cambio espacios de color
			img_to_yuv[:,:,0] = cv2.equalizeHist(img_to_yuv[:,:,0])
			hist_equalization_result = cv2.cvtColor(img_to_yuv, cv2.COLOR_YUV2BGR) #ecualizo
			dst = cv2.filter2D(hist_equalization_result,-1,filtro) #guardo el resultado de la ecualización
			cv2.imwrite('ecualizada.png',hist_equalization_result) #guardo las imagenes
			cv2.imwrite('suavizada.png',dst)
			gray_image = cv2.cvtColor(hist_equalization_result, cv2.COLOR_BGR2GRAY) #cambio espacios de color de imagen para imagen en blanco y negro
			cv2.imwrite('foto_old.png',gray_image)
			
			shutil.copy('foto_old.png', direc+"/"+"foto_old.png")
			shutil.copy('ecualizada.png', direc+"/"+'ecualizada.png')
			shutil.copy('suavizada.png', direc+"/"+'suavizada.png')
			shutil.copy('img.png', direc+"/"+'img.png')


			cap.release()
			cv2.destroyAllWindows()
	return render_template('fotos.html')

@server.route('/conect',methods=['GET'])     # método get recibimos los valores
def conect():
	name = request.args.get('nom_red')       # se cachan en variables con tal nombre
	password = request.args.get('contra_red')
	if(is_empty(name) or is_empty(password)):
		output="No se llenó el rubro solicitado. Favor de introducir la información solicitada."
		return html('<div class="message"><p> '+output+' </p><i class="message-close-btn">&times;</i></div>')

	mensaje=createNewConnection(name, password) #se conecta usando la función de arriba

	output="Ya se ha hecho la conexión con "+name+ " cuyo password introducido fue "+password+". "+mensaje
	return html('<div class="message"><p> '+output+' </p><i class="message-close-btn">&times;</i></div>')

@server.route('/busc_google',methods=['GET'])     # método get recibimos los valores
def busc_google():
	busqueda = request.args.get('busq')           # se cachan en variables con tal nombre

	path='chromedriver'      # dirección del driver de chrome
	try:
		driver=webdriver.Chrome(path)
		driver.get('https://google.com')
		time.sleep(5)
		buscador=driver.find_element_by_xpath('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input') #busca direccion de buscador 
		buscador.send_keys(busqueda)		#introduce valor
		lupa=driver.find_element_by_xpath('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[3]/center/input[1]').click()		#da click en buscar 	
		output='Resultados de búsqueda '+str(busqueda)
		html('<div class="message"><p> '+output+' </p><i class="message-close-btn">&times;</i></div>')
		time.sleep(300000)
		return render_template('funcionalidades.html')
	except:
		return html('<div class="message"><p> Hubo un problema con el servidor </p><i class="message-close-btn">&times;</i></div>')

######################################################################################################
# En caso de que el usuario quiera guardar las fotos tomada por la cámara se puede hacer con sendfile
######################################################################################################

@server.route('/b_n')
def b_n():
   return send_file('foto_old.png', as_attachment=True)

@server.route('/suav')
def suav():
   return send_file('suavizada.png', as_attachment=True)

@server.route('/norm')
def norm():
   return send_file('img.png', as_attachment=True)

@server.route('/contr')
def contr():
   return send_file('ecualizada.png', as_attachment=True)




######################################################################################################
#Se corre el servidor en desde debug para que cualquier modificación en timpo real se vea reflejada en 
#el servidor y no se requiere para su ejecución para ver cómo se ve reflejado el cambio
######################################################################################################

if __name__ == '__main__':
   server.run(debug=True)
  
