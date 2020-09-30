import os

from RecibirInfoMsql import FnInfoMsql

from pydicom import dcmread
from pydicom.dataset import Dataset

from pynetdicom import AE, evt
from pynetdicom.sop_class import PatientRootQueryRetrieveInformationModelFind

def FnFindScp():

 # Implement the handler for evt.EVT_C_FIND
 def handle_find(event):
     """Handle a C-FIND request event."""
     ds = event.identifier

     # Import stored SOP Instances
     instances = []
     
     #Función para recibir información de MySQL
     instances = FnInfoMsql()
     
     if 'QueryRetrieveLevel' not in ds:
         # Failure
         yield 0xC000, None
         return

     if ds.QueryRetrieveLevel == 'PATIENT':
         if 'PatientName' in ds:
             if ds.PatientName not in ['*', '', '?']:
                 matching = [
                     inst for inst in instances if inst.PatientName == ds.PatientName
                 ]

             # Skip the other possibile values...

         # Skip the other possible attributes...

     # Skip the other QR levels...

     for instance in matching:
         # Check if C-CANCEL has been received
         if event.is_cancelled:
             yield (0xFE00, None)
             return
         #print('instanciaaaaaaaaaaaa', instance)
         #print('matttchiiiii', matching)
         identifier = Dataset()
         identifier.PatientName = instance.PatientName
         identifier.Modality = instance.Modality
         identifier.StudyDate = instance.StudyDate
         #print('inst:',instance.SOPInstanceUID)
         identifier.SOPInstanceUID = instance.SOPInstanceUID
         identifier.SeriesDescription = instance.SeriesDescription
         identifier.ProtocolName = instance.ProtocolName
         identifier.StudyDescription = instance.StudyDescription

         # Pending
         yield (0xFF00, identifier)


 handlers = [(evt.EVT_C_FIND, handle_find)]

# Initialise the Application Entity and specify the listen port
 ae = AE()

# Add the supported presentation context
 ae.add_supported_context(PatientRootQueryRetrieveInformationModelFind)
# print(ae)

# Start listening for incoming association requests
 ae.start_server(('', 11130), evt_handlers=handlers)


#FnFindScp()
