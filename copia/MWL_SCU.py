from pydicom.dataset import Dataset

from pynetdicom import AE, debug_logger
from pynetdicom.sop_class import ModalityWorklistInformationFind
from pynetdicom.sop_class import PatientRootQueryRetrieveInformationModelFind


#debug_logger()
def FnMwlScu(UID,nombre):

# Initialise the Application Entity
 ae = AE()
 u=0
# Add a requested presentation context
 ae.add_requested_context(ModalityWorklistInformationFind)


# Create our Identifier (query) dataset
 ds = Dataset()
 ds.PatientName = nombre
 ds.StudyInstanceUID = UID
 ds.StudyDate = '20070101'
 t=[]
#ds.ScheduledProcedureStepSequence = [Dataset()]
#item = ds.ScheduledProcedureStepSequence[0]
#item.ScheduledStationAETitle = b'PYNETDICOM'


 #print('ds:',ds)
 #print(ae)

# Associate with peer AE at IP 127.0.0.1 and port 11112
 assoc = ae.associate('127.0.0.1', 11140)

 if assoc.is_established:
    # Use the C-FIND service to send the identifier
    responses = assoc.send_c_find(ds, ModalityWorklistInformationFind)
    for (status, identifier) in responses:
        if status:
            print('C-FIND query status: 0x{0:04x}'.format(status.Status))
            t.append(identifier)
            u=u+1
            
        else:
            print('Connection timed out, was aborted or received invalid response')

    # Release the association
    
    assoc.release()
 else:
    print('Association rejected, aborted or never connected')

 #print('t:',t[0].SOPInstanceUID)
 
 t.append(u)


 return(str(u-1),t)

#[t1,u]= FnMwlScu('1.2.826.0.1.3680043.8.1055.1.20111102150758591.92402465.76095170','Luis')
#z=u[0].SOPInstanceUID
#z=str(z)
#print(t1)

