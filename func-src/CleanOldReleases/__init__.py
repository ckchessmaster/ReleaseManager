import logging, os
import azure.functions as func

from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

def main(req: func.HttpRequest) -> func.HttpResponse:
  logging.info(f'Clean old releases reuqest received.\n')

  connect_str = os.getenv('AzureWebJobsStorage')
  blob_service_client = BlobServiceClient.from_connection_string(connect_str)
  container_client = blob_service_client.get_container_client("clientreleases")

  previous_releases = [b.name for b in list(container_client.list_blobs())]

  # No need to go further, we know this is the max release
  if (len(previous_releases) < 2):
    return

  max_release = previous_releases[0]
  max_version = get_version_from_name(max_release)

  iterator = iter(previous_releases)
  next(iterator) # Skip the 1st one

  for release in iterator:
    release_version = get_version_from_name(release)
    if compare_version_numbers(max_version, release_version) == -1:
      max_release = release
      max_version = release_version

  previous_releases.remove(max_release)

  logging.info(f'Deleting old releases...')
  container_client.delete_blobs(*previous_releases)
  
  logging.info(f'Release processing complete.')

def get_version_from_name(name):
  version_tag = name.split('-')
  version_number = version_tag[-1].replace('v', '')

  return version_number

def compare_version_numbers(version1, version2):
  version1_parts = version1.split('.')
  version2_parts = version2.split('.')

  # check major version
  if int(version1_parts[0]) > int(version2_parts[0]):
    return 1
  elif int(version1_parts[0]) < int(version2_parts[0]):
    return -1
  else:
    # check minor version
    if int(version1_parts[1]) > int(version2_parts[1]):
      return 1
    elif int(version1_parts[1]) < int(version2_parts[1]):
      return -1
    else:
      # check build revision
      if int(version1_parts[2]) > int(version2_parts[2]):
        return 1
      elif int(version1_parts[2]) < int(version2_parts[2]):
        return -1
      else:
        return 0