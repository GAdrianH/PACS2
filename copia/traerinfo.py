import mysql.connector
from os import remove
from pydicom import dcmread




## ----------------Enviar LA INFORMACION DE MI TABLA informe

def EnvInfo(Nombre,Info):
 cnx = mysql.connector.connect(user='PACS', password='DICOM1',
                               host='localhost',
                               database='dicom_pru')
 cursor = cnx.cursor()
 sqlInsertar = "insert into informe(NombrePaciente,Informe)values(%s,%s)"
 #y=' Paciente en buenas condiciones'
 #z='1.2.826.0.1.3680043.8.1055.1.20111102150758591.03296050.69180943'
 cursor.execute(sqlInsertar,(Nombre,Info))
 cnx.commit() #FORZAR EL GUARDADO DE LOS DATOS EN LA BD
 cursor.close()
 cnx.close()
 return()

#EnvInfo('Blanca','Examen sin anomalías')


## ----------------Enviar LAS IMAGENES A MI TABLA DICOM

def EnvIma(nombre):

 dire='./Subir_imagen_DICOM/'+nombre
 file= open(dire,'rb')
 contenido= file.read()
 file.close()
 cnx = mysql.connector.connect(user='PACS', password='DICOM1',
                               host='localhost',
                               database='dicom_pru')
 cursor = cnx.cursor()
 sqlInsertar = "insert into dicom(ID,Image,Name_Img)values(%s,%s,%s)"
 cursor.execute(sqlInsertar,('6',contenido,nombre))
 cnx.commit() #FORZAR EL GUARDADO DE LOS DATOS EN LA BD
 cursor.close()
 cnx.close()
 return()

#EnvIma('Paciente1.dcm')

## ----------------RECIBIR  LAS IMAGENES A MI TABLA DICOM

def ReciIma():

 cnx = mysql.connector.connect(user='PACS', password='DICOM1',
                               host='localhost',
                               database='dicom_pru')
# creacion dell cursor
 cursor = cnx.cursor()
 sqlret= "SELECT * FROM dicom "
 cursor.execute(sqlret)

#registro= cursor.fetchone()
 registro= cursor.fetchall()
#print(registro[0])
 u=[]
 t=[]
 for datos in registro:
     u.append(datos[0])
     t.append(datos[2])

 l=len(t)
 #print(u[0])
 #print(t[0])
 return(u,t,l)

#ReciIma()
## ----------------RECIBIR  LAS Iinforme de MI TABLA informes

def ReciInforme():

 cnx = mysql.connector.connect(user='PACS', password='DICOM1',
                               host='localhost',
                               database='dicom_pru')
# creacion dell cursor
 cursor = cnx.cursor()
 sqlret= "SELECT * FROM informe "
 cursor.execute(sqlret)

#registro= cursor.fetchone()
 registro= cursor.fetchall()
#print(registro[0])
 u=[]
 t=[]
 for datos in registro:
     u.append(datos[0])
     t.append(datos[1])

 l=len(t)
 #print(u[0])
 #print(t[0])
 return(u,t,l)

#ReciIma()

#----------------MOSTRAR LA INFORMACION DE MI TABLA informe

def ReciInfo(SOPP):
 cnx = mysql.connector.connect(user='PACS', password='DICOM1',
                               host='localhost',
                               database='dicom_pru')
# creacion dell cursor
 cursor = cnx.cursor()
 q=SOPP
 t= "'"+ q + "'"
#t= "'re.dcm'"
 y='WHERE NombrePaciente = '+ t
 sqlret= "SELECT * FROM informe "+y

 #print(y)
#sqlret= "SELECT * FROM imagenes2 WHERE address = 'aguzman86'"

 cursor.execute(sqlret)

#registro= cursor.fetchone()
 registro= cursor.fetchall()
#print(registro[0])
 u=[]
 for datos in registro:
     u.append(datos[1])


 #print(u[0])
 return()

#----------------ELIMINAR LA IIMAGEN DE MI TABLA DICOM

def ElimiInfo(numero):
 cnx = mysql.connector.connect(user='PACS', password='DICOM1',
                               host='localhost',
                               database='dicom_pru')
# creacion dell cursor
 cursor = cnx.cursor()
 q=numero
 t= "'"+ q + "'"
#t= "'re.dcm'"
 y='WHERE ID = '+ t
 sqlret= "delete FROM dicom "+y

 #print(y)
#sqlret= "SELECT * FROM imagenes2 WHERE address = 'aguzman86'"

 cursor.execute(sqlret)
 cnx.commit() #FORZAR EL GUARDADO DE LOS DATOS EN LA BD
 cursor.close()
 cnx.close()
 return()

#ElimiInfo('32')

#----------------ELIMINAR el informe DE MI TABLA informe2

def ElimiInforme(numero):
 cnx = mysql.connector.connect(user='PACS', password='DICOM1',
                               host='localhost',
                               database='dicom_pru')
# creacion dell cursor
 cursor = cnx.cursor()
 q=numero
 t= "'"+ q + "'"
#t= "'re.dcm'"
 y='WHERE NombrePaciente = '+ t
 sqlret= "delete FROM informe "+y

 #print(y)
#sqlret= "SELECT * FROM imagenes2 WHERE address = 'aguzman86'"

 cursor.execute(sqlret)
 cnx.commit() #FORZAR EL GUARDADO DE LOS DATOS EN LA BD
 cursor.close()
 cnx.close()
 return()

#ElimiInfo('32')
