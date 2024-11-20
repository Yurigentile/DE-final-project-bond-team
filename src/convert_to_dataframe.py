import pandas as pd
import boto3
        
#Need to discuss if it`s better to trigger the lambda with another lambda or from the update of the bucket

def convert_json_to_dataframe(datadict):  
        newdict = {}
        for key in datadict:               
                newdict[key] = pd.DataFrame(datadict[key]) 
        print(newdict)
        return newdict