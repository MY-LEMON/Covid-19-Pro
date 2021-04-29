<template>
  <div class="infinite-list-wrapper" style="overflow: auto; height: auto;">
    <div
        class="list"
        v-infinite-scroll="load"
        infinite-scroll-disabled="disabled"
        style="overflow: auto; height: 500px">

      <el-row v-for="i in data" :key="i.id" class="list-item">


        <el-col :span="12" :offset="4">
          <div >
              <p>{{i.abstract}}</p>
          </div>
        </el-col>
        <el-col :span="4" >
          <div >
            <el-image
              style="width: 100px; height: 100px"
              :src=i.imgs[0]
              ></el-image>
          </div>
        </el-col>

      </el-row>

    </div>
    <div style="height: auto">
      <p v-if="!loading && !noMore"></p>
      <p v-if="loading">加载中...</p>
      <p v-if="noMore">没有更多了</p></div>
  </div>
</template>

<script>
import {doSearch} from '../apis/search.js'
export default {
  data () {
    return {
      index:0,
      count: 0,
      loading: false,
      data:[]
    }
  },
  computed: {
    noMore () {
      return this.count >= 10
    },
    disabled () {
      return this.loading || this.noMore
    }
  },
  methods: {
    getdata(){
      doSearch('/News').then(resp=>{
        // console.log(resp.data.data);
        for (let i = 0; i < resp.data.data.length; i++) {
          var temp = resp.data.data[i];
          temp.id += this.data.length;
          this.data.push(temp);
        }
        this.count += 3
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
</style>
