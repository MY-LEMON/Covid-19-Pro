<template>

    <el-container>
    <el-header>
      <el-input placeholder="请输入问题" v-model="input" onfocus="select">

        <el-button @click="submit" slot="append" icon="el-icon-search"></el-button>
      </el-input>
    </el-header>
    <el-container v-if="isloaded">

      <el-aside width="30%">{{textdata}}</el-aside>
      <el-main><Kgraph  v-bind:graph_json_data="graphdata" ></Kgraph></el-main>
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
      isloaded: false
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
      this.isloaded = false
      axios.get("https://b2f65068-d22f-4c9e-81c6-2faa7d5cb2bd.mock.pstmn.io/qna",{
        params:{
          "key":this.input
        }
      }).then(resp=>{
        console.log("loading data")
        this.graphdata = resp.data.data[1]
        this.textdata = resp.data.data[0]
        this.isloaded = true
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
