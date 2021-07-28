'''
This file contains all the functions required by main program

'''
import constants as cons
import requests
import json
from base64 import b64encode

# Function to authenticate ( Basic ) and getting token value 

def getToken():
    username = cons.ANAPLAN_USR
    password = cons.ANAPLAN_PASS
    
    header_string = { 'Authorization':'Basic ' + b64encode((username + ":" + password).encode('utf-8')).decode('utf-8') }
    anaplan_url='https://auth.anaplan.com/token/authenticate'

    print('getting Token')

    r=requests.post(anaplan_url, headers=header_string)

    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("Error: " + str(e))
        exit()

    resp_dict = json.loads(r.text)
    return resp_dict['tokenInfo']['tokenValue']
  
 
# Function to get list of workspaces
# t is token value

def getWorkspaces(t):

    workspace_url = 'https://api.anaplan.com/2/0/workspaces/?tenantDetails=true'
    header = {'Authorization':'AnaplanAuthToken ' + t}
    r = requests.get(workspace_url,headers=header)

    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("Error: " + str(e))
        exit()

    return r.json()

# Function to get list of model
# t is token value

def getModel(t):
    
    model_url = 'https://api.anaplan.com/2/0/models/?modelDetails=True'
    model_header = {'Authorization':'AnaplanAuthToken ' + t}
    r = requests.get(model_url, headers=model_header)
    
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("Error: " + str(e))
        exit()
    
    return r.json()

#function to upload data file to anaplan server
# wId = workspace id , mID = model ID , fID = import file ID , fName = Upload file name , t = token value

def uploadFile(wID,mID,fID,fName,t):

    upload_url = 'https://api.anaplan.com/2/0/workspaces/'+wID+'/models/'+mID+'/files/'+fID
    header = {'Authorization':'AnaplanAuthToken ' + t,'Content-Type':'application/octet-stream'}
    dataFile = open(fName, 'r').read().encode('utf-8')
    r = requests.put(upload_url, headers= header,data=dataFile)
    if r.status_code == 204:
        print("File uploaded")
    else:
        print('Something went wrong')
        exit()

#Function to get process Id's for a model
#wId = workspace id , mID = model ID ,  t = token value)

def getProcess(wID,mID,t):

    getprocess_url = 'https://api.anaplan.com/2/0/workspaces/'+wID+'/models/'+mID+'/processes/'
    header = {'Authorization':'AnaplanAuthToken ' + t,'Content-Type':'application/json'}
    r = requests.get(getprocess_url, headers= header)
    print(r.json())

#Function to run a process
#wId = workspace id , mID = model ID , pID = process to run ID ,  t = token value)

def runProcess(wID,mID,pID,t):

    runprocess_url = 'https://api.anaplan.com/2/0/workspaces/'+wID+'/models/'+mID+'/processes/'+pID+'/tasks'
    header = {'Authorization':'AnaplanAuthToken ' + t,'Content-Type':'application/json'}
    data = '{"localeName": "en_US"}'
    r = requests.post(runprocess_url, headers= header,data=data)

    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("Error: " + str(e))
        exit()
    
    
    taskid = r.json()['task']['taskId']

    taskState = 'NOT_STARTED'
    count = 1
    while taskState != 'COMPLETE' and count<=10:

        print('running task request number '+str(count))

        r = requests.get(runprocess_url + '/'+taskid, headers= header,)

        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print("Error: " + str(e))
            exit()

        taskState = r.json()['task']['taskState']
        failureDumpAvailable = r.json()['task']['result']['failureDumpAvailable']
        count +=1
    
    print('Process status '+taskState +' Failure dumps available '+str(failureDumpAvailable))


#Function to get all fileids for a model
#wId = workspace id , mID = model ID, t = token value

def getFileIds(wID,mID,t):

    getFileIds_url = 'https://api.anaplan.com/2/0/workspaces/'+wID+'/models/'+mID+'/files'
    header = {'Authorization':'AnaplanAuthToken ' + t,'Accept':'application/json'}
    r = requests.get(getFileIds_url, headers= header)

    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("Error: " + str(e))
        exit()
    
    print(r.json())
    #use below to print in nice format
    #print(r.json(),indent=4) 


#function to get all line items for a model
#mID = model ID, t = token value

def getAlllineitems(mID,t):
    getalllineitems_url = 'https://api.anaplan.com/2/0/models/'+mID+'/lineItems'
    header = {'Authorization':'AnaplanAuthToken ' + t,'Accept':'application/json','Content-Type': 'application/json'}
    r = requests.get(getalllineitems_url, headers= header)

    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("Error: " + str(e))
        exit()
    
    print(r.json())
    #use below to print in nice format
    #print(r.json(),indent=4) 


def getLists(wID,mID,t):

    getlists_url = 'https://api.anaplan.com/2/0/workspaces/'+wID+'/models/'+mID+'/lists'
    header = {'Authorization':'AnaplanAuthToken ' + t,'Accept':'application/json'}
    r = requests.get(getlists_url, headers= header)

    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("Error: " + str(e))
        exit()
    print(r.json())
    #use below to print in nice format
    #print(r.json(),indent=4)

def getmoduleID(mID,t):
    module_url = 'https://api.anaplan.com/2/0/models/'+mID+'/modules'
    header = {'Authorization':'AnaplanAuthToken ' + t,'Accept':'application/json'}
    r = requests.get(module_url, headers= header)

    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("Error: " + str(e))
        exit()
    
    print(r.json())
    #use below to print in nice format
    #print(r.json(),indent=4)