<template>
  <div id="app" style=" height: 100%;width: 100%">
    <eheader></eheader>
    <router-view></router-view>
  </div>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

</style>
<script>
import Eheader from './components/eheader'
export default {
  components: { Eheader }
}
</script>
