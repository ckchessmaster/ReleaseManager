import unittest, json
from unittest import mock

import azure.functions as func

from CleanOldReleases import main 

class FakeBlob:
  def __init__(self, name):
    self.name = name

class TestCleanOldReleases(unittest.TestCase):
  @mock.patch('CleanOldReleases.BlobServiceClient')
  def test_no_other_releases(self, mock_blob_service_client):
    # Arrange
    mock_blob_service_client.from_connection_string().get_container_client().list_blobs.return_value = [FakeBlob('OneReleaseToRuleThemAll-v1.2.3.zip')]

    # Act
    main(None)

    # Assert
    mock_blob_service_client.from_connection_string().get_container_client().delete_blobs.assert_not_called()

  @mock.patch('CleanOldReleases.BlobServiceClient')
  def test_major_version(self, mock_blob_service_client):
    # Arrange
    previous_releases = [
      FakeBlob('OneReleaseToRuleThemAll-v2.1.1.zip'),
      FakeBlob('OneReleaseToRuleThemAll-v1.2.1.zip'),
      FakeBlob('OneReleaseToRuleThemAll-v1.1.2.zip')
    ]

    mock_blob_service_client.from_connection_string().get_container_client().list_blobs.return_value = previous_releases

    expected_delete = [
      'OneReleaseToRuleThemAll-v1.2.1.zip',
      'OneReleaseToRuleThemAll-v1.1.2.zip'
    ]

    # Act
    main(None)

    # Assert
    mock_blob_service_client.from_connection_string().get_container_client().delete_blobs.assert_called_with(*expected_delete)

  @mock.patch('CleanOldReleases.BlobServiceClient')
  def test_minor_version(self, mock_blob_service_client):
    # Arrange
    previous_releases = [
      FakeBlob('OneReleaseToRuleThemAll-v1.3.1.zip'),
      FakeBlob('OneReleaseToRuleThemAll-v1.2.1.zip'),
      FakeBlob('OneReleaseToRuleThemAll-v1.1.2.zip')
    ]

    mock_blob_service_client.from_connection_string().get_container_client().list_blobs.return_value = previous_releases

    expected_delete = [
      'OneReleaseToRuleThemAll-v1.2.1.zip',
      'OneReleaseToRuleThemAll-v1.1.2.zip'
    ]

    # Act
    main(None)

    # Assert
    mock_blob_service_client.from_connection_string().get_container_client().delete_blobs.assert_called_with(*expected_delete)

  @mock.patch('CleanOldReleases.BlobServiceClient')
  def test_build_version(self, mock_blob_service_client):
    # Arrange
    previous_releases = [
      FakeBlob('OneReleaseToRuleThemAll-v1.1.3.zip'),
      FakeBlob('OneReleaseToRuleThemAll-v1.1.2.zip'),
      FakeBlob('OneReleaseToRuleThemAll-v1.1.1.zip')
    ]

    mock_blob_service_client.from_connection_string().get_container_client().list_blobs.return_value = previous_releases

    expected_delete = [
      'OneReleaseToRuleThemAll-v1.1.2.zip',
      'OneReleaseToRuleThemAll-v1.1.1.zip'
    ]

    # Act
    main(None)

    # Assert
    mock_blob_service_client.from_connection_string().get_container_client().delete_blobs.assert_called_with(*expected_delete)
    