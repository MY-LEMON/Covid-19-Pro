<template>
  <div class="div" v-if="isloaded">
    <Kgraph  v-bind:graph_json_data="graphdata"></Kgraph>
  </div>
</template>

<script>
import {doSearch} from "@/apis/search";
import Kgraph from "../components/kgraph.vue";
export default {
  name: 'QNA',
  props:{
    graphdata:{
      type: Object,
      require: true
    }
  },
  data(){
    return{
      isloaded: false
    }
  },
beforeMount() {
    console.log("QNA page mounting")
  doSearch("https://b2f65068-d22f-4c9e-81c6-2faa7d5cb2bd.mock.pstmn.io/qna").then(resp=>{
    console.log("loading data")
    this.graphdata = resp.data.data[1]
    this.isloaded = true
  })
},
  mounted() {
    console.log("QNA page mounted")
  },
  components: {
    Kgraph
  }
}
</script>

<style scoped>

</style>
