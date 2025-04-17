# whois-status-alert

### The Problem

This project is a script to periodically check a domain's status. 

There is a domain I would like, however it currently has the following bizarre statuses. 

'''
  Domain Status: DeleteProhibited
  Domain Status: Hold
  Domain Status: Locked
  Domain Status: RegistrantTransferProhibited
'''

this is because it is locked due to its involvement in multiple romanian court cases. 
I would like to know when it frees up, but a lot of domain brokers do not truck in .ro domains.

So I build this myself.

### The Solution

TODO: detail. 

TODO: This code will evolve over time to be hosted on AWS and ultimately alert via text

### security concerns

Even though the log of the last time the whois was queried is not public facing and it's highly unlikely to be tampered with, we've opted not to use pickle as quoting from python's docs here: https://docs.python.org/3/library/pickle.html

> Warning
> The pickle module is not secure. Only unpickle data you trust.
> It is possible to construct malicious pickle data which will execute arbitrary code during unpickling. Never unpickle data that could have come from an untrusted  source, or that could have been tampered with.
> Consider signing data with hmac if you need to ensure that it has not been tampered with.
> Safer serialization formats such as json may be more appropriate if you are processing untrusted data. See Comparison with json.

as we only need to store a simple list, json will suffice. 