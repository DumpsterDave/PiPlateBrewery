# PiPlateBrewery
Brewery controller software for a Raspberry Pi coupled with a DAQC2 and THERMOplate from Pi-Plates.

# Configuration
You will need to create a conf.json or rename conf_template.json to conf.json file in the py folder on your device to utilize the Azure logging function.  Format of the file should be:
```
{	
    "WorkspaceId": "",	
    "WorkspaceKey": "",	
    "LogName": ""	
}
```
- WorkspaceId can be found in the Advanced Settings of your Log Analytics instance.  
- Workspace Key can be found in the same location and can be either the Primary or Secondary key.  
- Log Name is the name that entries will appear as once ingested into Log Analytics.  Log Analytics will automatically append '\_CL' to the end of the log name.
