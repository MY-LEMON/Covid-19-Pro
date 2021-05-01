<template>
  <div>
    <p>1. 您好，请告诉我您现在是否有以下的症状</p>
    <el-checkbox-group v-model="checkList" >
      <el-checkbox :label="0">发烧（腋窝温度高于37℃）</el-checkbox>
      <el-checkbox :label="1">干咳</el-checkbox>
      <el-checkbox :label="2">乏力</el-checkbox>
      <el-checkbox :label="3">鼻塞</el-checkbox>
      <el-checkbox :label="4">流涕</el-checkbox>
      <el-checkbox :label="5">咽痛</el-checkbox>
      <el-checkbox :label="6">腹泻</el-checkbox>
      <el-checkbox :label="7">其他</el-checkbox>
    </el-checkbox-group>
    <p>2.请问前两周您有否去过新冠确诊人数比较密集的地区？</p>
    <el-radio-group v-model="radio">
      <el-radio :label="8">去过</el-radio>
      <el-radio :label="9">没去过</el-radio>
    </el-radio-group>
    <p>3.请您回忆在最近两周的情况</p>
    <el-checkbox-group v-model="checkList" >
      <el-checkbox :label="10">是否接触过来自新冠确诊人数比较密集地区的人。</el-checkbox>
      <el-checkbox :label="11">与您接触的家人、朋友、同事中，是否有至少一个人有上述症状？</el-checkbox>
      <el-checkbox :label="12">是否曾接触、探视、照顾过疑似或确诊病人？</el-checkbox>
      <el-checkbox :label="13">您居住的小区内是否有确诊病人？ </el-checkbox>
    </el-checkbox-group>
    <p>4.请告诉我您是否有以下疾病或者症状</p>
    <el-checkbox-group v-model="checkList" >
      <el-checkbox :label="14">高血压</el-checkbox>
      <el-checkbox :label="15">冠心病/心衰</el-checkbox>
      <el-checkbox :label="16">糖尿病</el-checkbox>
      <el-checkbox :label="17">慢性肾脏疾病/肾衰（中医中的肾虚不包括在此）</el-checkbox>
      <el-checkbox :label="18">需要服用激素或者免疫抑制剂的疾病</el-checkbox>
      <el-checkbox :label="19">肿瘤</el-checkbox>
      <el-checkbox :label="20">肝硬化</el-checkbox>
      <el-checkbox :label="21">慢性肺病（肺纤维化、COPD、呼衰等）</el-checkbox>
      <el-checkbox :label="22">脑血管疾病</el-checkbox>
    </el-checkbox-group>

    <el-button @click="submit">submit</el-button>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "SelfService",
  data(){
    return{
      radio: 0,
      checkList:[]
    }
  },
  methods:{
    submit(){
      this.checkList.push(this.radio)
      axios.get("/selfservice",{
      params :{
        "self_test":this.checkList.toString()
      }
      }).then(ans=>{
        alert(ans)
      })
    }
  }
}
</script>

<style scoped>

</style>
