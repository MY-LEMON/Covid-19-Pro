<template>
  <div>
    <el-menu
        :default-active="activeIndex2"
        class="el-menu-demo"
        mode="horizontal"
        @select="handleSelect"
        background-color="#545c64"
        text-color="#fff"
        active-text-color="#ffd04b">
      <el-menu-item index="1" @click="jumpto('/')">主页</el-menu-item>
      <el-menu-item index="2" @click="jumpto('/News')">新闻</el-menu-item>
      <el-menu-item index="3" @click="jumpto('/QNA')">问答</el-menu-item>

    </el-menu>
  </div>
</template>

<script>
export default {
  name: 'eheader',
  data () {
    return {
      activeIndex: '1',
      activeIndex2: '1'
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
