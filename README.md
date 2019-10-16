# Azure_CustomVision_Blob_Connector
Need to do a service to service transfer loading blob images into Azure's custom vision service?  This is a python based program to do just that.

Example usage:
python ./src/main.py --storage_account "YOUR_ACCOUNT_NAME" --storage_key "YOUR_ACCOUNT_KEY" --storage_container "YOUR_STORAGE_CONTAINER" --cv_endpoint "https://{YOUR_REGION}.api.cognitive.microsoft.com/" --cv_train_key "YOUR_CUSTOM_VISION_KEY" --cv_project_id "YOUR_CUSTOM_VISION_PROJECT_ID"

Of all of the parameters, the project_id is the hardest to locate.  Navigate to the custom vision portal and select the project which you have created that you wish to copy the images into.  The URL will look like this:

https://www.customvision.ai/projects/{YOUR_PROJECT_ID}d#/manage

It'll be a bunch of numbers, letters and hyphens.  That is your project_id.