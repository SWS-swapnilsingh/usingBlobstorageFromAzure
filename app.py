from flask import Flask,request, redirect
import os
from azure.storage.blob import BlobServiceClient

app = Flask(__name__)

#retrive the connection string from the environment variable
connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
connect_str = 'DefaultEndpointsProtocol=https;AccountName=mystorageaccount1947;AccountKey=4AyIwGd23iteMKvGi8OxrIe/xOKJiG/OReqr2awGWXRWrsfUm/CHwUFbGGM/tiboSA5SzdqXjSAy+AStYIbuiA==;EndpointSuffix=core.windows.net'
print(connect_str,"**************************")
container_name = "photos"  #container name in which images will be store in the storage account

blob_service_client = BlobServiceClient.from_connection_string(conn_str=connect_str)
try:
    container_client = blob_service_client.get_container_client(container=container_name)
    container_client.get_container_properties()
except Exception as e:
    container_client = blob_service_client.create_container(container_name)


# DefaultEndpointsProtocol=https;AccountName=mystorageaccount1947;AccountKey=4AyIwGd23iteMKvGi8OxrIe/xOKJiG/OReqr2awGWXRWrsfUm/CHwUFbGGM/tiboSA5SzdqXjSAy+AStYIbuiA==;EndpointSuffix=core.windows.net
@app.route("/")
def view_photos():
    blob_items = container_client.list_blobs()


    img_html = ""
    

    for blob in blob_items:
        blob_client = container_client.get_blob_client(blob=blob.name)
        img_html += "<img src='{}' width='auto' height='200' />".format(blob_client.url)
    return '''
    <h1>Upload new File</h1>
    <form method = "post" action = "/upload-photos" enctype = "multipart/form-data">
    <input type="file" name="photos" multiple >
    <input type="submit">
    </form>
    '''+ img_html

#flask endpoint to upload a photo
@app.route("/upload-photos", methods=['POST'])
def upload_photos():
    filenames = ""
    for file in request.files.getlist("photos"):
        try:
            container_client.upload_blob(file.filename, file)
            filenames += file.filename + "<br />"
        except Exception as e:
            print(e)
            print("Ignoring duplicate filesnames")
        # filenames += file.filename + " "
    # return "<p>Uploaded: <br />{}</p>".format(filenames)
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
