<template>
  <div class="home">
<!--    <Kgraph></Kgraph>-->
    <p>Home {{item}}</p><br>
    <el-button type="primary" @click="search('qna')">主要按钮</el-button>
  </div>
</template>

<script>
// @ is an alias to /src
import {doSearch} from '../apis/search.js'
// import Kgraph from "./components/kgraph";
export default {
  name: 'Home',
  data(){
    return{
      a : '1',
      item: []
    }
  },
  components: {
    // Kgraph
  },
  methods: {
    search(key){
      doSearch(key).then(resp=>{
        this.item = 'done'
        console.log(resp.data)
      })
    }
  }
}
</script>
