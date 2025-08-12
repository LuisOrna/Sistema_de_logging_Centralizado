from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

#Lista de tokens validos
TOKENS_VALIDOS = ["ABC123XYZ", "DEF456UVW", "GHI789RST"]


#App
app = Flask(__name__)


#Mensaje de inicio
@app.route('/')
def inicio():
    return "Servidor de logging funcionando"

#Recibir logs
@app.route('/logs', methods = ['POST'])
def recibir_logs(): 
    #Verificar Token primero 
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Token '):
        return jsonify({"Error": "Cliente desconocido"}), 401
    
    token = auth_header.replace("Token ", '')
    if token not in TOKENS_VALIDOS:
        return jsonify({'Error': "Cliente desconocido"}), 401
    
    #Si llega a aqui el token es valido 
    datos = request.get_json()
    print("log recibido:", datos)
    

    #Guardar en la base de datos
    conn = sqlite3.connect('logs.db')
    cursor = conn.cursor()

    cursor.execute(''' INSERT INTO logs (timestamp, service, severity, message, recibido_a_las)
                   VALUES (?, ?, ?, ?, ?)''', (datos['timestamp'], datos['service'], datos['severity'], 
                    datos['message'], datetime.now().strftime('%Y-%m-%d, %H:%M:%S')))
    
    conn.commit()
    conn.close()

    return "Log guardado correctamente", 200

#Consultar Logs
@app.route('/logs', methods= ['GET'])
def consultar_logs():
    '''Permite hacer consultas con filtros, por defecto son consultas de toda la tabla'''

    #En caso de filtros
    timestamp_start = request.args.get('timestamp_start') #Sin el get son dict
    timestamp_end = request.args.get('timestamp_end')
    
    #Segundos filtros
    received_at_start = request.args.get('received_at_start')
    received_at_end = request.args.get('received_at_end')

    #Terceros filtros 
    severity = request.args.get('severity')

    #Cuarto filtro
    service = request.args.get('service')

    #Logica de base de datos
    conn = sqlite3.connect('logs.db')
    cursor = conn.cursor()
    
    #Consulta con truco base
    query = 'SELECT * FROM logs WHERE 1 = 1'
    parametros = [] #en esta lista voy almacenando los parametros que den true

    #Agregar filtros a la consulta, si existen
    if timestamp_start:
        query += ' AND timestamp >= ?'
        parametros.append(timestamp_start)

    if timestamp_end:
        query += ' AND timestamp <= ?'
        parametros.append(timestamp_end)

    #Filtros para received_at
    if received_at_start:
        query += ' AND recibido_a_las >= ?'
        parametros.append(received_at_start)

    if received_at_end:
        query += ' AND recibido_a_las <= ?'
        parametros.append(received_at_end)

    #Filtro Serveity
    if severity:
        query += ' AND severity = ?'
        parametros.append(severity)

    #Filtro Service
    if service:
        query += ' AND service = ?'
        parametros.append(service)

    #Ejecuto la consulta compuesta
    cursor.execute(query, parametros)

    #Resto de la logica
    logs = cursor.fetchall()
    conn.close()

    #Convertir lista resultante 
    resultado = []
    for log in logs:
        resultado.append({
            'id': log[0],
            'timestamp': log[1],
            'service': log[2],
            'severity': log[3],
            'message': log[4],
            'recibido_a_las': log[5]
        })
    return jsonify(resultado) #La lista de diccionarios se convierte en JSON

#RUTAS ADICIONALES
@app.route('/estadisticas', methods= ['GET'])
def estadisticas():
    '''Estadisticas de la tabla, hasta ahora disponible, numero de logs, logs por servicio, logs por severity'''
    conn = sqlite3.connect('logs.db')
    cursor = conn.cursor()

    #Consulta para numero de logs
    cursor.execute('SELECT COUNT(*) FROM logs')
    numero_de_logs = cursor.fetchall()[0][0]
    numero_de_logs = int(numero_de_logs) #El valor en numero se encuentra almacenado en la variable

    #Consulta logs por servicio
    cursor.execute('''SELECT service, COUNT(service) FROM logs
                   GROUP BY service
                   ORDER BY COUNT(service)''')
    conteo_logs_servicio = cursor.fetchall()
    diccionario_conteo_logs_servicio = {service[0]: int(service[1]) for service in conteo_logs_servicio}
    
    #Consulta logs por severity 
    cursor.execute('''SELECT severity, COUNT(severity) FROM logs
                   GROUP BY severity
                   ORDER BY COUNT(severity) DESC''')
    conteo_logs_severity = cursor.fetchall()
    diccionario_conteo_logs_severity = {i[0]: int(i[1]) for i in conteo_logs_severity}

    #Resultante todo en un diccionario y de alli a un JSON
    estadisticas_tabla = {
        'numero_de_logs': numero_de_logs,
        'conteo_logs_service': diccionario_conteo_logs_servicio,
        'conteo_logs_severity': diccionario_conteo_logs_severity
    }
    
    return jsonify(estadisticas_tabla)


if __name__ == '__main__':
    app.run(debug=True)
    