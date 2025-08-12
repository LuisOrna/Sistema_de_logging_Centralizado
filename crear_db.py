import sqlite3

#Creo la base de datos
conn = sqlite3.connect('logs.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS logs
               (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                timestamp TEXT,
                service TEXT,
                severity TEXT,
                message TEXT,
                recibido_a_las TEXT)''')

conn.commit()
conn.close()
print("Base de datos creada")
