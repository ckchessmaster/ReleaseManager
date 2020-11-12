import logging, os
import azure.functions as func

from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__

def main(blob: func.InputStream):
  logging.info(f'Python blob trigger function triggered by new release: {blob.name}')

  connect_str = os.getenv('AzureWebJobsStorage')
  blob_service_client = BlobServiceClient.from_connection_string(connect_str)
  container_client = blob_service_client.get_container_client("clientreleases")

  blob_list = [b.name for b in list(container_client.list_blobs())]

  new_release_name = list(blob.name.split('/'))[-1]

  blob_list.remove(new_release_name)

  logging.info(f'Deleting old releases...')
  container_client.delete_blobs(*blob_list)
  logging.info(f'Release processing complete.')