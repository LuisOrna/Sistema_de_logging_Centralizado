## DESCRIPCION
El proyecto esta enfocado a la creacion de un sistema de loggins centralizado, es decir tener aplicaciones(simuladas) que generan logs y envian a un servidor, este servidor guarda los datos en una base de datos.

Para un mejor entendimiento y viasualizacion se puede ver:
[Esquema y diagrama de flujo del proyecto](https://miro.com/app/board/uXjVJXKt1LQ=/?share_link_id=670224869519&shareablePresentation=1 "Este enlace te lleva a una presentación en MIRO")  

https://github.com/LuisOrna/Sistema_de_logging_Centralizado/blob/main/base%20de%20datos.jpg



### Archivos

#### servidor.py
Es el servidor central (api) y tiene las siguientes funciones:
Recibe los logs enviados a: POST /logs.
Verifica el token de autenticación.
Guarda los logs en una base de datos.
Tiene las rutas (endpoints) para consultar los logs: GET/logs
Tiene una ruta adicional para obtener estadisticas: GET/estadisticas
Acepta parametros opcionales en la ruta GET/logs:
  - severity: ERROR, INFO, DEBUG
  - service: pagos, pedidos, usuarios
  - timestamp_start: formato YYYY-MM-DD
  - timestamp_end: formato YYYY-MM-DD

#### central.py
Es un archivo que articula los 3 servicios (simulados), funciona importando los archivos donde esta el codigo de cada uno de los servicios y creando un hilo (thread) de ejeccion para cada uno de ellos. Tiene un thread.join() para pausar la ejecicion hasta que el thread finalice. 

#### chat_atencion.py, pedidos.py, servicio_de_pagos.py
Estos tres archivos tienen la misma estructura y codigo, varian en la lista manual de logs que cada uno tiene y el token con el cual se identifican. Su funcion principal es elegir logs aleatorios de acuerdo a una probabilidad de ocurrencia (pesos). La cantidad de iteraciones esta controlada por una variable que es alegida aleatoriamente dentro de un rango y al final de la iteracion se ejecuta un delay cuyo tiempo tambien es elegido aleatoriamente dentro de un rango configurable de numeros. 

#### crear_db.py
Su funcion es la creacion de la base de datos, decidi hacerlo en un archivo a aparte para evitar que se itere repetidamente este comando y ademas para protegerlo del acceso del servidor. 

### Ejecucion
Para crear la base de datos se ejecuta el archivo crear_db.py
Para poder acceder a la base de datos, consultas y permitir la carga de nuevos logs, se debe ejecutar el archivo servidor.py
Para que inicie la carga automatica de logs, debe estar en ejecucion el archivo servidor.py y posteriormente se ejecuta el archivo central.py, la ejecucion de este archivo termina de manera limpia una vez que se finalizan la cantidad de iteraciones configuradas y se finalizan los hilos, threads.

---

### Apendizajes
Antes de iniciar este proyecto el concepto de logging era desconocido. 
Sin embargo sin saber su nombre al momento de trabajar en proyectos previos era algo de lo cual sentia necesidad. 

Tambien este proyecto me permitio comenzar a modularizar, sin embargo no lo hice porque debia, sino porque el proyecto me hizo sentir en necesidad de hacerlo. 

Tambien entendi mejor como funcionan los servidores de una pagina web, como una api conecta diferentes puntos y a leer una url y los simbolos ('/' , '?', '=')

El protocolo de HTTP es muy fuerte y manejarlo es clave para poder establecer comunicaciones claras, entender los metodos POST y GET esfundamental para entender las bases de la comunicacion por este medio.

Aprendi tambien a utilizar la herramienta POSTMAN, que permite construir api's de manera sencilla y definitivamente me habria gustado comenzar a aplicarlo desde el principio de la construccion del proyecto, habria facilitado mucho las cosas. 

Conoci y trabaje por primera vez con JSON que era un termino y un tipo de archivo con el cual me habia topado varias veces y realmenteno entendia porque es tan conocido y fugura en todas partes. Ahora me doy cuenta que conocerlo y manejarlo es esencial. 

