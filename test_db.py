import mysql.connector

conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Admin",
    database="Nomada"
)

cursor = conexion.cursor()

cursor.execute("SELECT * FROM destinos")

resultados = cursor.fetchall()

for fila in resultados:
    print(fila)

conexion.close()