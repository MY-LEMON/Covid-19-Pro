<template>
  <div style="margin-top: 0;margin-bottom: 10px">
    <el-menu
        :default-active="this.$parent.$route.path"
        class="el-menu-demo"
        mode="horizontal"
        @select="handleSelect"
        background-color="#545c64"
        text-color="#fff"
        active-text-color="#ffd04b" >
      <el-menu-item index="/" @click="jumpto('/')">主页</el-menu-item>
      <el-menu-item index="/News" @click="jumpto('/News')">新闻</el-menu-item>
      <el-menu-item index="/QNA" @click="jumpto('/QNA')">问答</el-menu-item>
      <el-menu-item index="/SelfService" @click="jumpto('/SelfService')">自诊</el-menu-item>
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

<style scoped>

</style>
