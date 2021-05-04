<template>
  <el-container style="height: 100%">

      <el-main v-if="this.mapisloaded" style="height: 100%">
        <el-row class="mainbox">
          <el-col :span="6" class="leftbox">
            <el-row style="height: 50%">
              <pie-chart v-bind:resq="provincePieData" style="width: 100%; height: 100% ;margin-left: 10px"></pie-chart>
            </el-row>
            <el-row style="height: 50%">
              <rank v-bind:resq="rankData" style="width: 100%; height: 100% ;margin-left: 10px"></rank>
            </el-row>
          </el-col>
          <el-col :span="12" class="middlebox">

            <map-china v-bind:china="chinadata" v-bind:province="provincedata" style="width: 100%; height: 100%"></map-china>

          </el-col>
          <el-col :span="6" class="rightbox">
            <el-row style="height: 50%">
              <piechart_foreign v-bind:resq="countryPieData" style="width: 100%; height: 100% ;margin-left: 10px"></piechart_foreign>
            </el-row>
            <el-row style="height: 50%">
              <rank_foreign v-bind:resq="rankForeignData" style="width: 100%; height: 100% ;margin-left: 10px"></rank_foreign>
            </el-row>
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
import rank from "@/components/rank";
import rank_foreign from "@/components/rank_foreign";
export default {
  name: 'Home',
  data(){
    return{
      chinadata:[],
      provincedata:{},
      provincePieData:{},
      countryPieData:{},
      rankData:{},
      rankForeignData:{},
      mapisloaded:false
    }
  },
  components: {

    mapChina,
    pieChart,
    piechart_foreign,
    rank,
    rank_foreign
  },
  mounted() {
    this.mapisloaded = false
  axios.get("http://172.22.69.121:5000/").then(resp=>{
    this.chinadata = resp.data.data["China"]
    this.provincedata = resp.data.data["Provinces"]
    this.provincePieData = resp.data.data["pie_province"]
    this.countryPieData = resp.data.data["bar_country"]
    this.rankData = resp.data.data["bar_province"]
    this.rankForeignData = resp.data.data["bar_country"]
    this.mapisloaded = true
  })
  },
  methods: {

  }
}
</script>
<style>
.mainbox{
  width: 100%;
  height: 100%;
}
.leftbox{
  width: 25%;
  height: 100%;
}
.middlebox{
  width: 50%;
  height: 100%;
}
.rightbox{
  width: 25%;
  height: 100%;
}
</style>
