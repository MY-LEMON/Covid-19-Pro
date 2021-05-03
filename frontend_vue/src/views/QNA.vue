<template>

    <el-container v-loading="loading">
      <el-header>
      <el-input placeholder="请输入问题" v-model="input" :class="isLoaded?'b2t':'t2b'" style="width: 60%" >

        <el-button @click="submit" slot="append" icon="el-icon-search"></el-button>
      </el-input>
      </el-header>
    <el-container v-if="isLoaded">

      <el-aside width="30%" v-if="isSearched">{{textdata}}</el-aside>
        <el-main v-if="isSearched">
          <Kgraph  v-bind:graph_json_data="graphdata" ></Kgraph>
        </el-main>

      <div v-if="!isSearched">
        <h3>未搜索到结果</h3>
      </div>
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
      loading: false,
      input:'',
      isLoaded: false,
      resMsg:"",
      // teststyle0:{
      //
      // },
      // teststyle1:{
      //   width: '60%' ,
      //   top:'30%' ,
      //   left: '20%'
      // }
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
      this.loading=true
      this.isLoaded = false
      axios.get("https://b2f65068-d22f-4c9e-81c6-2faa7d5cb2bd.mock.pstmn.io/qna",{
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
        this.loading = false

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
.t2b{
  animation: start1 1s cubic-bezier(.7,0,.3,1);
  animation-fill-mode:forwards;
  /*margin-top: 100px;*/
}
.b2t{
  animation: end1 1s cubic-bezier(.7,0,.3,1);
  animation-fill-mode:forwards;
}
@keyframes start1 {
  0%{
    transform: translateY(0px);
    /*top:0px*/
  }

  100%{
    transform: translateY(200px);
    /*top: 100px*/
  }
}
@keyframes end1 {
  from{
    transform: translateY(200px);
  }
  to{
    transform: translateY(0px);
  }
}
</style>
