<template>
  <div id="app">
    <eheader style="height: 60px"></eheader>
<!--    <Kgraph></Kgraph>-->
    <router-view style="height: 660px ;background: #f6f6f6"></router-view>
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

#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>
<script>
import Eheader from './components/eheader'
// import Kgraph from "./components/kgraph";
export default {
  components: { Eheader }
}
</script>
