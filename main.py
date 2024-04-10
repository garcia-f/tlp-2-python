# import sys
import csv
import MySQLdb as mysql



# Conexión a la base de datos
try:
    db = mysql.connect("localhost","root","","localidadesdb" )
except mysql.Error as e:
    print("No se pudo conectar a la base de datos:", e)
    exit(1)


# crear una tabla para el archivo localidades.csv
try:
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS localidades;")
    cursor.execute("""CREATE TABLE localidades (
                   provincia VARCHAR(255), 
                   `id` INT(11),
                   localidad VARCHAR(255),
                   cp INT(11), id_prov_mstr INT(11))""")
    # leer el archivo localidades.csv
    with open('localidades.csv', 'r', newline='') as archivo_csv:
        lector_csv = csv.reader(archivo_csv, delimiter=',', quotechar='"')
        next(lector_csv)  # Para omitir la fila de encabezados si la hay
        for fila in lector_csv:
            provincia, id, localidad, cp, id_prov_mstr = fila
            cursor.execute("INSERT INTO localidades (provincia, id, localidad, cp, id_prov_mstr) VALUES (%s, %s, %s, %s, %s)", (provincia, id, localidad, cp, id_prov_mstr))
            print(fila)
    # Confirmar la transacción
    db.commit()

except mysql.Error as e:
    db.rollback()
    print(e)

# # Cerrar la conexión a la base de datos
# db.close()


# crea un archivo csv por cada provincia
try:
    cursor = db.cursor()
    cursor.execute("SELECT DISTINCT provincia FROM localidades;")
    provincias = cursor.fetchall()
    for provincia in provincias:
        cursor.execute("SELECT * FROM localidades WHERE provincia = '%s'" % (provincia[0]))
        localidades = cursor.fetchall()
        with open(f"provincias/{provincia[0]}.csv", "w", newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(localidades)
except mysql.Error as e:
    db.rollback()
    print(e)



