from pynetdicom import AE, VerificationPresentationContexts

def FnEchoScp(llave=1):
    if llave == 1:
         ae = AE(ae_title=b'MY_ECHO_SCP')
# Or we can use the inbuilt VerificationPresentationContexts list,
#   there's one for each of the supported Service Classes
# In this case, we are supporting any requests to use Verification SOP
#   Class in the association
         ae.supported_contexts = VerificationPresentationContexts

# Start the SCP on (host, port) in blocking mode
         ae.start_server(('', 104), block=True)

#FnEchoScp()


    

    

