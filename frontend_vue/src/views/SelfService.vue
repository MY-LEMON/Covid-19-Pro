<template>
  <div style=" overflow: auto;height: 100%">
    <div style="height: 90%">
<!--    <el-container>-->
<!--      <el-row>-->
<!--        <el-col :span="24">-->
<!--          <p>1. 您好，请告诉我您现在是否有以下的症状</p>-->
<!--        </el-col>-->
<!--      </el-row>-->
<!--      <el-row>-->
<!--        <el-col :span="24">-->
<!--          <el-checkbox-group v-model="checkList" >-->
<!--            <el-checkbox :label="0">发烧（腋窝温度高于37℃）</el-checkbox>-->
<!--            <el-checkbox :label="1">干咳</el-checkbox>-->
<!--            <el-checkbox :label="2">乏力</el-checkbox>-->
<!--            <el-checkbox :label="3">鼻塞</el-checkbox><br>-->
<!--            <el-checkbox :label="4">流涕</el-checkbox>-->
<!--            <el-checkbox :label="5">咽痛</el-checkbox>-->
<!--            <el-checkbox :label="6">腹泻</el-checkbox>-->
<!--            <el-checkbox :label="7">其他</el-checkbox>-->
<!--          </el-checkbox-group>-->
<!--        </el-col>-->
<!--      </el-row>-->
<!--    </el-container>-->
<!--    <el-container>-->
<!--      <el-row>-->
<!--        <p>2.请问前两周您有否去过新冠确诊人数比较密集的地区？</p>-->
<!--      </el-row>-->
<!--      <el-row>-->
<!--        <el-radio-group v-model="radio">-->
<!--          <el-radio :label="8">去过</el-radio>-->
<!--          <el-radio :label="9">没去过</el-radio>-->
<!--        </el-radio-group>-->
<!--      </el-row>-->
<!--    </el-container>-->
<!--    <el-container>-->
<!--      <el-row>-->
<!--        <div><p>3.请您回忆在最近两周的情况</p></div>-->
<!--      </el-row>-->
<!--      <el-row>-->
<!--        <el-checkbox-group v-model="checkList" >-->
<!--          <el-checkbox :label="10">是否接触过来自新冠确诊人数比较密集地区的人。</el-checkbox><br>-->
<!--          <el-checkbox :label="11">与您接触的家人、朋友、同事中，是否有至少一个人有上述症状？</el-checkbox><br>-->
<!--          <el-checkbox :label="12">是否曾接触、探视、照顾过疑似或确诊病人？</el-checkbox><br>-->
<!--          <el-checkbox :label="13">您居住的小区内是否有确诊病人？ </el-checkbox><br>-->
<!--        </el-checkbox-group>-->
<!--      </el-row>-->
<!--    </el-container>-->
<!--    <el-container>-->
<!--      <el-row>-->
<!--        <p>4.请告诉我您是否有以下疾病或者症状</p>-->
<!--      </el-row>-->
<!--      <el-row>-->
<!--        <el-checkbox-group v-model="checkList" >-->
<!--          <el-checkbox :label="14">高血压</el-checkbox>-->
<!--          <el-checkbox :label="15">冠心病/心衰</el-checkbox>-->
<!--          <el-checkbox :label="16">糖尿病</el-checkbox>-->
<!--          <el-checkbox :label="17">慢性肾脏疾病/肾衰（中医中的肾虚不包括在此）</el-checkbox>-->
<!--          <el-checkbox :label="18">需要服用激素或者免疫抑制剂的疾病</el-checkbox>-->
<!--          <el-checkbox :label="19">肿瘤</el-checkbox>-->
<!--          <el-checkbox :label="20">肝硬化</el-checkbox>-->
<!--          <el-checkbox :label="21">慢性肺病（肺纤维化、COPD、呼衰等）</el-checkbox>-->
<!--          <el-checkbox :label="22">脑血管疾病</el-checkbox>-->
<!--        </el-checkbox-group>-->
<!--      </el-row>-->
<!--    </el-container>-->

<!--    <el-button @click="submit">submit</el-button>-->
<!--*****************-->
    <el-row>
      <el-col :span="24">
        <div >
          <el-row>
            <el-col :span="24">
              <img src="../imgs/selfservice.png" height="420" width="750"/></el-col>
          </el-row>
          <el-row>
            <el-col :span="18" :offset="3">
              <p style="font-weight: lighter">本自测系统是基于流行病学史和个人症状，做出的建议性意见，仅供测试者参考。此测试不属于医疗范畴，不是医生诊疗行为，鉴于肺炎疫情的复杂性、客观条件的限制、个人认知的局限性、及诸多不可预见因素，测试结果可能存在偏差。如测试者出现肺炎疫情的典型症状，请根据所在国家官方机构的诊疗方案居家隔离或前往医疗机构就诊。本系统研发方及合作方不因此测试而与测试者形成任何合约、医疗或其他法律关系，不对测试结果的准确性、测试结果及官方医疗机构的检测结果的偏差承担任何责任。测试者知悉并接受以上，并自愿进行本自测系统测试。</p>
            </el-col>
          </el-row>
        </div>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="12" :offset="6">
        <div class="grid-content bg-purple-light">
          <el-row>
            <el-col :span="24">
              <p>1. 您好，请告诉我您现在是否有以下的症状</p>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="24">
              <el-checkbox-group v-model="checkList" >
                <el-checkbox :label="0">发烧（腋窝温度高于37℃）</el-checkbox>
                <el-checkbox :label="1">干咳</el-checkbox>
                <el-checkbox :label="2">乏力</el-checkbox>
                <el-checkbox :label="3">鼻塞</el-checkbox><br>
                <el-checkbox :label="4">流涕</el-checkbox>
                <el-checkbox :label="5">咽痛</el-checkbox>
                <el-checkbox :label="6">腹泻</el-checkbox>
                <el-checkbox :label="7">其他</el-checkbox>
              </el-checkbox-group>
            </el-col>
          </el-row>
        </div>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="12" :offset="6">
        <div class="grid-content bg-purple-light">
                <el-row>
                  <p>2.请问前两周您有否去过新冠确诊人数比较密集的地区？</p>
                </el-row>
                <el-row>
                  <el-radio-group v-model="radio">
                    <el-radio :label="8">去过</el-radio>
                    <el-radio :label="9">没去过</el-radio>
                  </el-radio-group>
                </el-row>
        </div>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="12" :offset="6">
        <div class="grid-content bg-purple-light">
                <el-row>
                  <div><p>3.请您回忆在最近两周的情况</p></div>
                </el-row>
                <el-row>
                  <el-checkbox-group v-model="checkList" >
                    <el-checkbox :label="10">是否接触过来自新冠确诊人数比较密集地区的人。</el-checkbox><br>
                    <el-checkbox :label="11">与您接触的家人、朋友、同事中，是否有至少一个人有上述症状？</el-checkbox><br>
                    <el-checkbox :label="12">是否曾接触、探视、照顾过疑似或确诊病人？</el-checkbox><br>
                    <el-checkbox :label="13">您居住的小区内是否有确诊病人？ </el-checkbox><br>
                  </el-checkbox-group>
                </el-row>
        </div>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="12" :offset="6">
        <div class="grid-content bg-purple-light">
                <el-row>
                  <p>4.请告诉我您是否有以下疾病或者症状</p>
                </el-row>
                <el-row>
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
                </el-row>
        </div>
      </el-col>
    </el-row>
    <el-row>
      <el-button type="primary" @click="submit">提交</el-button>
    </el-row>
    </div>
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
      if(this.radio!=0){
        this.checkList.push(this.radio)
      }
      axios.get("http://172.22.69.121:5000/selfservice",{
      params :{
        "self_test":this.checkList.toString()
      }
      }).then(ans=>{
        console.log(ans)
        this.$message({
          dangerouslyUseHTMLString: true,
          message:'<p style="line-height: 17px">'+ans.data.result1+'</p>',
          duration:8000,
          showClose:true,
          offset:120
        })
      })
    }
  }
}
</script>

<style>
/*.p{*/
/*  float: left;*/
/*}*/
/*.el-checkbox-group{*/
/*  float: left;*/
/*}*/
/*.el-checkbox{*/
/*  float: left;*/
/*}*/
</style>
