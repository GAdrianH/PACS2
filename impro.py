from flask import Flask, render_template, redirect, url_for, request
import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

from Visualizar import visualiza

from traerinfo import EnvInfo, ReciInfo, EnvIma, ReciIma, ElimiInfo, ReciInforme, ElimiInforme
from Imatabla import MostraIma

# app = Flask(__name__)


# @app.route('/')
# def home():

#     return render_template("prueba.html")


# # @app.route('/subir', methods=['POST'])
# # def subir():
# #     pas = request.form['archivo']
# #     file= open('subir.dcm','wb')
# #     pas=bytes(pas)
# #     file.write(pas)
# #     file.close
# #     return ('ya')



# instancia del objeto Flask
app = Flask(__name__)
# Carpeta de subida
app.config['UPLOAD_FOLDER'] = './Subir_imagen_DICOM'

@app.route("/")
def upload_file():
 # renderiamos la plantilla "formulario.html"
 return render_template('prueba.html')

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
  return (filename)








@app.route('/usuario', methods=['POST'])
def usuar():
    nom = request.form['usuarios']
    pas = request.form['Password']

    if nom == "Total" and pas == "PACS":
        return('entro')

    else:
        return('incorrecto')

    # return render_template("portada.html")


if __name__ == '__main__':
    app.run(debug=True)
