<template>

    <el-container>
    <el-header>
      <el-input placeholder="请输入问题" v-model="input" onfocus="select">

        <el-button @click="submit" slot="append" icon="el-icon-search"></el-button>
      </el-input>
    </el-header>
    <el-container v-if="isLoaded">

      <el-aside width="30%" v-if="isSearched">{{textdata}}</el-aside>
      <el-main v-if="isSearched"><Kgraph  v-bind:graph_json_data="graphdata" ></Kgraph></el-main>

      <div v-if="!isSearched">
        <h3>未搜索到结果</h3>
      </div>
    </el-container>
      <el-container v-if="this.isloaded == true">

      </el-container>
    </el-container>



</template>

<script>
// import {doSearch} from "@/apis/search";
import Kgraph from "../components/kgraph.vue";
import axios from "axios";
export default {
  name: 'QNA',
  props:{
    graphdata:{
      type: Object,
      require: true
    },
    textdata:{
      type: Object,
      require: true
    }
  },
  data(){
    return{
      input:'',
      isLoaded: false,
      resMsg:""
    }
  },
  computed:{
    isSearched(){
      return this.resMsg=="搜索结果"
    }
  },
beforeMount() {
    console.log("QNA page mounting")

},

  mounted() {
    console.log("QNA page mounted")
  },
  components: {
    Kgraph
  },
  methods: {
    submit(){
      this.isLoaded = false
      axios.get("http://172.22.69.121:5000/search",{
        params:{
          "key":this.input
        }
      }).then(resp=>{
        console.log("loading data")
        console.log(resp.data)
        this.graphdata = resp.data.data[1]
        this.textdata = resp.data.data[0]
        this.resMsg = resp.data.message
        this.isLoaded = true

      })
    }
  }
}
</script>

<style scoped>
.left {
  float: left;
  width: 200px;
  height: 100%;
}
.right {
  margin-left: 200px;
}
</style>
