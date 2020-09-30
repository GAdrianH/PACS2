
from pydicom.dataset import Dataset

from pynetdicom import AE, debug_logger
from pynetdicom.sop_class import PatientRootQueryRetrieveInformationModelFind

#debug_logger()

def FnFindScu(nombrepac):
    
# Initialise the Application Entity
 u=0
 ae = AE()
# Add a requested presentation context
 ae.add_requested_context(PatientRootQueryRetrieveInformationModelFind)
 #print(ae)
# Create our Identifier (query) dataset
 ds = Dataset()
 ds.PatientName = nombrepac
 ds.QueryRetrieveLevel = 'PATIENT'
 t=[]
# Associate with peer AE at IP 127.0.0.1 and port 11112
 assoc = ae.associate('127.0.0.1', 11130)

 if assoc.is_established:
    # Use the C-FIND service to send the identifier
    responses = assoc.send_c_find(ds, PatientRootQueryRetrieveInformationModelFind)

    for (status, identifier) in responses:
        if status:
            print('C-FIND query status: 0x{0:04x}'.format(status.Status))
            #print(status)
            #q= status.NumberOfCompletedSuboperations
            #q=str(q)
            t.append(identifier)
            u=u+1

            # If the status is 'Pending' then identifier is the C-FIND response
           # if status.Status in (0xFF00, 0xFF01):
            #    print('t',identifier)
        else:
            print('Connection timed out, was aborted or received invalid response')

     # Release the association
    assoc.release()
 else:
    print('Association rejected, aborted or never connected')
    
 t.append(u)
 return(str(u-1),t)

#[t2,u]=FnFindScu('Anonymized')
#z=u[0].SOPInstanceUID
#z=str(z)
#print('q:',t2)
