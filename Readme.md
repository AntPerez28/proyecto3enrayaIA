# Proyecto IA - 3 en raya

<div style="text-align: justify;">
Con este proyecto podremos jugar una partida del 3 en raya contra ChatGPT de OpenAI. Nosotros jugaremos como la ficha "X" y la IA como "O". La colocación de las fichas se realizará por voz, debemos decir el número de la celda donde queremos colocar nuestra ficha, y ChatGPT colocará la suya justo después.


Al ejecutar la interfaz del proyecto, tendremos un tablero 3 x 3, cuyas celdas estarán numeradas del 1 al 9.
Habrá una etiqueta de texto justo debajo, para mensajes de errores, victoria, empate... Y por último, tendremos dos botones, uno para grabar audio y otro para resetear el juego.
</div>

## Elementos necesarios

<div style="text-align: justify;">Necesitaremos 4 ficheros .py, y una carpeta. Estos son los elementos:</div>

- `credentials.py`

- `funciones.py`

- `interfaz.py`

- `openaiAPI.py`

- `recursos/`

<div style="text-align: justify;">Vamos a ver cada fichero uno a uno.</div>

### credentials.py

<div style="text-align: justify;">
En este fichero, tendremos las credenciales de acceso a OpenAI, es decir, nuestra key. No se aporta en este proyecto, por privacidad, y por tanto deberemos crearlo para que el proyecto funcione correctamente. Posteriormente en el apartado de puesta en marcha, veremos que debemos hacer para que el proyecto funcione.

Esta es la estructura que tendrá este fichero:

</div>

```python
# Key de acceso a la API de OpenAI
api_key="coloque_aqui_su_key"
```

### funciones.py

<div style="text-align: justify;">
Este fichero se proporciona en el proyecto y contiene las funciones:

- `grabarAudio`: Función para grabar el audio del micrófono.

- `obtenerNumero`: Función para obtener el número del texto que obtenemos al transcribir el audio.

- `pasarTableroATexto`: Función para pasar el tablero en forma de lista a un string para ChatGPT.

- `obtenerListaDeTableroApi`: Función para pasar el tablero en string que responde ChatGPT a un tablero en lista.

- `encontrarPosicionDistinta`: Función que compara el tablero actual con el tablero de ChatGPT, obtiene la posición distinta.

- `guardarInfo`: Función para guardar información de la aplicación en un xml llamado `datos.xml` en la carpeta `recursos`, si no existe se creará automáticamente.

- `formatearXml`: Función que se encargará de formatear el xml para que sea más bonito visualmente.

Todas estas funciones son necesarias para realizar diversas funciones importantes, procesar y estructurar los datos.

Para funcionar necesitará las librerias `pyaudio`, `wave` y `re`.
</div>

### interfaz.py

<div style="text-align: justify;">
Este fichero contiene la interfaz de la aplicación, tenemos una clase `InterfazTresEnRaya`, con sus atributos y sus métodos. Hará uso del fichero `funciones.py` y `openaiAPI.py` para funcionar correctamente. Y necesitará la librería `tkinter`. 

Este fichero se proporciona con el proyecto.
</div>

### openaiAPI.py

<div style="text-align: justify;">
Este fichero se encargará de toda la conexión a la API de OpenAI, se usará ChatGPT como el adversario del juego, y Whisper para el speech-to-text del audio. Necesitará el fichero `credentials.py`, y la librería `openai`.

Contiene estas dos funciones:

- `peticionJugadaAPI`: conectará con ChatGPT para que realice su jugada.

- `peticionTranscribirAudio`: conectará con whisper de OpenAI, para pasar el audio a texto.

Este fichero se proporciona con el proyecto.
</div>

### recursos/

<div style="text-align: justify;">
Esta carpeta no se proporciona con el proyecto por lo que habrá que crearla, contendrá el fichero de audio donde se grabará la jugada del usuario, y el fichero de datos con información de la partida. Estos fichero se crearán automaticamente, por lo que solo será necesario crear la carpeta vacía. El nombre del fichero de es "audio.mp3", y el de datos "datos.xml".
</div>

## Librerías utilizadas

<div style="text-align: justify;">
Se han usado varias librerías para el funcionamiento de la aplicación. Estos son sus usos en la aplicación:
</div>

- `openai`: Para trabajar con la API de OpenAI.
- `pyaudio`: Para poder realizar grabación de audio.
- `tkinter`: Para realizar la interfaz.
- `datetime`: Para recoger la hora del equipo.
- `wave`: Para poder trabajar con los ficheros de audio.
- `re`: Para trabajar con expresiones regulares.
- `ElementTree`: Para crear elementos xml.
- `os`: Para trabajar con rutas.
- `minidom`: Para formatear xml.
- `socket`: Para recoger información del equipo.

## Puesta a punto

<div style="text-align: justify;">
Todo este proyecto se ha realizado en `python 3.12.0`, por lo que para mayor compatibilidad se recomienda el uso de esa versión.

Colocamos los ficheros que se proporcionan con este proyecto, es decir, `funciones.py`, `interfaz.py` y `openaiAPI.py`, en una carpeta con el nombre del proyecto.

Creamos un fichero en la raíz del proyecto, es decir, al mismo nivel que los tres ficheros anteriores, que se llame `credentials.py`. Su contenido será el mostrado en el apartado donde hablamos sobre ese fichero (deberás de tener una key de OpenAI y sustituir "coloque_aqui_su_key" por la tuya).

A continuación, creamos la carpeta `recursos/` en la raíz del proyecto.

Ahora deberemos instalar las librerías necesarias para que el proyecto funcione, en la terminal vamos instalandolas una a una:

</div>

```
pip install openai
pip install pyaudio

```

`tkinter` debería funcionar por defecto en Python, como ocurre con la librería `re` para expresiones regulares que también necesitamos, pero si no funcionase con un `import`, podemos instalarlo como:

```
pip install tk
```

Con todo esto, estaremos preparados para hacer funcionar el proyecto.

## Funcionamiento

<div style="text-align: justify;">
Una vez hemos realizado la puesta a punto, debemos ejecutar el fichero `interfaz.py`. Al hacerlo, nos aparecerá la interfaz de la aplicación que mostrará un tablero de 9 celdas, con números del 1 al 9.

Pulsamos sobre el boton para grabar el audio, y aparecer que se está grabando. Diremos solamente el número de la casilla, nada más, es decir, no hay que decir una frase, solo el número de la celda. Si la transcripción no tiene éxito, aparecerá un mensaje en pantalla que indicará que ha habido un error de audio, entonces, deberemos volver a pulsar el botón de grabar y volver a seleccionar una casilla. Si la transcripción del audio es exitosa, se prodecerá a pedir el movimiento a ChatGPT. Si la petición a la API no tiene éxito, se mostrará un mensaje indicando que hay un error con la API, por lo que se eliminará el movimiento del usuario y tendrás que volver a elegir celda.

En cada movimiento se comprobará si hay algún ganador, por lo que cuando lo haya, aparecerá un mensaje en pantalla que indica quien ha ganado, posteriormente se bloqueará el botón de grabar audio para que no se pueda seguir jugando. 

Puedes reiniciar el juego en cualquier momento, lo que devuelve todo el tablero a su estado inicial.
</div>