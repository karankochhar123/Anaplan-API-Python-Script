# Anaplan-API-Python-Script
Simple Python Script which connects download and load data to Anaplan using Python and Anaplan Public API's

**Pre Requisite**

1- anaplan model design should be in place .

2- should be workspace admin to make api calls.

3- If you have SSO enabled then account which runs this sacript should be exception user . This is anaplan requirement



**Constant.Py** :- This file contains all variables used by main file . Please populate this before running the main program

eg 
  **ANAPLAN_USR** = "Enter your user name here"

  **ANAPLAN_PASS** = "Enter your password here"

  **ANAPLAN_IMPORT_FILE_NAME** = "This is the name of the output file eg data.csv"

  **ANAPLAN_LOADMODEL_WORKSPACEID** = "Enter the workspace id of the model where data is loaded. You can get this from anaplan"

  **ANAPLAN_LOADMODEL_MODELID** = "Enter model id of the model where data is loaded you can get this from anaplan"

  **ANAPLAN_LOADMODEL_FILEID** = "Enter file id of the upload file. To get this you can run get fileIds API call included in the script and then paste the value here"

  **ANAPLAN_PROCESSID** = "Enter process id which will run after file has been uplaoded.To get this you can run get processId API call included in the script and then paste the value here"

**Functions.Py**
This is where all functions are defined. run.py uses this to make call

**run.py**

This is the main file which calls all the functions in an order
