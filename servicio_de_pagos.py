#DEPENDENCIAS
import requests #Para hacer los POST 
import random #Para aplicar aleatoriedad a la eleccion del log
from datetime import datetime #Para generar el timestamp con la hora actual
import time #Para hacer que las iteraciones no sean inmediatas

#VARIABLES GLOBALES
#Iteraciones
iteraciones = random.randint(10, 20)
#Token
token = 'ABC123XYZ'

#URL del servidor
url = "http://localhost:5000/logs"

#Datos a enviar
log_pagos = [
    {"service": "pagos", "severity": "ERROR", "message": "Pago rechazado por fondos insuficientes"},
    {"service": "pagos", "severity": "INFO", "message": "Pago procesado exitosamente"},
    {"service": "pagos", "severity": "ERROR", "message": "Error de conexión con pasarela de pago"},
    {"service": "pagos", "severity": "ERROR", "message": "Transacción duplicada detectada"},
    {"service": "pagos", "severity": "INFO", "message": "Usuario ha abandonado la pasarela"}
    ]

#Probabilidad de ocurrencia de cada log
pesos = [10, 60, 5, 5, 20] #siguen el mismo orden de la lista log_pagos


#Agregar token en el header
headers = {
    "Authorization": f"Token {token}"
}

def ejecutar_servicio_pagos ():
    #BUCLE DE REPETICIONES
    for i in range(iteraciones):
        print(f"Enviando log servicio de pagos {i+1}/{iteraciones}")
        #ELECION DEL POST
        post_elegido = random.choices(population= log_pagos, weights= pesos, k= 1)[0]

        #AGREGAR TIME STAMP
        post_elegido['timestamp'] = datetime.now().strftime('%Y-%m-%d, %H:%M:%S')

        #Enviar post
        respuesta = requests.post(url= url, json= post_elegido, headers= headers)

        print(f'Codigo de respuesta(SP): {respuesta.status_code}')
        print(f"Respuesta del servidor(SP): {respuesta.text}")

        time.sleep(random.randint(4, 15))

if __name__ == '__main__':
    ejecutar_servicio_pagos()