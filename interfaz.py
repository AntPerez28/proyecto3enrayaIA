import tkinter as tk
import funciones
import openaiAPI

# He ido haciendo la interfaz con la documentación de tkinter (https://docs.python.org/es/3/library/tkinter.html)
# y preguntanto a chatGPT.
class InterfazTresEnRaya:
    def __init__(self, root):
        self.root = root
        self.root.title("3 en Raya")

        # Inicializamos el tablero, el primero tendrá la propia tabla de la interfaz, donde mostraremos digitos
        # del 1 al 9, y X o O para las fichas. El otro tablero será una lista con las casillas vacias en None,
        # y las fichas como X y O, esta lista la usaremos para comprobar el ganador y la que formatearemos para
        # pasarsela a la API.
        self.tablero = [None] * 9
        self.lista_tablero = [None] * 9

        # Aquí crearemos el tablero de la interfaz, y etiquetaremos cada celda con la posición para poder colocar las
        # fichas posteriormente con más facilidad.
        for i in range(3):
            for j in range(3):
                numero_celda = i * 3 + j
                etiqueta_celda = tk.Label(root, text=str(numero_celda + 1), width=10, height=5, relief="solid", borderwidth=1)
                etiqueta_celda.grid(row=i, column=j)
                self.tablero[numero_celda] = etiqueta_celda

        # Creamos una campo de texto, una etiqueta, para colocar mensajes, como por ejemplo si ha ganado algún jugador.
        self.etiqueta_victoria = tk.Label(root, text='', font=('Helvetica', 14))
        self.etiqueta_victoria.grid(row=4, column=0, columnspan=3, pady=10)

        # Botón para comenzar a grabar audio, y que se realicen todos los demás procesos del juego.
        self.boton_grabar_colocar = tk.Button(root, text='Grabar y Colocar Ficha', command=self.grabar_y_colocar)
        self.boton_grabar_colocar.grid(row=5, column=0, columnspan=3, pady=10)

        # Botón para reiniciar el tablero y empezar desde el principio.
        self.boton_reiniciar = tk.Button(root, text='Reiniciar Tablero', command=self.reiniciar_tablero)
        self.boton_reiniciar.grid(row=6, column=0, columnspan=3, pady=10)

    # Esta es la función que se ejecutará al pulsar el boton de grabar audio. Representa la lógica principal del juego.
    # Primero llamaremos a la funcion para grabar audio, luego se pasará el audio a la API para transcribirlo, comprobamos si se ha transcrito bien,
    # si no es así, se muestra un mensaje de error. Si está correcto, colocamos la ficha, comprobamos si hay ganador,
    # si no, hacemo la peticion a la API para que coloque su ficha, comprobamos si hay ganador de nuevo. Si la
    # petición a la API falla, se mostrará un mensaje de error y se eliminará la ficha colocada por el usuario para que
    # la coloque de nuevo.
    def grabar_y_colocar(self):
        # Reseteamos el mensaje de la etiqueta.
        self.etiqueta_victoria.config(text=f'')
        self.etiqueta_victoria.update_idletasks()

        # Grabamos el audio de la ficha del usuario. Y mandamos el audio a la API para transcribirlo.
        funciones.grabarAudio("recursos/audio.mp3", 2, self.etiqueta_victoria)
        self.etiqueta_victoria.config(text=f'')
        resultado = openaiAPI.peticionTranscribirAudio()

        # Con el numero que obtenemos, lo pasamos a la función que obtiene el numero, por si se ha colado algo más
        # en el audio, así solo recogemos el número.
        numero_obtenido = funciones.obtenerNumero(resultado)
        #print(numero_obtenido)

        # Si el audio se ha obtenido correctamente, procedemos a colocar fichas y llamar a la API, pero
        # si el audio falla, mostramos mensaje de error.
        if numero_obtenido != "Error":
            # Al número obtenido le restamos 1 para que coincida con el índice de la lista. Colocamos nuestra ficha X.
            self.colocar_ficha(numero_obtenido - 1, "X")

            # Comprobamos si hay ganador. Si lo hay, ponemos quien ha ganado en la etiqueta. Si hay empate, lo colocamos
            # también, en los dos casos bloquearemos el botón de grabar porque ya se ha terminado el juego. Si no
            # hay ganador seguimos con la lógica del juego.
            ganador = self.ha_ganado()
            #print(ganador)
            if ganador:
                self.etiqueta_victoria.config(text=f'¡Ha ganado el jugador {ganador}!')
                self.boton_grabar_colocar.config(state="disabled")
            elif ganador == "Empate":
                self.etiqueta_victoria.config(text=f'¡Empate!')
                self.boton_grabar_colocar.config(state="disabled")
            else:

                # Procesamos el tablero/lista de la interfaz a texto y se lo pasamos a la API.
                # Obtenemos respuesta y la procesamos para quedarnos con una lista de
                # igual estructura a la lista de la interfaz. Buscamos la posicion que ha colocado
                # la API y colocamos la ficha, si ha fallado, volvemos al estado inicial y mostramos mensaje de error.

                tablero_procesado = funciones.pasarTableroATexto(self.lista_tablero)
                #print(tablero_procesado)
                respuesta_api = openaiAPI.peticionJugadaAPI(tablero_procesado)
                #print(respuesta_api)
                lista_api = funciones.obtenerListaDeTableroApi(respuesta_api)
                #print(self.lista_tablero)
                #print(lista_api)
                posicion_colocada_api = funciones.encontrarPosicionDistinta(self.lista_tablero,lista_api)
                #print(posicion_colocada_api)

                # Si la posición de la ficha de la API ha resultado correcta, se coloca, no hace falta restar 1 porque
                # en este caso, obtenemos la posición empezando por 0. Si la posición ha resultado como None, entonces
                # Se vuelve al estado inicial antes de iniciar la grabación. Y mostramos el error.
                if posicion_colocada_api is not None:
                    self.colocar_ficha(posicion_colocada_api, "O")
                else:
                    self.tablero[numero_obtenido - 1].configure(text=str(numero_obtenido))
                    self.lista_tablero[numero_obtenido - 1] = None
                    self.etiqueta_victoria.config(text='Error adversario.')


                # Comprobamos si hay ganador de nuevo, una vez colocada la ficha de la API
                ganador = self.ha_ganado()
                print(ganador)
                if ganador:
                    self.etiqueta_victoria.config(text=f'¡Ha ganado el jugador {ganador}!')
                    self.boton_grabar_colocar.config(state="disabled")
                elif ganador == "Empate":
                    self.etiqueta_victoria.config(text=f'¡Empate!')
                    self.boton_grabar_colocar.config(state="disabled")

        else:
            self.etiqueta_victoria.config(text='Error audio.')

    # Con esta función colocaremos la ficha en el tablero de la interfaz, y además en la lista.
    def colocar_ficha(self, numero_celda, ficha):
        # Lógica para colocar la ficha (X o O) en la celda deseada
        self.tablero[numero_celda].configure(text=ficha)
        self.lista_tablero[numero_celda] = ficha

    # Con esta función comprobaremos si hay ganador o hay empate. Si hay ganador, se devolverá X o O dependiendo de
    # quien haya ganado, si hay empate devolveremos Empate, y si no hay nada, devolveremos None.
    def ha_ganado(self):
        # Comprobamos las filas.
        for i in range(0, 9, 3):
            if self.lista_tablero[i] == self.lista_tablero[i + 1] == self.lista_tablero[i + 2] and self.lista_tablero[i] is not None:
                return self.lista_tablero[i]

        # Comprobamos las columnas.
        for i in range(3):
            if self.lista_tablero[i] == self.lista_tablero[i + 3] == self.lista_tablero[i + 6] and self.lista_tablero[i] is not None:
                return self.lista_tablero[i]

        # Comprobamos las diagonales.
        if self.lista_tablero[0] == self.lista_tablero[4] == self.lista_tablero[8] and self.lista_tablero[0] is not None:
            return self.lista_tablero[0]
        if self.lista_tablero[2] == self.lista_tablero[4] == self.lista_tablero[6] and self.lista_tablero[2] is not None:
            return self.lista_tablero[2]

        # Comprobamos si hay empate viendo si quedan None en la lista.
        if None not in self.lista_tablero:
            return "Empate"

        # Si no hay ganador
        return None

    # Esta será la función que se ejecutará al pulsar el botón de reiniciar. Volveremos el tablero y la lista al
    # estado inicial, y la etiqueta de los mensajes la dejaremos vacia. Además habilitaremos de nuevo el botón para
    # grabar.
    def reiniciar_tablero(self):
        # Reiniciar el tablero asignando los números iniciales a las celdas y limpiando el mensaje de victoria
        for i, etiqueta_celda in enumerate(self.tablero):
            etiqueta_celda.configure(text=str(i + 1))  # Restaurar los números iniciales

        self.etiqueta_victoria.config(text='')  # Limpiar el mensaje de victoria
        self.lista_tablero = [None] * 9
        self.boton_grabar_colocar.config(state="normal")

# Con esto iniciamos la interfaz, creamos el objeto de la interfaz.
if __name__ == "__main__":
    root = tk.Tk()
    interfaz = InterfazTresEnRaya(root)
    root.mainloop()