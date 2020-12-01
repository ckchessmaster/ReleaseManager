import axios from 'axios';
import ReleaseService from '@/services/releaseService'

jest.mock('axios');

describe('When getting the latest release', () => {
  it('Should return the only available version when there is only one version', async () => {
    // Arrange
    const expectedVersion = '0.1.289'

    const response = { 
      data: `
      <EnumerationResults ContainerName="https://uansagamerelease.blob.core.windows.net/clientreleases">
        <Blobs>
          <Blob>
            <Name>gameClient-v${expectedVersion}.zip</Name>
          </Blob>
        </Blobs>
      </EnumerationResults>` 
    }

    axios.get.mockResolvedValue(response)

    // Act
    const releaseService = new ReleaseService()
    const result = await releaseService.getLatestRelease()

    // Assert
    expect(result).toBe(expectedVersion)
  })

  it('Should return the latest version by major version', async () => {
    // Arrange
    const expectedVersion = '2.1.289'

    const response = { 
      data: `
      <EnumerationResults ContainerName="https://uansagamerelease.blob.core.windows.net/clientreleases">
        <Blobs>
          <Blob>
            <Name>gameClient-v${expectedVersion}.zip</Name>
          </Blob>
          <Blob>
            <Name>gameClient-v1.1.289.zip</Name>
          </Blob>
        </Blobs>
      </EnumerationResults>` 
    }

    axios.get.mockResolvedValue(response)

    // Act
    const releaseService = new ReleaseService()
    const result = await releaseService.getLatestRelease()

    // Assert
    expect(result).toBe(expectedVersion)
  })

  it('Should return the latest version by minor version', async () => {
    // Arrange
    const expectedVersion = '1.2.289'

    const response = { 
      data: `
      <EnumerationResults ContainerName="https://uansagamerelease.blob.core.windows.net/clientreleases">
        <Blobs>
          <Blob>
            <Name>gameClient-v${expectedVersion}.zip</Name>
          </Blob>
          <Blob>
            <Name>gameClient-v1.1.289.zip</Name>
          </Blob>
        </Blobs>
      </EnumerationResults>` 
    }

    axios.get.mockResolvedValue(response)

    // Act
    const releaseService = new ReleaseService()
    const result = await releaseService.getLatestRelease()

    // Assert
    expect(result).toBe(expectedVersion)
  })

  it('Should return the latest version by build version', async () => {
    // Arrange
    const expectedVersion = '1.1.290'

    const response = { 
      data: `
      <EnumerationResults ContainerName="https://uansagamerelease.blob.core.windows.net/clientreleases">
        <Blobs>
          <Blob>
            <Name>gameClient-v${expectedVersion}.zip</Name>
          </Blob>
          <Blob>
            <Name>gameClient-v1.1.289.zip</Name>
          </Blob>
        </Blobs>
      </EnumerationResults>` 
    }

    axios.get.mockResolvedValue(response)

    // Act
    const releaseService = new ReleaseService()
    const result = await releaseService.getLatestRelease()

    // Assert
    expect(result).toBe(expectedVersion)
  })
})
