<template>
  <el-container>

      <el-aside>

      </el-aside>
      <el-main v-if="this.mapisloaded">
        <map-china v-bind:china="chinadata" v-bind:province="provincedata"></map-china>
      </el-main>

  </el-container>
</template>

<script>
// @ is an alias to /src
// import {doSearch} from '../apis/search.js'
// import Kgraph from "./components/kgraph";
import mapChina from "@/components/mapChina.vue";
import axios from "axios";
export default {
  name: 'Home',
  data(){
    return{
      chinadata:{},
      provincedata:{},
      mapisloaded:false
    }
  },
  components: {
    mapChina
  },
  mounted() {
  axios.get("http://172.22.69.121:5000/").then(resp=>{
    this.chinadata = resp.data.data["China"]
    this.provincedata = resp.data.data["Provinces"]
    this.mapisloaded = true
  })
  },
  methods: {

  }
}
</script>
<style>

</style>
