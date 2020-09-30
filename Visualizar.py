import numpy as np
import cv2
import pydicom as dicom
from skimage import exposure


def visualiza(nombre):
 #nombre= './Subir_imagen_DICOM/' + nombre
 ds=dicom.dcmread(nombre)
 dcm_sample=ds.pixel_array
 dcm_sample=exposure.equalize_adapthist(dcm_sample)
 cv2.imshow('Visualizador PACS',dcm_sample)
 cv2.waitKey()
 return()

#visualiza('2.dcm')
