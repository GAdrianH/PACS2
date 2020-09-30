from pydicom.dataset import Dataset

from pynetdicom import AE, evt, build_role, debug_logger
from pynetdicom.sop_class import (
    PatientRootQueryRetrieveInformationModelGet,
    CTImageStorage
)

#debug_logger()

def FnGetScu(UID,nombre):
 q='t'
# Implement the handler for evt.EVT_C_STORE
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

# Add the requested presentation contexts (QR SCU)
 ae.add_requested_context(PatientRootQueryRetrieveInformationModelGet)
# Add the requested presentation context (Storage SCP)
 ae.add_requested_context('1.2.840.10008.5.1.4.1.1.2', transfer_syntax='1.2.840.10008.1.2.4.91')
 ae.add_supported_context('1.2.840.10008.5.1.4.1.1.2', transfer_syntax='1.2.840.10008.1.2')
 ae.add_requested_context('1.2.840.10008.5.1.4.1.1.2', transfer_syntax='1.2.840.10008.1.2')

 #print(ae)
# Create an SCP/SCU Role Selection Negotiation item for CT Image Storage
 role = build_role(CTImageStorage, scp_role=True)

# Create our Identifier (query) dataset
# We need to supply a Unique Key Attribute for each level above the
#   Query/Retrieve level
 ds = Dataset()
 ds.QueryRetrieveLevel = 'STUDY'
 ds.StudyInstanceUID = UID
 ds.PatientID = '0'
 ds.Modality = 'CT'
 #ds.StudyInstanceUID ='1.2.826.0.1.3680043.8.1055.1.20111102150758591.92402465.76095170'
 ds.PatientName = nombre
 

# Associate with peer AE at IP 127.0.0.1 and port 11112
 assoc = ae.associate('127.0.0.1', 11120, ext_neg=[role], evt_handlers=handlers)

 if assoc.is_established:
    # Use the C-GET service to send the identifier
     responses = assoc.send_c_get(ds, PatientRootQueryRetrieveInformationModelGet)
     for (status, identifier) in responses:
         if status:
             print('C-GET query status: 0x{0:04x}'.format(status.Status))
             #print(status)
             q= status.NumberOfCompletedSuboperations
             q=str(q)
             #print('id:',identifier)
         else:
             print('Connection timed out, was aborted or received invalid response')

    # Release the association
     #q.append(status.NumberOfCompletedSuboperations)
     assoc.release()
 else:
     print('Association rejected, aborted or never connected')
     
     
 return(q)

#t= '1.2.826.0.1.3680043.8.1055.1.20170626100116652.756727516.6235062'
#r=FnGetScu(t)
#print('q:',r)


