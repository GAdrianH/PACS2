
from pydicom import dcmread

from pynetdicom import AE, debug_logger
from pynetdicom.sop_class import CTImageStorage

 #debug_logger()

def FnStoreScu(imagendcm,ipdcm):
# Initialise the Application Entity
 ae = AE()

# Add a requested presentation context
 ae.add_requested_context(CTImageStorage)
 ae.add_requested_context('1.2.840.10008.5.1.4.1.1.2', transfer_syntax='1.2.840.10008.1.2.4.91')

# Read in our DICOM CT dataset
 ds = dcmread(imagendcm)

# Associate with peer AE at IP 127.0.0.1 and port 11112
 assoc = ae.associate(ipdcm, 11112)
 if assoc.is_established:
    # Use the C-STORE service to send the dataset
    # returns the response status as a pydicom Dataset
     status = assoc.send_c_store(ds)

    # Check the status of the storage request
     if status:
        # If the storage request succeeded this will be 0x0000
         print('C-STORE request status: 0x{0:04x}'.format(status.Status))
         z='C-STORE request status: 0x0000'
     else:
         print('Connection timed out, was aborted or received invalid response')
         z='Connection timed out, was aborted or received invalid response'

    # Release the association
     assoc.release()
 else:
     print('Association rejected, aborted or never connected')
     z='Association rejected, aborted or never connected'
     
 return(z)

#y=input()
#x=input()
#FnStoreScu(y, x)
#t=FnStoreScu(y, x)
#print('t:',t)
