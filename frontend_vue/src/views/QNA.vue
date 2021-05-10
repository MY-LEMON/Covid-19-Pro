<template>

    <el-container v-loading="loading" style="height: 100%; ">
      <el-header style="height: 10%">
        <el-input placeholder="请输入疫情相关问题" v-model="input" :class="isLoaded?'b2t':'t2b'" style="width: 80%;top: 15px" >

          <el-button @click="submit" slot="append" icon="el-icon-search"></el-button>
        </el-input>
      </el-header>
<!--    <el-container v-if="isLoaded">-->

<!--      <el-aside width="30%" v-if="isSearched">-->
<!--        <el-card>-->
<!--        {{textdata}}-->
<!--        </el-card>-->
<!--      </el-aside>-->
<!--        <el-main v-if="isSearched">-->
<!--          <el-card>-->
<!--          <Kgraph  v-bind:graph_json_data="graphdata" ></Kgraph>-->
<!--          </el-card>-->
<!--        </el-main>-->

<!--      <div v-if="!isSearched">-->
<!--        <h3>未搜索到结果</h3>-->
<!--      </div>-->
<!--    </el-container>-->
      <div v-if="!isLoaded">

        <img src="../imgs/QNAimg.png" /></div>
    <div v-if="isLoaded" style="height: 90%">
      <el-row v-if="isSearched" :gutter="10" style="height: 100%">
        <el-col :span="6" style="height: 100%">
          <el-card :class="isLoaded?'b2t':'t2b'" style="height: 98%;width: 100%; overflow-y: auto" >
            <p>
              {{textdata}}
            </p>

          </el-card>

        </el-col>
        <el-col :span="18" style="height: 100%">
          <el-card :class="isLoaded?'b2t':'t2b'" style=" width: 100%; height: 98%">
            <Kgraph  v-bind:graph_json_data="graphdata" ></Kgraph>
          </el-card>
        </el-col>
      </el-row >
      <el-row v-if="!isSearched" style="height: 100%" type="flex" justify="center" :class="isLoaded?'b2t':'t2b'">
        <el-card>
          <h3>未搜索到结果</h3>
        </el-card>
      </el-row>
    </div>
    </el-container>



</template>

<script>
// import {doSearch} from "@/apis/search";
import Kgraph from "../components/kgraph.vue";
import axios from "axios";
export default {
  name: 'QNA',
  props:{
    // graphdata:{
    //   type: Object,
    //   require: true
    // },
    // textdata:{
    //   type: Object,
    //   require: true
    // }
  },
  data(){
    return{
      graphdata:{},
      textdata:{},
      loading: false,
      input:"",
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
