<template>
  <div id="app" :style="'height:'+this.webHeight*0.95+'px;witdh:'+this.webWidth+'px'">
    <eheader style="height: 8%"></eheader>
<!--    <Kgraph></Kgraph>-->
    <router-view style="height: 90%; width: 100% ;background: #f6f6f6"></router-view>
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
  components: { Eheader },
  data(){
    return{
      webWidth:600,
      webHeight:900
    }
  },
  mounted() {
    this.webWidth=document.documentElement.clientWidth;
    this.webHeight = document.documentElement.clientHeight;
  }
}
</script>
