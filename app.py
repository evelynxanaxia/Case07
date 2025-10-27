from flask import Flask, jsonify, request, render_template
from dotenv import load_dotenv
import os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient


#load_dotenv()  # reads .env into process env


app = Flask(__name__)
CONTAINER_NAME = "images-demo"

def get_blob_service_client():
    connection_string = os.environ.get('STORAGE_KEY')
    if not connection_string:
        raise ValueError("STORAGE_KEY not found in environment variables")
    return BlobServiceClient.from_connection_string(connection_string)


@app.route('/api/v1/health')
def health():
   return jsonify({
       'status': 'ok'
   }),200


@app.route('/api/v1/upload', methods=['POST'])
def upload():
   file = request.files['file']
   try:
       container_client = blob_service_client.get_container_client(CONTAINER_NAME)
       blob_client = container_client.get_blob_client(file.filename)
       blob_client.upload_blob(file, overwrite=True)
       return jsonify({
       'ok': True,
       'url': container_client.url + '/' + file.filename
       }), 200
   except Exception as e:
       return jsonify({
           'ok': False,
           'error': str(e)  
       }),500




@app.route('/api/v1/gallery', methods=['GET'])
def gallery():
   try:
       container_client = blob_service_client.get_container_client(CONTAINER_NAME)
       blobs = container_client.list_blobs()
       return jsonify({
        "ok": True,
        "gallery": [f'{container_client.url}/{blob.name}' for blob in blobs],
   }), 200
   except Exception as e:
       return jsonify({
           'error': str(e)
       }),500


@app.route('/')
def index():
   return render_template('index.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
