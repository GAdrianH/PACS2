from pydicom.dataset import Dataset

from pynetdicom import AE, evt, StoragePresentationContexts
from pynetdicom.sop_class import PatientRootQueryRetrieveInformationModelMove
from pynetdicom.sop_class import CTImageStorage

def FnMoveScu(UID,nombre):
 q='t'
 def handle_store(event):
    """Handle a C-STORE request event."""
    ds = event.dataset
    ds.file_meta = event.file_meta

    # Save the dataset using the SOP Instance UID as the filename
    ds.save_as(ds.SOPInstanceUID, write_like_original=False)

    # Return a 'Success' status
    return 0x0000

 handlers = [(evt.EVT_C_STORE, handle_store)]

# Initialise the Application Entity
 ae = AE()

# Add a requested presentation context
 ae.add_requested_context(PatientRootQueryRetrieveInformationModelMove)
#ae.add_requested_context(CTImageStorage)

# Add the Storage SCP's supported presentation contexts
 ae.supported_contexts = StoragePresentationContexts
 ae.add_requested_context('1.2.840.10008.5.1.4.1.1.2', transfer_syntax='1.2.840.10008.1.2.4.91')
 ae.add_supported_context('1.2.840.10008.5.1.4.1.1.2', transfer_syntax='1.2.840.10008.1.2.4.91')

# Start our Storage SCP in non-blocking mode, listening on port 104
 ae.ae_title = b'OUR_STORE_SCP'
 #print('---- ae -------')
 #print(ae)
 scp = ae.start_server(('', 11120), block=False, evt_handlers=handlers)

# Create out identifier (query) dataset
 ds = Dataset()
 ds.QueryRetrieveLevel = 'STUDY'
#ds.PatientID = '0'
 ds.StudyInstanceUID = UID
 ds.PatientName = nombre
#ds.SOPInstanceUID = '1.2.826.0.1.3680043.8.1055.1.20111102150758825.42401392.26682309'

# Associate with peer AE 
 assoc = ae.associate('127.0.0.1', 11112)

 if assoc.is_established:
    # Use the C-MOVE service to send the identifier
    responses = assoc.send_c_move(ds, b'OUR_STORE_SCP', PatientRootQueryRetrieveInformationModelMove)
    
    for (status, identifier) in responses:
        if status:
            print('C-MOVE query status: 0x{0:04x}'.format(status.Status))
            #print(status.NumberOfCompletedSuboperations)
            q= status.NumberOfCompletedSuboperations
            q=str(q)
            #print('iden:',identifier)
            #print('status',status)

            # If the status is 'Pending' then `identifier` is the C-MOVE response

        else:
            print('Se agotó el tiempo de conexión, se canceló o recibió una respuesta no válida')

    # Release the association
    assoc.release()
 else:
    print('Asociación rechazada, abortada o nunca conectada')

# Stop our Storage SCP
#scp.shutdown()

 return(q)

#r=FnMoveScu('1.2.826.0.1.3680043.8.1055.1.20111102150758591.92402465.76095170','Luis')
#r=FnMoveScu('1.2.840.113619.2.55.3.4271045733.996.1449464144.595')

#print('q:',r)

