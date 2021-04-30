<template>
  <div>
    <p>nihao?</p>
    <el-radio-group v-model="radio">
      <el-radio :label="3" @click="test">备选项</el-radio>
      <el-radio :label="6" @click="test">备选项</el-radio>
      <el-radio :label="9" @select="test">备选项</el-radio>
    </el-radio-group>
  </div>
</template>

<script>
export default {
  name: "SelfService",
  data(){
    return{
      radio: 0
    }
  },
  methods:{
    test(){
      console.log(this.radio)
    }
  }
}
</script>

<style scoped>

</style>
