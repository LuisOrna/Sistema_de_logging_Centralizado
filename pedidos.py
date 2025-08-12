#DEPENDENCIAS
import requests #Para hacer los POST 
import random #Para aplicar aleatoriedad a la eleccion del log
from datetime import datetime #Para generar el timestamp con la hora actual
import time #Para hacer que las iteraciones no sean inmediatas

#VARIABLES GLOBALES
#Iteraciones
iteraciones = random.randint(10, 20)
#Token
token = 'GHI789RST'

#URL del servidor
url = "http://localhost:5000/logs"

#Datos a enviar
log_pedidos = [
    {"service": "pedidos", "severity": "INFO", "message": "Pedido recibido y validado"},
    {"service": "pedidos", "severity": "INFO", "message": "Stock verificado para todos los productos"},
    {"service": "pedidos", "severity": "INFO", "message": "Pedido enviado a depósito para preparación"},
    {"service": "pedidos", "severity": "INFO", "message": "Pedido empaquetado y etiquetado"},
    {"service": "pedidos", "severity": "INFO", "message": "Pedido despachado con transportista"},
    {"service": "pedidos", "severity": "WARN", "message": "Stock insuficiente para producto en pedido"},
    {"service": "pedidos", "severity": "WARN", "message": "Pedido requiere aprobación manual"},
    {"service": "pedidos", "severity": "WARN", "message": "Retraso en preparación de pedido"},
    {"service": "pedidos", "severity": "ERROR", "message": "Error al procesar pedido - datos incompletos"},
    {"service": "pedidos", "severity": "ERROR", "message": "Fallo en comunicación con depósito"},
    {"service": "pedidos", "severity": "ERROR", "message": "Producto dañado durante empaque"}
]

#Probabilidad de ocurrencia de cada log
pesos = [25, 20, 18, 15, 12, 4, 3, 2, 0.5, 0.3, 0.2]

#Agregar token en el header
headers = {
    "Authorization": f"Token {token}"
}

#FUNCION PRINCIPAL
def ejecutar_pedidos():
    #BUCLE DE REPETICIONES
    for i in range(iteraciones):
        print(f"Enviando log (p) {i+1}/{iteraciones}")
        #ELECION DEL POST
        post_elegido = random.choices(population= log_pedidos, weights= pesos, k= 1)[0]

        #AGREGAR TIME STAMP
        post_elegido['timestamp'] = datetime.now().strftime('%Y-%m-%d, %H:%M:%S')

        #Enviar post
        respuesta = requests.post(url= url, json= post_elegido, headers= headers)

        print(f'Codigo de respuesta(P): {respuesta.status_code}')
        print(f"Respuesta del servidor(P): {respuesta.text}")

        time.sleep(random.randint(4, 15))

if __name__ == '__main__':
    ejecutar_pedidos()
