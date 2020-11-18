<template>
  <div id="app">
    <Navigation />
    <div id="download-container">
      <h2>Current Version: v{{currentReleaseVersion}}</h2>
      <a class="btn" :href="downloadLink">Download</a>
    </div>
  </div>
</template>

<script>
import ReleaseService from './services/releaseService'

import Navigation from './components/Navigation.vue'

export default {
  name: 'App',
  components: {
    Navigation
  },
  data: () => ({
    releaseService: null,
    currentReleaseVersion: '',
    downloadLink: ''
  }),
  async mounted () {
    this.releaseService = new ReleaseService()
    this.currentReleaseVersion = await this.releaseService.getLatestRelease()
    this.downloadLink = this.releaseService.getDownloadLink(this.currentReleaseVersion)
  }
}
</script>

<style lang="scss">
@import '@/styles/main.scss';

#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  margin-top: 60px;
}

#download-container {
  margin: 0;
  position: absolute;
  top: 50%;
  left: 50%;
  -ms-transform: translate(-50%, -50%);
  transform: translate(-50%, -50%);
}

h2 {
  padding: 10px;
}
</style>
