<template>
  <div class="home">
    <p>Home {{item}}</p><br>
    <el-button type="primary" @click="search('新型冠状病毒肺炎有哪些症状')">主要按钮</el-button>
  </div>
</template>

<script>
// @ is an alias to /src
import {doSearch} from '../apis/search.js'
export default {
  name: 'Home',
  data(){
    return{
      a : '1',
      item: []
    }
  },
  components: {
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
