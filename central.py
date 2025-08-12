import threading
import servicio_de_pagos
import chat_atencion
import pedidos

if __name__ == '__main__':
    
    print("Iniciando todos los servicios...")

    #Creo los hilos para cada uno
    thread_pagos = threading.Thread(target=servicio_de_pagos.ejecutar_servicio_pagos)
    thread_atencion = threading.Thread(target=chat_atencion.ejecutar_chat_atencion)
    thread_pedidos = threading.Thread(target=pedidos.ejecutar_pedidos)

    #Inicio los hilos
    thread_pagos.start()
    thread_atencion.start()
    thread_pedidos.start()

    #Esperar a que terminen todos
    thread_pagos.join()
    thread_atencion.join()
    thread_pedidos.join()

    print('Los servicios han terminado')


