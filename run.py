'''
This is the main file which runs and calls all functions.
All functions are defined in functions.py
All constants are specified in constants.py

'''

import constants as cons
import functions as anaplan
import pandas as pd
from datetime import datetime

#This function contains the flow logic . It calls functions from function.py in order highlighted below
def run():
    
    #STEP 1 :- Authentication to get Auth Token
    token = anaplan.getToken()

    #STEP 2 :- Get all workspaces user has access to and save in dataframe
    workspaces_response = anaplan.getWorkspaces(token)

    #Saving workspace data in dataframe
    workspace_df = pd.DataFrame(workspaces_response['workspaces'])
    print('Workspace dataframe populated')

    #Step 3 :- Get all models user has access to and save in dataframe
    models_response = anaplan.getModel(token)

    #Filtering out non-active(non archived) models.Only active models contribute towards space
    active_models = [a for a in models_response['models'] if a['activeState'] != 'ARCHIVED']

    #Saving model data in dataframe
    models_df =pd.DataFrame(active_models)
    print('Model dataframe populated')

    #STEP 4 : Merging and Saving file which will be loaded into anaplan
    
    #Merging workspace dataframe and model dataframe to create one output
    output_df = pd.merge(models_df,workspace_df[['id','active','sizeAllowance','currentSize']],left_on='currentWorkspaceId', right_on='id')
    
    #Adding Line ID column to begining 
    output_df.insert(0,'Line_ID','#'+(models_df.index+1).astype(str))

    #Adding todays date column 
    output_df['load_date']= datetime.today().strftime('%Y-%m-%d')

    #Saving csv
    output_df.to_csv(cons.ANAPLAN_IMPORT_FILE_NAME,index=False)
    print('File '+cons.ANAPLAN_IMPORT_FILE_NAME+' saved')

    #STEP 5 : Upload data file to anaplan
    anaplan.uploadFile(cons.ANAPLAN_LOADMODEL_WORKSPACEID,cons.ANAPLAN_LOADMODEL_MODELID,cons.ANAPLAN_LOADMODEL_FILEID,cons.ANAPLAN_IMPORT_FILE_NAME,token)

    #STEP 6 : Run Import Process
    anaplan.runProcess(cons.ANAPLAN_LOADMODEL_WORKSPACEID,cons.ANAPLAN_LOADMODEL_MODELID,cons.ANAPLAN_PROCESSID,token)

    # OTHER API CALLS
    # you can run these calls to get file id's , process id's etc 

    #Get list of processes for a model
    #anaplan.getProcess(cons.ANAPLAN_LOADMODEL_WORKSPACEID,cons.ANAPLAN_LOADMODEL_MODELID,token)

    #Get all files for a model
    #anaplan.getFileIds(cons.ANAPLAN_LOADMODEL_WORKSPACEID,cons.ANAPLAN_LOADMODEL_MODELID,token)

    #Get all Line items for a model
    #anaplan.getAlllineitems(cons.ANAPLAN_LOADMODEL_MODELID,token)

    #Get module Ids for a model
    #anaplan.getmoduleID(cons.ANAPLAN_LOADMODEL_MODELID,token)

    #Get lists Id's for a model
    #anaplan.getLists(cons.ANAPLAN_LOADMODEL_WORKSPACEID,cons.ANAPLAN_LOADMODEL_MODELID,token)

#Main function call
if __name__ == '__main__':
    
    run()