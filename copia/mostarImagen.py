from matplotlib import pylab
import matplotlib.pyplot as plt
import pydicom
import sys


def Imagen(Nom):
    dataset = pydicom.dcmread(Nom)
    plt.imshow(dataset.pixel_array, cmap=plt.cm.bone)
    #plt.imshow(dataset.pixel_array)
    plt.show()
    return()



#Imagen(1,'Paciente1.dcm')

