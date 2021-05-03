<template>
  <el-container>

      <el-main v-if="this.mapisloaded">
        <el-row class="mainbox">
          <el-col :span="6" class="leftbox">

              <pie-chart v-bind:resq="provincePieData" style="width: 100%;"></pie-chart>

          </el-col>
          <el-col :span="12" class="middlebox">

          <map-china v-bind:china="chinadata" v-bind:province="provincedata" style="width: 100%;"></map-china>

          </el-col>
          <el-col :span="6" class="rightbox" >

              <piechart_foreign v-bind:resq="countryPieData" style="width: 100%;"></piechart_foreign>

          </el-col>
        </el-row>


      </el-main>

  </el-container>
</template>

<script>
// @ is an alias to /src
// import {doSearch} from '../apis/search.js'
// import Kgraph from "./components/kgraph";
import mapChina from "@/components/mapChina.vue";
import axios from "axios";
import pieChart from "@/components/pieChart"
import piechart_foreign from "@/components/pieChart_foreign";
export default {
  name: 'Home',
  data(){
    return{
      chinadata:[],
      provincedata:{},
      provincePieData:{},
      countryPieData:{},
      mapisloaded:false
    }
  },
  components: {

    mapChina,
    pieChart,
    piechart_foreign
  },
  mounted() {
    this.mapisloaded = false
  axios.get("http://172.22.69.121:5000/").then(resp=>{
    this.chinadata = resp.data.data["China"]
    this.provincedata = resp.data.data["Provinces"]
    this.provincePieData = resp.data.data["pie_province"]
    this.countryPieData = resp.data.data["bar_country"]
    this.mapisloaded = true
  })
  },
  methods: {

  }
}
</script>
<style>
.mainbox{

}
.leftbox{
  width: 300px
}
.middlebox{
  width: 600px
}
.rightbox{
  width: 300px
}
</style>
