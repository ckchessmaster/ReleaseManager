import logging, os
import azure.functions as func

from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

def main(mytimer: func.TimerRequest) -> None:
  logging.info(f'Cleaning old releases...\n')

  connect_str = os.getenv('AzureWebJobsStorage')
  blob_service_client = BlobServiceClient.from_connection_string(connect_str)
  container_client = blob_service_client.get_container_client("clientreleases")

  releases = [b.name for b in list(container_client.list_blobs())]

  # No need to go further, we know this is the max release
  if (len(releases) < 2):
    return

  client_releases = list(filter(lambda release: 'Client' in release, releases))
  server_releases = list(filter(lambda release: 'Server' in release, releases))

  if len(client_releases) > 0:
    releases.remove(get_max_version(client_releases))
  
  if len(server_releases) > 0:
    releases.remove(get_max_version(server_releases))

  # previous_releases.remove(max_release)

  container_client.delete_blobs(*releases)
  
  logging.info(f'Cleaning complete.')

def get_version_from_name(name):
  version_number = name.split('-v')[-1]

  return version_number

def get_max_version(releases):
  max_release = releases[0]
  max_version = get_version_from_name(max_release)

  iterator = iter(releases)
  next(iterator) # Skip the 1st one

  for release in iterator:
    release_version = get_version_from_name(release)
    if compare_version_numbers(max_version, release_version) == -1:
      max_release = release
      max_version = release_version

  return max_release

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