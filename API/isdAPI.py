from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import boto3
import brotli
import decimal
import hashlib
import pathlib
import pvl
import json
import os
import shutil
import sys

app = FastAPI()

path = pathlib.Path(__file__).parent.resolve()

aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
region_name = os.environ.get('AWS_REGION', 'us-east-2')  # Default to 'us-east-2' if not set
table_name = os.environ.get('DYNAMO_TABLE_NAME', 'ISD-DynamoDB-9EN5K7Y5DJHO') 


# Initialize DynamoDB resource
dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=region_name
)

# Reference the DynamoDB table
table = dynamodb.Table(table_name)
# Pydantic model for item input validation
class Item(BaseModel):
    ID: str
    Isd: str
    
class decimalToFloat(json.JSONEncoder):
    def default(self, value):
        if isinstance(value, decimal.Decimal):
            return float(value)
    
def create_mini_label(input_file):
    
    # opening label file
    with open(input_file, 'r') as label_file:
        label_dict = pvl.load(label_file)

    # populate miniLabelDict with acceptable groups
    mini_label_dict = {key:label_dict['IsisCube'][key] for key in ['Core', 'Instrument', 'BandBin', 'Kernels']}

    #  Add Label object to miniLabelDict
    mini_label_dict['Label'] = label_dict['Label']

    # convert mini label dictionary to string
    mini_label_string = str(mini_label_dict)

    return mini_label_string
    
def create_hash(mini_label_string):

    # creating hash of encoded MiniLabel string
    hashData = hashlib.sha256(mini_label_string.encode())

    # creating hexidecimal version of hash
    hashHex = hashData.hexdigest()

    # return hexidecimal hash
    return hashHex
    
@app.post("/getIsd")
async def get_isd(request: Request):
    label = await request.body()
    label_uncompress = brotli.decompress(label)
    label_string = label_uncompress.decode()
    
    temp_file = 'temp.lbl'
    
    with open(temp_file, 'w') as label_file:
        label_file.write(label_string)
    
    
    spiceinit_cmd = f"spiceinit from={temp_file}"
    os.system (spiceinit_cmd)
        
    requested_isd = os.system(f'isd_generate {temp_file} -v')
    mini_label = create_mini_label(temp_file)
    isd_hash = create_hash(mini_label)
    
    os.remove(temp_file)
    
    with open('temp.json', 'r') as isd_file:
        isd_dict = json.load(isd_file, parse_float = decimal.Decimal)
        
    table.put_item(
        Item = {
            'id': isd_hash,
            'isd': isd_dict
        }
    )
        
    serverResponse = table.get_item(
        Key = {
            'id': isd_hash
        }
    )
    # remove server response metadata, return isd key values only
    outputDict = {key:serverResponse['Item'][key] for key in ['isd']}

    # remove isd key, only have inner values
    outputDict = outputDict['isd']
    
    outputFile = f"{path}/returned_isds/{isd_hash}_isd.json"

    # serializes dictionary to json object and writes to file
    with open(outputFile, 'w') as isd_output:
        json.dump(outputDict, isd_output, cls = decimalToFloat, indent = 2)

# CRUD Operations inside FastAPI routes
@app.post("/create")
def create_item(inHash: str, isdDict: dict):
    with open(inIsd, 'r') as isdFile:
        isdDict = json.load(isdFile, parse_float = decimal.Decimal)

    # sends item with hash id and isd value to table, then saves response
    table.put_item(
        Item = {
            'id': inHash,
            'isd': isdDict
        }
    )
    

@app.get("/read/{id}")
def read_item(inHash: str):
    serverResponse = table.get_item(
        Key = {
            'id': inHash
        }
    )
    # remove server response metadata, return isd key values only
    outputDict = {key:serverResponse['Item'][key] for key in ['isd']}

    # remove isd key, only have inner values
    outputDict = outputDict['isd']
    
    # serializes dictionary to json object and writes to file
    with open(outputFile, 'w') as isd_output:
        json.dump(outputDict, isd_output, cls = decimalToFloat, indent = 2)

@app.put("/update/{id}")
def update_item(id: str, item: Item):
    table.update_item(
        Key={'ID': id},
        UpdateExpression="set Name = :name, Age = :age",
        ExpressionAttributeValues={
            ':name': item.Name,
            ':age': item.Age
        }
    )
    return {"message": "Item updated"}

@app.delete("/delete/{id}")
def delete_item(id: str):
    table.delete_item(Key={'ID': id})
    return {"message": "Item deleted"}

# Run the app with: uvicorn isdAPI:app --reload
