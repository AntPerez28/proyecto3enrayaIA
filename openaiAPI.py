from openai import OpenAI
import credentials

# Me ha sido de mucha utilidad la documentación de OpenAI para realizar las peticiones a la API.
# https://platform.openai.com/docs/quickstart?context=python

# Esta función se encarga de reañlizar la petición a la API de ChatGPT para que analice el estado actual del tablero
# de juego y coloque una ficha. La respuesta debería devolver el tablero con la nueva ficha.
def peticionJugadaAPI(tablero):

    client = OpenAI(
        api_key=credentials.api_key,
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": f"Estás jugando al tres en raya. Eres el jugador 2. Tu adversario es el jugador 1. "
                        f"El tablero inicial es una matriz 3x3 llena de 0. Solo puedes colocar una nueva "
                        f"ficha en las posiciones con un 0. Este es el estado actual del tablero: {tablero}. "
                        f"Es tu turno. Responde con el nuevo tablero actualizado."},
        ]
    )

    return response.choices[0].message.content.strip()

# Documentación para la trabscripción de audio. https://platform.openai.com/docs/guides/speech-to-text/quickstart

# Esta función se encarga de realizar la petición a la API de OpenAI para transcribir el audio a texto.
def peticionTranscribirAudio():
    client = OpenAI(
        api_key=credentials.api_key,
    )

    audio_file = open("recursos/audio.mp3", "rb")
    response = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        response_format="text"
    )

    return str(response)