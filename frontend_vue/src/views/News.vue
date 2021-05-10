<template>
  <div class="infinite-list-wrapper" style="overflow: auto; height: 100%;">
    <div
        class="list"
        v-infinite-scroll="load"
        infinite-scroll-disabled="disabled"
        style="overflow: auto; height: 90%">

      <el-row v-for="i in data" :key="i.id" class="list-item" type="flex" justify="center">
        <el-card>
          <el-col :span="12" :offset="4">
            <el-link :href="i.src" >
              <p>{{i.abstract}}</p>
            </el-link>
          </el-col>
          <el-col :span="4" >
            <div >
              <el-image
                  style=" height: 100px"
                  :src=i.imgs[0]
                  fit= contain
              ></el-image>
            </div>
          </el-col>
        </el-card>

      </el-row>

    </div>
    <div style="height: auto">
      <p v-if="!loading && !noMore"></p>
      <p v-if="loading">加载中...</p>
      <p v-if="noMore">没有更多了</p></div>
  </div>
</template>

<script>
// import {doSearch} from '../apis/search.js'
import axios from "axios";

export default {
  data () {
    return {
      count: 0,
      num:5,
      loading: false,
      data:[]
    }
  },
  computed: {
    noMore () {
      return false
    },
    disabled () {
      return this.loading || this.noMore
    }
  },
  methods: {
    getdata(){
      axios.get('http://127.0.0.1:5000/news',{
        params:{
          "from":this.count,
          "to":this.count+this.num
        }
      }).then(resp=>{
        console.log(resp.data);
        for (let i = 0; i < resp.data.data.length; i++) {
          var temp = resp.data.data[i];
          temp.id += this.data.length;
          this.data.push(temp);
        }
        this.count += resp.data.data.length
      });
      // console.log(this);
    },

    load () {
      this.loading = true
      setTimeout(() => {
        this.getdata();
        this.loading = false
      }, 50)
    }
  }
}
</script>
<style>
.el-row {
  margin-bottom: 20px;
&:last-child {
   margin-bottom: 0;
 }
}
.el-col {
  border-radius: 4px;
}
.bg-purple-dark {
  background: #99a9bf;
}
.bg-purple {
  background: #d3dce6;
}
.bg-purple-light {
  background: #e5e9f2;
}
.grid-content {
  border-radius: 4px;
  min-height: 36px;
}
.row-bg {
  padding: 10px 0;
  background-color: #f9fafc;
}
.el-card{
  width: 60%;
}
</style>
