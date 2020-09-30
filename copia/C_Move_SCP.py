import os

from pydicom import dcmread
from pydicom.dataset import Dataset
from RecibirInfoMsql import FnInfoMsql

from pynetdicom import AE, StoragePresentationContexts, evt
from pynetdicom.sop_class import CTImageStorage
from pynetdicom.sop_class import PatientRootQueryRetrieveInformationModelMove

def FnMoveScp():

# Implement the evt.EVT_C_MOVE handler
 def handle_move(event):
    """Handle a C-MOVE request event."""
    ds = event.identifier

    if 'QueryRetrieveLevel' not in ds:
        # Failure
        yield 0xC000, None
        return

    #yield '127.0.0.1', 11120 
    
    known_aet_dict ={"addr":'127.0.0.1', "port":11120}
    #print (known_aet_dict)
    
   
    #addr1=known_aet_dict.get("addr")
    #port1=known_aet_dict.get("port")

    (addr1, port1)=known_aet_dict.values()
    #print ("addr1= ",addr1)
    #print ('port1= ',port1)

    # Yield the IP address and listen port of the destination AE

    yield addr1, port1
    

    
    # Import stored SOP Instances
    instances = []
    matching = []
    instances = FnInfoMsql()
    
    if ds.QueryRetrieveLevel == 'STUDY':
        if ds.PatientName != '0':
             matching = [
                inst for inst in instances if inst.PatientName == ds.PatientName
             ]
        if ds.StudyInstanceUID != '0':
            matching = [
                inst for inst in instances if inst.StudyInstanceUID == ds.StudyInstanceUID
            ]


    # Skip the other QR levels...

    #print('Instances')
    #print(instances)
    # Yield the total number of C-STORE sub-operations required
    yield len(matching)
    # Yield the matching instances
    for instance in matching:
        # Check if C-CANCEL has been received
        if event.is_cancelled:
            yield (0xFE00, None)
            return

        # Pending
        yield (0xFF00, instance)


 handlers = [(evt.EVT_C_MOVE, handle_move)]

# Create application entity
 ae = AE()

# Add the requested presentation contexts (Storage SCU)
#ae.requested_contexts = StoragePresentationContexts
 ae.add_supported_context('1.2.840.10008.5.1.4.1.1.2', transfer_syntax='1.2.840.10008.1.2.4.91')
 ae.add_requested_context('1.2.840.10008.5.1.4.1.1.2', transfer_syntax='1.2.840.10008.1.2.4.91')
#ae.add_requested_context(CTImageStorage)
# Add a supported presentation context (QR Move SCP)
 ae.add_supported_context(PatientRootQueryRetrieveInformationModelMove)
#print('---- ae -------')
 #print(ae)
# Start listening for incoming association requests
 ae.start_server(('', 11112), evt_handlers=handlers)

#FnMoveScp()
