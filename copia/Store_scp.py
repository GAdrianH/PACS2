from pydicom.dataset import Dataset
from pynetdicom.sop_class import CTImageStorage
from pydicom.uid import UID
from pynetdicom import AE, evt
from pynetdicom import AE, debug_logger



#debug_logger()

def FnStoreScp():

# Implement a handler for evt.EVT_C_STORE
 def handle_store(event):
    """Handle a C-STORE request event."""
    # Decode the C-STORE request's *Data Set* parameter to a pydicom Dataset
    ds = event.dataset

    # Add the File Meta Information
    ds.file_meta = event.file_meta

    # Save the dataset using the SOP Instance UID as the filename
    ds.save_as(ds.SOPInstanceUID, write_like_original=False)

    # Return a 'Success' status
    return 0x0000

 handlers = [(evt.EVT_C_STORE, handle_store)]

# Initialise the Application Entity
 ae = AE()

# Support presentation contexts for all storage SOP Classes

 ae.add_supported_context('1.2.840.10008.5.1.4.1.1.2', transfer_syntax='1.2.840.10008.1.2.4.91')


# Start listening for incoming association requests
 ae.start_server(('', 11112), evt_handlers=handlers)


#FnStoreScp()
 
