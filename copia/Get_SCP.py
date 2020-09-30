import os

from pydicom import dcmread
from pydicom.dataset import Dataset
from RecibirInfoMsql import FnInfoMsql

from pynetdicom import AE, StoragePresentationContexts, evt
from pynetdicom.sop_class import PatientRootQueryRetrieveInformationModelGet

def FnGetScp():
# Implement the handler for evt.EVT_C_GET
 def handle_get(event):
    """Handle a C-GET request event."""
    ds = event.identifier
    if 'QueryRetrieveLevel' not in ds:
        # Failure
         yield 0xC000, None
         return

    # Import stored SOP Instances
    instances = []
    matching = []
    instances = FnInfoMsql()
    #print(instances)

    if ds.QueryRetrieveLevel == 'STUDY':
     if ds.PatientName != '0':
             matching = [
                inst for inst in instances if inst.PatientName == ds.PatientName
             ]
     if ds.StudyInstanceUID != '0':
            matching = [
                inst for inst in instances if inst.StudyInstanceUID == ds.StudyInstanceUID
            ]

        # Skip the other possible attributes...

    # Skip the other QR levels...

    # Yield the total number of C-STORE sub-operations required
    yield len(instances)

    # Yield the matching instances
    for instance in matching:
         #print(instance)
        # Check if C-CANCEL has been received
         if event.is_cancelled:
             yield (0xFE00, None)
             return
         
         
        

        # Pending
         yield (0xFF00, instance)

 handlers = [(evt.EVT_C_GET, handle_get)]
 

# Create application entity
 ae = AE()

# Add the supported presentation contexts (Storage SCU)

 ae.add_supported_context('1.2.840.10008.5.1.4.1.1.2', transfer_syntax='1.2.840.10008.1.2.4.91')
 ae.add_supported_context('1.2.840.10008.5.1.4.1.1.2', transfer_syntax='1.2.840.10008.1.2')
 ae.add_requested_context('1.2.840.10008.5.1.4.1.1.2', transfer_syntax='1.2.840.10008.1.2')

# Accept the association requestor's proposed SCP role in the
#   SCP/SCU Role Selection Negotiation items
 for cx in ae.supported_contexts:
    cx.scp_role = True
    cx.scu_role = False

 # Add a supported presentation context (QR Get SCP)
 ae.add_supported_context(PatientRootQueryRetrieveInformationModelGet)
 ae.add_requested_context('1.2.840.10008.5.1.4.1.1.2', transfer_syntax='1.2.840.10008.1.2.4.91')


 #print(ae)
# Start listening for incoming association requests
 ae.start_server(('', 11120), evt_handlers=handlers)


#FnGetScp()

