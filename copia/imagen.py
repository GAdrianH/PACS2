import mysql.connector
from os import remove

cnx = mysql.connector.connect(user='PACS', password='DICOM1',
                              host='localhost',
                              database='dicom_pru') #----------------MOSTRAR LA INFORMACION DE MI TABLA
# creacion dell cursor
cursor = cnx.cursor()


#abrir el archivo

file= open('Paciente1.dcm','rb')

#leer el archivo

contenido= file.read()

#cierra el archivo
file.close()

#sentencia de interaccion 
sql= "INSERT INTO dicom (idDICOM, DICOMcol, dicomcol2) VALUES (%s,%s, %s)"

# informacion a ingresar
valores= ('5',contenido,'Paci1.dcm')

#insertar registro en la tabla
cursor.execute(sql,valores)

cnx.commit()
"""

# Descargar archivo en el computador

q=input()
#t= "'re.dcm'"
t= "'"+ q + "'"
y='WHERE name = '+ t
sqlret= "SELECT * FROM imagenes2 "+y

print(y)
#sqlret= "SELECT * FROM imagenes2 WHERE address = 'aguzman86'"

cursor.execute(sqlret)

#registro= cursor.fetchone()
registro= cursor.fetchall()
#print(registro[0])
u=[]
for datos in registro:
    u.append(datos[0])


print(u)


"""





    
