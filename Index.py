from Visualizar import visualiza
from flask import Flask, render_template, redirect, url_for, request
import os


from flask import Flask, render_template, request
from werkzeug.utils import secure_filename


import numpy as np
import cv2
import pydicom as dicom
from skimage import exposure


# -------------------------Importo los modulos de los servicios a utilizar ----------------------

from C_ECHO_SCP import FnEchoScp
from C_ECHO_SCU import FnEchoScu
from Store_scp import FnStoreScp
from Storescu import FnStoreScu
from Get_SCP import FnGetScp
from Get_SCU import FnGetScu
from FIND_scp import FnFindScp
from FIND_SCU import FnFindScu
from C_Move_SCP import FnMoveScp
from C_MOVE_SCU import FnMoveScu
from mwl_scp import FnMwlScp
from MWL_SCU import FnMwlScu


# -------------------------------------------InformesMySQL----------------------------------------

from traerinfo import EnvInfo, ReciInfo, EnvIma, ReciIma, ElimiInfo, ReciInforme, ElimiInforme
from Imatabla import MostraIma
UID = 0
NOM = 0
Utotal = 0


# ---------------------------------------------VIZUALISAR ------------------------------------------------

# -------------------------------------------------------------------------------------------------

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './Subir_imagen_DICOM'
# -------------------------------paginas de inicio--------------------------------------


@app.route('/')
def home():

    return render_template('portada.html')


# --------------------------------------Usuarios-----------------------------------------------------
@app.route('/Iniciar')
def Iniciar():
    if Utotal == "OK" or Utotal == "OKK":
      return render_template('Inicio.html')
    else:
      return render_template('bloqueo.html')
    

@app.route('/usuario', methods=['POST'])
def usuar():
    nom = request.form['usuarios']
    pas = request.form['Password']

    if (nom == "Total" and pas == "PACS") or (nom == "Parcial" and pas == "PACS"):
        globals().update({"Utotal": 'OK'})
        if nom == "Total" and pas == "PACS":
            globals().update({"Utotal": 'OKK'})
        return render_template('Inicio.html')

    else:
        globals().update({"Utotal": 'Fail'})
        return render_template('bloqueo.html')

    # return render_template("portada.html")

@app.route('/cerrar')
def cerrar():

    globals().update({"Utotal": 'Fail'})
    return render_template('portada.html')

# -----------------------------------ECHO-------------------------------------------------
@app.route('/echoScu')
def echoscu():
    if Utotal == "OK" or Utotal == "OKK":
      return render_template('echoscu.html')
    else:
      return render_template('bloqueo.html')


@app.route('/echoScp')
def echoscp():
    if Utotal == "OK" or Utotal == "OKK":
      return render_template('echoscp.html')
    else:
      return render_template('bloqueo.html')
    

# -----------------------------------STORE-------------------------------------------------


@app.route('/StoreScu')
def storescu():
    if Utotal == "OK" or Utotal == "OKK":
      return render_template('storescu.html')
    else:
      return render_template('bloqueo.html')
    


@app.route('/StoreScp')
def storescp():
    if Utotal == "OK" or Utotal == "OKK":
      return render_template('storescp.html')
    else:
      return render_template('bloqueo.html')
    

# -----------------------------------GET-------------------------------------------------


@app.route('/GetScu')
def getscu():
    if Utotal == "OK" or Utotal == "OKK":
      return render_template('getscu.html')
    else:
      return render_template('bloqueo.html')
    


@app.route('/GetScp')
def getscp():
    if Utotal == "OK" or Utotal == "OKK":
      return render_template('getscp.html')
    else:
      return render_template('bloqueo.html')
    

# -----------------------------------FIND-------------------------------------------------


@app.route('/FindScu')
def findscu():
    if Utotal == "OK" or Utotal == "OKK":
      return render_template('findscu.html')
    else:
      return render_template('bloqueo.html')
    


@app.route('/FindScp')
def findscp():
    if Utotal == "OK" or Utotal == "OKK":
      return render_template('findscp.html')
    else:
      return render_template('bloqueo.html')
    

# -----------------------------------MOVE-------------------------------------------------


@app.route('/MoveScu')
def movescu():
    if Utotal == "OK" or Utotal == "OKK":
      return render_template('movescu.html')
    else:
      return render_template('bloqueo.html')
    


@app.route('/MoveScp')
def movescp():
    if Utotal == "OK" or Utotal == "OKK":
      return render_template('movescp.html')
    else:
      return render_template('bloqueo.html')
    

# -----------------------------------MWL-------------------------------------------------


@app.route('/MwlScu')
def mwlscu():
    if Utotal == "OK" or Utotal == "OKK":
      return render_template('mwlscu.html')
    else:
      return render_template('bloqueo.html')
    


@app.route('/MwlScp')
def mwlscp():
    if Utotal == "OK" or Utotal == "OKK":
      return render_template('mwlscp.html')
    else:
      return render_template('bloqueo.html')
    


# --------------------------------IMAGEN------------------
@app.route('/imagen')
def imagen():
    if Utotal == "OK" or Utotal == "OKK":
      return render_template('pruebaiamge.html')
    else:
      return render_template('bloqueo.html')
    


@app.route('/imagenabrir')
def imagenabrir():
    # plt.close('all')
    [_, u] = FnMwlScu(UID, NOM)
    z = u[0].SOPInstanceUID
    z = str(z)
    #filename = z
    visualiza(z)

    return render_template("Inicio.html")


@app.route('/Ima1')
def Ima1():
    MostraIma(0)
    visualiza('Temporal_1.dcm')
    return(ImaMysql())


@app.route('/Ima2')
def Ima2():
    MostraIma(1)
    visualiza('Temporal_1.dcm')
    return(ImaMysql())


@app.route('/Ima3')
def Ima3():
    MostraIma(2)
    visualiza('Temporal_1.dcm')
    return(ImaMysql())


@app.route('/Ima4')
def Ima4():
    MostraIma(3)
    visualiza('Temporal_1.dcm')
    return (ImaMysql())
# -------------------------------------------INFORMES----------------------------


@app.route('/informe', methods=['POST'])
def informe():
    y = request.form['informe']
    [_, u] = FnMwlScu(UID, NOM)
    z = u[0].PatientName
    z = str(z)
    EnvInfo(z, y)
    return(InformeMysql())

# -------------------------------------------MySQL----------------------------


@app.route('/MySQl')
def ImaMysql():
    if Utotal == "OK" or Utotal == "OKK":
      u = ['--', '--', '--']
      t = ['--', '--', '--']
      [u, t, l] = ReciIma()
      return render_template('subirMysql.html', long=l, parametro1=u[0], parametro2=t[0], parametro3=u[1], parametro4=t[1], parametro5=u[2], parametro6=t[2], parametro7=u[3], parametro8=t[3])
    else:
      return render_template('bloqueo.html')
    

@app.route('/MySQl_subir', methods=['POST'])
def GuardarMysql():
    y = request.form['nombreDI']
    EnvIma(y)
    return (ImaMysql())

@app.route("/upload", methods=['POST'])
def uploader():
 if request.method == 'POST':
  # obtenemos el archivo del input "archivo"
  f = request.files['archivo']
  filename = secure_filename(f.filename)
  # Guardamos el archivo en el directorio "Archivos PDF"
  f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
  # Retornamos una respuesta satisfactoria
  EnvIma(filename)
#   visualiza(filename)
  return (ImaMysql())


@app.route('/MySQl_eliminar', methods=['POST'])
def EliminaMysql():
    if Utotal == "OKK":
     y = request.form['numeroDI']
     ElimiInfo(y)
     return (ImaMysql())
    else:
      return render_template('bloqueo.html')



@app.route('/MySQl_Informe')
def InformeMysql():
    if Utotal == "OK" or Utotal == "OKK":
     u = ['--', '--', '--']
     t = ['--', '--', '--']
     [u, t, l] = ReciInforme()
     return render_template('verinfor.html', long=l, parametro1=u[0], parametro2=t[0], parametro3=u[1], parametro4=t[1], parametro5=u[2], parametro6=t[2], parametro7=u[3], parametro8=t[3])
    else:
     return render_template('bloqueo.html')



@app.route('/MySQl_Informe_eliminar', methods=['POST'])
def InformeEliminaMysql():
    if Utotal == "OKK":
      y = request.form['numeroDI']
      ElimiInforme(y)
      return (InformeMysql())
    else:
      return render_template('bloqueo.html')



# _----------------------------------------------------------------------------------------
# --------------------------Se ejecutan los servicios---------------------------------------
# -----------------------------------------------------------------------------------------

# -------------------------- C-ECHO SOLO PARA EL SCP-------------------------------------

@app.route('/echoScp_ejecutando')
def echoss():

    FnEchoScp()
    # os.system('C:/Users/user/Desktop/HTML/PaginaDicom/static/ECHO/scp/C-ECHO_SCP.py')
    return render_template("layout.html", mensaje='Se termino de escuchar')


# -------------------------- C-ECHO SOLO PARA EL SCU-------------------------------------
@app.route('/echoScu_ejecutando')
def echosr():
    x = FnEchoScu()
    if x == 'Se termino el codigo y no se asocio':
        parametro = 'Porfavor revisar si el SCP se encuentra esuchando'
    else:
        parametro = 'Se realizo correctameente la asociacion'
    # os.system('C:/Users/user/Desktop/HTML/PaginaDicom/static/ECHO/scu/C-ECHO_SCU.py')
    return render_template('respuesta.html', solucion=x, parametro1=parametro)


# -------------------------- C-STORE SOLO PARA EL SCP-------------------------------------

@app.route('/storeScp_ejecutando')
def storesx():

    FnStoreScp()
    #os.system('taskkill /F /IM python.exe')
    return()


# -------------------------- C-STORE SOLO PARA EL SCU-------------------------------------
@app.route('/storeScu_ejecutando', methods=['POST'])
def storesr():
    nombredcm1 = request.form['nombredcm']
    ipdcm = request.form['dcmip']
    t = FnStoreScu(nombredcm1, ipdcm)
    if t == 'C-STORE request status: 0x0000':
        parametro = 'Se realizo correctameente la asociacion y el envio de la imagen'
    else:
        parametro = 'Porfavor revisar si el SCP se encuentra esuchando y si el nombre y el ip son correctos'
        #os.system('taskkill /F /IM python.exe')
    return render_template('respuesta.html', solucion=t, parametro1=parametro)

# -------------------------- C-GET SOLO PARA EL SCP-------------------------------------


@app.route('/getScp_ejecutando')
def getsx():

    FnGetScp()
    #os.system('taskkill /F /IM python.exe')
    return()


# -------------------------- C-GET SOLO PARA EL SCU-------------------------------------


@app.route('/getScu_ejecutando', methods=['POST'])
def getsr():
    ip = request.form['idpaci']
    nombrepaci = request.form['nombrepaci']
    globals().update({"UID": ip})
    globals().update({"NOM": nombrepaci})
    t = FnGetScu(ip, nombrepaci)
    [_, u] = FnMwlScu(ip, nombrepaci)
    if t == '0':
        parametro = 'Ninguna de las imagenes en la base de datos corresponde a la informacion de referencia'
        r = 'C-GET request status: 0x0000'
        return render_template('respuesta.html', solucion=r, parametro1=parametro)
    if t == 't':
        parametro = 'Porfavor revisar si el SCP se encuentra esuchando'
        r = 'Association rejected, aborted or never connected'
        return render_template('respuesta.html', solucion=r, parametro1=parametro)
    else:
        parametro = 'Se realizo correctameente la asociacion y se encontraron ' + \
            t+' imagenes con la informacion que usted suministro'
        r = 'C-GET request status: 0x0000'
        return render_template('respuesta2.html', solucion=r, parametro1=parametro, parametro2=u[0].PatientName, parametro3=u[0].Modality, parametro4=u[0].StudyDate, parametro5=u[0].ProtocolName, parametro6=u[0].StudyDescription)


# -------------------------- C-FIND SOLO PARA EL SCP-------------------------------------

@app.route('/findScp_ejecutando')
def findsx():

    FnFindScp()
    #os.system('taskkill /F /IM python.exe')
    return()


# -------------------------- C-FIND SOLO PARA EL SCU-------------------------------------


@app.route('/findScu_ejecutando', methods=['POST'])
def findsr():
    nombrepac = request.form['nombrepaci']
    [t1, u] = FnFindScu(nombrepac)
    if t1 == '0':
        parametro = 'Ninguna de las imagenes en la base de datos corresponde a la informacion de referencia'
        r = 'C-GET request status: 0x0000'
        return render_template('respuesta.html', solucion=r, parametro1=parametro)
    if t1 == '-1':
        parametro = 'Porfavor revisar si el SCP se encuentra esuchando'
        r = 'Association rejected, aborted or never connected'
        return render_template('respuesta.html', solucion=r, parametro1=parametro)
    else:
        parametro = 'Se realizo correctameente la asociacion y se encontraron ' + \
            t1+' imagenes con la informacion que usted suministro'
        r = 'C-GET request status: 0x0000'
        return render_template('respuesta3.html', solucion=r, parametro1=parametro, parametro2=u[0].PatientName, parametro3=u[0].Modality, parametro4=u[0].StudyDate, parametro5=u[0].ProtocolName, parametro6=u[0].StudyDescription)


# -------------------------- C-MOVE SOLO PARA EL SCP-------------------------------------

@app.route('/moveScp_ejecutando')
def movesx():

    FnMoveScp()
    #os.system('taskkill /F /IM python.exe')
    return()


# -------------------------- C-MOVE SOLO PARA EL SCU-------------------------------------


@app.route('/moveScu_ejecutando', methods=['POST'])
def movesr():
    nombrepaci1 = request.form['nombrepaci']
    uid1 = request.form['UID2']
    globals().update({"UID": uid1})
    globals().update({"NOM": nombrepaci1})
    [_, u] = FnMwlScu(uid1, nombrepaci1)
    t = FnMoveScu(uid1, nombrepaci1)
    if t == '0':
        parametro = 'Ninguna de las imagenes en la base de datos corresponde a la informacion de referencia'
        r = 'C-GET request status: 0x0000'
        return render_template('respuesta.html', solucion=r, parametro1=parametro)
    if t == 't':
        parametro = 'Porfavor revisar si el SCP se encuentra esuchando'
        r = 'Association rejected, aborted or never connected'
        return render_template('respuesta.html', solucion=r, parametro1=parametro)
    else:
        parametro = 'Se realizo correctameente la asociacion y se encontraron ' + \
            t+' imagenes con la informacion que usted suministro'
        r = 'C-GET request status: 0x0000'
        return render_template('respuesta2.html', solucion=r, parametro1=parametro, parametro2=u[0].PatientName, parametro3=u[0].Modality, parametro4=u[0].StudyDate, parametro5=u[0].ProtocolName, parametro6=u[0].StudyDescription)


# -------------------------- C-MWL SOLO PARA EL SCP-------------------------------------

@app.route('/mwlScp_ejecutando')
def mwlsx():

    FnMwlScp()
    #os.system('taskkill /F /IM python.exe')
    return()


# -------------------------- C-MWL SOLO PARA EL SCU-------------------------------------


@app.route('/mwlScu_ejecutando', methods=['POST'])
def mwlsr():
    modalidad = request.form['modalidad']
    nombrepaci = request.form['nombrepaci']
    [t1, u] = FnMwlScu(modalidad, nombrepaci)
    if t1 == '0':
        parametro = 'Ninguna de las imagenes en la base de datos corresponde a la informacion de referencia'
        r = 'C-GET request status: 0x0000'
        return render_template('respuesta.html', solucion=r, parametro1=parametro)
    if t1 == '-1':
        parametro = 'Porfavor revisar si el SCP se encuentra esuchando'
        r = 'Association rejected, aborted or never connected'
        return render_template('respuesta.html', solucion=r, parametro1=parametro)
    else:
        parametro = 'Se realizo correctameente la asociacion y se encontraron ' + \
            t1+' imagenes con la informacion que usted suministro'
        r = 'C-GET request status: 0x0000'
        return render_template('respuesta3.html', solucion=r, parametro1=parametro, parametro2=u[0].PatientName, parametro3=u[0].Modality, parametro4=u[0].StudyDate, parametro5=u[0].ProtocolName, parametro6=u[0].StudyDescription)


if __name__ == '__main__':
    app.run(debug=True)
