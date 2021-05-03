<template>
  <div style="margin-top: 0;margin-bottom: 10px">
    <el-menu
        :default-active="this.$parent.$route.path"
        class="el-menu-demo"
        mode="horizontal"
        @select="handleSelect"
        background-color="#ffffff"
        text-color="#878fa4"

        active-text-color="#2a64f5" >
      <el-menu-item index="/" @click="jumpto('/')">
        <h2 :class="this.$parent.$route.path==='/' ? 'selected': 'unselected'">
          主页
        </h2>
      </el-menu-item>
      <el-menu-item index="/News" @click="jumpto('/News')">
        <h2 :class="this.$parent.$route.path==='/News' ? 'selected': 'unselected'">
          新闻
        </h2>
      </el-menu-item>
      <el-menu-item index="/QNA" @click="jumpto('/QNA')">
        <h2 :class="this.$parent.$route.path==='/QNA' ? 'selected': 'unselected'">
          问答
        </h2>
      </el-menu-item>
      <el-menu-item index="/SelfService" @click="jumpto('/SelfService')">
        <h2 :class="this.$parent.$route.path==='/SelfService' ? 'selected': 'unselected'">
          自诊
        </h2>
      </el-menu-item>
      <a href="#/">
      <img src="../imgs/logo-text.png" height="15%" width="15%" style="float: right"/>
<!--      <img src="../imgs/logo.png" height="5%" width="5%" style="float: right; margin: inherit"/>-->
      </a>
    </el-menu>
  </div>
</template>

<script>
export default {
  name: 'eheader',
  data () {
    return {

    }
  },
  methods: {
    handleSelect (key, keyPath) {
      console.log(key, keyPath)
    },
    jumpto (arg) {
      this.$router.push({
        path: arg
      })
    }
  }
}
</script>

<style>
.el-menu-item>h2{
  margin: 0
}
.selected{
  font-weight: bold;
}
.unselected{
  font-weight: lighter;
}
</style>
