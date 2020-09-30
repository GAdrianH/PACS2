import os, pydicom, mysql.connector
from os import remove
from pydicom import dcmread

def FnInfoMsql(): 

 #conexión con MSQL 
 cnx = mysql.connector.connect(user='PACS', password='DICOM1',
                              host='localhost',
                              database='dicom_pru') 
 # creacion dell cursor
 cursor = cnx.cursor()

 sqlret= "select * from dicom"
 cursor.execute(sqlret)

 resultados = cursor.fetchall() 
 i=0

 contenido=[]
 for datos1 in resultados:
    file= open('Temporal_2.dcm','wb')
    file.write(datos1[1])
    file.close
    y = dcmread('Temporal_2.dcm')
    contenido.append(y)
    
 return(contenido)


