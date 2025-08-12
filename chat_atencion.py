#DEPENDENCIAS
import requests #Para hacer los POST 
import random #Para aplicar aleatoriedad a la eleccion del log
from datetime import datetime #Para generar el timestamp con la hora actual
import time #Para hacer que las iteraciones no sean inmediatas

#VARIABLES GLOBALES
#Iteraciones
iteraciones = random.randint(20, 30)
#Token
token = 'DEF456UVW'

#URL del servidor
url = "http://localhost:5000/logs"

log_chat = [
    {"service": "chat", "severity": "INFO", "message": "Chat iniciado por cliente"},
    {"service": "chat", "severity": "INFO", "message": "Consulta derivada a operador humano"},
    {"service": "chat", "severity": "INFO", "message": "Chat finalizado por cliente"},
    {"service": "chat", "severity": "INFO", "message": "Bot resolvió consulta exitosamente"},
    {"service": "chat", "severity": "INFO", "message": "Operador se conectó al chat"},
    {"service": "chat", "severity": "DEBUG", "message": "Buscando operador disponible"},
    {"service": "chat", "severity": "WARN", "message": "No hay operadores disponibles"},
    {"service": "chat", "severity": "WARN", "message": "Cliente inactivo por más de 5 minutos"},
    {"service": "chat", "severity": "WARN", "message": "Intento de spam detectado"},
    {"service": "chat", "severity": "ERROR", "message": "Error al derivar chat a operador"},
    {"service": "chat", "severity": "ERROR", "message": "Bot no pudo procesar consulta"}
]

pesos = [25, 15, 10, 10, 5, 7, 4, 3, 3, 3, 2]


#Agregar token en el header
headers = {
    "Authorization": f"Token {token}"
}

#FUNCION PRINCIPAL 
def ejecutar_chat_atencion ():
    #BUCLE DE REPETICIONES
    for i in range(iteraciones):
        print(f"Enviando log (CA) {i+1}/{iteraciones}")
        #ELECION DEL POST
        post_elegido = random.choices(population= log_chat, weights= pesos, k= 1)[0]

        #AGREGAR TIME STAMP
        post_elegido['timestamp'] = datetime.now().strftime('%Y-%m-%d, %H:%M:%S')

        #Enviar post
        respuesta = requests.post(url= url, json= post_elegido, headers= headers)

        print(f'Codigo de respuesta (CA): {respuesta.status_code}')
        print(f"Respuesta del servidor (CA): {respuesta.text}")

        time.sleep(random.randint(4, 15))

if __name__ == '__main__':
    ejecutar_chat_atencion()