import os, pydicom, mysql.connector
from os import remove
from pydicom import dcmread

def MostraIma(numero): 

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
 tr=resultados[numero]
 #print(tr[0])
 file= open('Temporal_1.dcm','wb')
 file.write(tr[1])
 file.close

 return()

#MostraIma()
