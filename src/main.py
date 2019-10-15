import argparse
import sys
import logging
from azure.storage.blob import (
    BlockBlobService,
    ContainerPermissions
)
import requests
import json
from typing import List

parser = argparse.ArgumentParser()
parser.add_argument("--storage_account", type=str)
parser.add_argument("--storage_key", type=str)
parser.add_argument("--storage_container", type=str)
parser.add_argument("--cv_endpoint", type=str)
parser.add_argument("--cv_train_key", type=str)
parser.add_argument("--cv_project_id", type=str)

print("Received arguments = " + repr(sys.argv))

args = parser.parse_args()

def image_request_format_from_sas(blob_sas):
    return {"url" : blob_sas}

def upload_to_custom_vision(blob_sas_list : List[str]):
    request_url = "https://{}/customvision/v3.0/training/projects/{}/images/urls".format(
        args.cv_endpoint,
        args.cv_project_id
    )
    headers = {
        "Training-Key" : args.cv_train_key,
        "Content-Type" : "application/json"
    }
    images_list = [image_request_format_from_sas(blob_sas) for blob_sas in blob_sas_list]
    request_body = {
        "images" : images_list
    }
    response = requests.post(request_url, json=json.dumps(request_body))
    print(response.json())


bbs = BlockBlobService(account_name=args.storage_account, account_key=args.storage_key)

limit = 63
counter = 0
blob_sas_block = []
for blob_name in bbs.list_blob_names():
    if(counter < limit):
        blob_sas_block.append(bbs.generate_blob_shared_access_signature(container_name=args.storage_container, blob_name=blob_name))
    else:
        upload_to_custom_vision(blob_sas_block)
        blob_sas_block = []
        counter = 0
        print("COMPLETED BLOCK")

print("DONE!!!")
    