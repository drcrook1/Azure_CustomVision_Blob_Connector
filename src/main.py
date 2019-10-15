import argparse
import sys
import logging
from azure.storage.blob import (
    BlockBlobService,
    BlobPermissions
)
from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.training.models import ImageUrlCreateEntry
import requests
import json
from datetime import datetime, timedelta
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

def check_print_failure(upload_result):
    if not upload_result.is_batch_successful:
        print("Image batch upload failed.")
        for image in upload_result.images:
            print("Image status: ", image.status)
    return None

bbs = BlockBlobService(account_name=args.storage_account, account_key=args.storage_key)
train_client = CustomVisionTrainingClient(args.cv_train_key, endpoint=args.cv_endpoint)

limit = 63
counter = 0
image_block = []

for blob_name in bbs.list_blob_names(args.storage_container):
    if(counter < limit):
        print("attempting blob: {}".format(blob_name))
        now = datetime.utcnow()
        permission = BlobPermissions(read=True)
        sas_token = bbs.generate_blob_shared_access_signature(container_name=args.storage_container, 
                                                                blob_name=blob_name,
                                                                start=now,
                                                                expiry=now + timedelta(minutes=15),
                                                                permission=permission)
        sas_url = bbs.make_blob_url(container_name=args.storage_container, blob_name=blob_name, sas_token=sas_token)
        print(sas_url)
        image_entry = ImageUrlCreateEntry(url=sas_url)
        image_block.append(image_entry)
        counter += 1
    else:
        print("attempting upload...")
        upload_result = train_client.create_images_from_urls(project_id=args.cv_project_id, images=image_block)
        check_print_failure(upload_result)
        image_block = []
        counter = 0
        print("COMPLETED BLOCK")

print(len(image_block))
upload_result = train_client.create_images_from_urls(project_id=args.cv_project_id, images=image_block)
check_print_failure(upload_result)
print("DONE!!!")
    