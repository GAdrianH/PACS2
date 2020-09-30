import os

from pydicom import dcmread
from pydicom.dataset import Dataset
from RecibirInfoMsql import FnInfoMsql

from pynetdicom import AE, evt
from pynetdicom.sop_class import ModalityWorklistInformationFind

def FnMwlScp():

 # Implement the handler for evt.EVT_C_FIND
 def handle_find(event):
     """Handle a C-FIND request event."""
     ds = event.identifier
     #print(ds)

     # Import stored SOP Instances
     instances = []
     instances = FnInfoMsql()
     matching = []
     


     #if 'QueryRetrieveLevel' not in ds:
         # Failure
      #   yield 0xC000, None
       #  return

    
     if ds.PatientName != '0':
             matching = [
                inst for inst in instances if inst.PatientName == ds.PatientName
             ]
     if ds.StudyInstanceUID != '0':
            matching = [
                inst for inst in instances if inst.StudyInstanceUID == ds.StudyInstanceUID
            ]


    
               #  print('matching:',matching)
                 

             # Skip the other possibile values...

         # Skip the other possible attributes...

     # Skip the other QR levels...

     for instance in matching:
         # Check if C-CANCEL has been received
         if event.is_cancelled:
             yield (0xFE00, None)
             return

         identifier = Dataset()
         identifier.PatientName = instance.PatientName
         identifier.Modality = instance.Modality
         identifier.StudyDate = ds.StudyDate
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
 ae.add_supported_context(ModalityWorklistInformationFind)
# print (ae)
 ae.title=b'ANY-SCP'
#print (ae)
# Start listening for incoming association requests
 ae.start_server(('', 11140), evt_handlers=handlers)


#FnMwlScp()
