const axios = require('axios')

export class ReleaseService {
  baseUrl = 'https://uansagamerelease.blob.core.windows.net/clientreleases'

  async getLatestRelease() {
    let response = await axios.get(`${this.baseUrl}?restype=container&comp=list`)

    let parser = new DOMParser()
    let xml = parser.parseFromString(response.data, "text/xml")
    let releases = xml.getElementsByTagName('Name')

    if (releases.length < 2) {
      return this.getVersionFromName(releases[0])
    }
    
    let maxRelease = releases[0].innerHTML
    let maxVersion = this.getVersionFromName(maxRelease)

    for (let i = 1; i < releases.length; i++) {
      let releaseVersion = this.getVersionFromName(releases[i].innerHTML)
      
      if (this.compareVersionNumbers(maxVersion, releaseVersion) == -1) {
        maxRelease = releases[i]
        maxVersion = releaseVersion
      }
    }

    return maxVersion
  }

  getDownloadLink(version) {
    return `${this.baseUrl}/game-v${version}.zip`
  }

  getVersionFromName(name) {
    let versionNumber = name.split('-v')[1].split('.zip')[0]

    return versionNumber
  }

  compareVersionNumbers(version1, version2) {
    let version1Parts = version1.split('.')
    let version2Parts = version2.split('.')

    // Check major version
    if (Number(version1Parts[0] > Number(version2Parts[0]))) {
      return 1
    } else if (Number(version1Parts[0] < Number(version2Parts[0]))) {
      return -1
    } else {
      // Check minor version
      if (Number(version1Parts[1] > Number(version2Parts[1]))) {
        return 1
      } else if (Number(version1Parts[1] < Number(version2Parts[1]))) {
        return -1
      } else {
        // Check build revision
        if (Number(version1Parts[2] > Number(version2Parts[2]))) {
          return 1
        } else if (Number(version1Parts[2] < Number(version2Parts[2]))) {
          return -1
        } else {
          return 0
        }
      }
    }
  }
}
