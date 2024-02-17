import pyaudio
import wave
import re
import xml.etree.ElementTree as ET
import os
from xml.dom import minidom
from datetime import datetime
import socket

# Función que graba desde el micrófono. Se le pasará por parámetro el fichero de
# sonido en formato mp3, la duración de la grabación, y la etiqueta de la interfaz para informar al usuario que se
# está grabando. He obtenido información útil para esta función en esta página:
# https://programacionpython80889555.wordpress.com/2018/10/16/grabacion-de-sonido-con-pyaudio-ejercicio-basico-en-python/
def grabarAudio(ruta,duracion, etiqueta):
    # Parametros del audio
    chunk = 1024
    rate = 44100
    canales = 2
    formato = pyaudio.paInt16

    # Instanciamos PyAudio
    p = pyaudio.PyAudio()

    # Abrimos stream. En este caso, como  vamos a leer audio, usamos input a true.
    stream = p.open(format=formato,
                    channels=canales,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk)

    #print("Grabando...")
    # Aquí es donde, en lugar de hacer un print de Grabando, lo mostramos en la etiqueta de la interfaz.
    etiqueta.config(text=f'Grabando...')
    etiqueta.update_idletasks()

    # Leemos los datos
    frames = []

    # Vamos guardando cada segundo de audio en el array frames
    for i in range(0, int(rate/chunk*duracion)):
        data = stream.read(chunk)
        frames.append(data)

    #print("Grabación terminada.")
    # Lo mismo para decir que ha terminado la grabación, actualizamos el mensaje de la interfaz.
    etiqueta.config(text=f'Grabación terminada.')
    etiqueta.update_idletasks()

    # Paramos el stream y lo cerramos
    stream.stop_stream()
    stream.close()

    # Cerramos PyAudio
    p.terminate()

    # Guardamos el audio en el fichero
    file = wave.open(ruta, "wb")
    file.setnchannels(canales)
    file.setsampwidth(p.get_sample_size(formato))
    file.setframerate(rate)
    file.writeframes(b"".join(frames))
    file.close()
    return

# Con esta función analizamos el texto de la respuesta de la API en la transcripción, buscamos con patrones, si el
# mensaje contiene el número en texto o en dígito, y lo devolvemos. Así nos evitamos problemas con la respuesta,
# ya que hay veces que se cuela otro contenido en el audio. Si no contiene los dígito que necesitamos, devolvemos
# Error.
def obtenerNumero(texto):

    if re.search(r'\b(?:uno|1)\b', texto, re.IGNORECASE):
        return 1
    elif re.search(r'\b(?:dos|2)\b', texto, re.IGNORECASE):
        return 2
    elif re.search(r'\b(?:tres|3)\b', texto, re.IGNORECASE):
        return 3
    elif re.search(r'\b(?:cuatro|4)\b', texto, re.IGNORECASE):
        return 4
    elif re.search(r'\b(?:cinco|5)\b', texto, re.IGNORECASE):
        return 5
    elif re.search(r'\b(?:seis|6)\b', texto, re.IGNORECASE):
        return 6
    elif re.search(r'\b(?:siete|7)\b', texto, re.IGNORECASE):
        return 7
    elif re.search(r'\b(?:ocho|8)\b', texto, re.IGNORECASE):
        return 8
    elif re.search(r'\b(?:nueve|9)\b', texto, re.IGNORECASE):
        return 9
    else:
        return "Error"

# Con esta función pasaremos la lista a un tablero en string para poder mandarselo a la
# API de ChatGPT y así, lo entienda mejor.
def pasarTableroATexto(lista):
    lista_procesada = [1 if elem == "X" else 2 if elem == "O" else 0 for elem in lista]
    return f"""| {lista_procesada[0]} | {lista_procesada[1]} | {lista_procesada[2]} |
---------
| {lista_procesada[3]} | {lista_procesada[4]} | {lista_procesada[5]} |
---------
| {lista_procesada[6]} | {lista_procesada[7]} | {lista_procesada[8]} |
"""

# Con esta función vamos a recoger solo el tablero de la respuesta de la API, ya que la respuesta
# pueden ser más cosas a parte del tablero, y vamos a convertirlo en una lista de la misma
# estructura que necesita la interfaz.
def obtenerListaDeTableroApi(tablero):
    # Utilizamos esta expresión regular para encontrar todos los números precedidos por | y un espacio en blanco
    lista = re.findall(r'\|\s*(\d+)', tablero)

    # Convierte las cadenas de números a enteros
    lista = [int(numero) for numero in lista]

    lista = ["X" if elem == 1 else "O" if elem == 2 else None for elem in lista]

    return lista

# Esta funcion se encargará de comparar las dos listas que corresponden a los tableros, el que hay actualmente,
# y la respuesta que da la API, si hay algun cambio devolvemos el indice que ha cambiado para colocar la ficha de la
# API, si no ha cambiado nada entonces devolveremos None. Esta función nos servirá para controlar posibles errores
# de la API al colocar una ficha, errores que suelen ocurrir.
def encontrarPosicionDistinta(lista_anterior, lista_nueva):
    for i in range(len(lista_anterior)):
        if lista_anterior[i] != lista_nueva[i]:
            return i
    return None

# Esta función se encarga de guardar información sobre la partida, como la hora de inicio y fin, el nombre
# del equipo, tablero final y el ganador.
def guardarInfo(hora_inicio, lista_tablero, j_ganador):

    rutaXml = "./recursos/datos.xml"

    if os.path.exists(rutaXml):
        tree = ET.parse(rutaXml)
        root = tree.getroot()
    else:
        root = ET.Element("registros")

    ejecucion = ET.Element("ejecucion")

    equipo = ET.Element("equipo")
    equipo.text = socket.gethostname()
    ejecucion.append(equipo)

    now = datetime.now()

    hora = ET.Element("hora")
    h_inicio = ET.Element("inicio")
    h_inicio.text = hora_inicio
    hora.append(h_inicio)
    h_fin = ET.Element("fin")
    h_fin.text = str(now.hour) + ":" + str(now.minute) + ":" + str(now.second)
    hora.append(h_fin)
    ejecucion.append(hora)

    tablero = ET.Element("tablero")
    tablero.text = '|'.join(str(elem) for elem in lista_tablero)
    ejecucion.append(tablero)

    ganador = ET.Element("ganador")
    ganador.text = j_ganador
    ejecucion.append(ganador)

    root.append(ejecucion)

    with open(rutaXml, "wb") as xml:
        xml.write(formatearXml(root).encode("utf-8"))
    return

# Funcion para formatear xml
def formatearXml(elem):
    rough_string = ET.tostring(elem,"utf-8")
    reparsed = minidom.parseString(rough_string)
    return '\n'.join([line for line in reparsed.toprettyxml(indent=' ' * 2).split('\n') if line.strip()])