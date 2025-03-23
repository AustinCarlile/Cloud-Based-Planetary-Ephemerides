from fastapi.testclient import TestClient
from isdAPI import app
import brotli
import os
import pathlib
import pvl
import json
import sys

test_client = TestClient(app)

#inLabel = sys.argv[1]


def test_send_encode(inLabel):
    
    with open(inLabel, 'r', errors = 'ignore') as label_file:
        label_bytes = label_file.read()
        
    label_encode = label_bytes.encode()
    
    label_compress = brotli.compress(label_encode)
    
    response = test_client.post("/getIsd", content = label_compress)
    assert response.status_code == 200
    
def test_recieve(inLabel):
    response = test_client.post("/read", content = label_compress)
    assert response.status_code == 200
    
def test_send(inLabel):
    with open(inLabel, 'r',) as label_file:
        label_bytes = label_file.read()
    
    response = test_client.post("/getIsd", content = label_bytes)
    assert response.status_code == 200
    
if __name__ == "__main__":
    for file in os.listdir('/home/austin/ale/miniLabels/docker_api/data/lbl//'):
         test_send_encode(f'/home/austin/ale/miniLabels/docker_api/data/lbl/{file}')
    #test_send_encode('/home/austin/ale/miniLabels/docker_api/M103595705LE_isis3.lbl')
