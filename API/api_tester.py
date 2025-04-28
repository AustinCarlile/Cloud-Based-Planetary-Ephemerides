from fastapi.testclient import TestClient
from isdAPI import app
import brotli
import os
import decimal
import pathlib
import pvl
import json
import sys

test_client = TestClient(app)

inLabel = sys.argv[1]

path = pathlib.Path(__file__).parent.resolve()
os.makedirs(f'{path}/returned_isds', exist_ok=True)

# JSON Encoder for parsing decimals to float values
class decimalToFloat(json.JSONEncoder):
    def default(self, value):
        if isinstance(value, decimal.Decimal):
            return float(value)

def test_send_encode(inLabel):
    
    with open(inLabel, 'r', errors = 'ignore') as label_file:
        label_bytes = label_file.read()
        
    label_encode = label_bytes.encode()
    
    label_compress = brotli.compress(label_encode)
    
    response = test_client.post("/getIsd", content = label_compress)
                                                                                    
    response_uncompress = brotli.decompress(response.content)
    decode_response = response_uncompress.decode()                           
    
    outputFile = f"{path}/returned_isds/test_isd.json"
    
    isd_dict = json.loads(decode_response, parse_float = decimal.Decimal)
    
    # serializes dictionary to json object and writes to file
    with open(outputFile, 'w') as isd_output:
        json.dump(isd_dict, isd_output, cls = decimalToFloat, indent = 2)
    
    assert response.status_code == 200
    
if __name__ == "__main__":
    #for file in os.listdir(f'{path}/test_data/'):
    #     test_send_encode(f'{path}/test_data/{file}')
    test_send_encode(f"{path}/{inLabel}")
