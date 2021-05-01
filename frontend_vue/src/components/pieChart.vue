<template>
  <div id="mychart3" style="width: 600px;height: 400px"></div>
</template>

<script>
import * as echarts from "echarts";

let Province=['黑龙江省','吉林省','辽宁省','内蒙古自治区','新疆维吾尔自治区','西藏自治区','青海省','甘肃省','四川省','云南省','山西省','陕西省','河北省',
  '北京市','天津市','河南省','山东省','安徽省',
  '江苏省','湖北省','湖南省','重庆市','贵州省','广东省','广西壮族自治区','浙江省','江西省','福建省','台湾','海南省','上海市','澳门','香港','宁夏省']

export default {
  name: "piechart",
  props:{
    resq:{
      type: Object,
      require:true
    }
  },
  data(){
    return{
      options:{
        legend:{
          data: Province,
          type:'scroll',
          left:'right',
          orient:'vertical'
        },
        title:{
          text:'各省确诊人数占比'
        },
        tooltip:{
          trigger:'item',
          formatter:'{a}</br>{b} : {c}人</br>全国占比 : {d}%',
          backgroundColor:'rgb(109,226,101,0.6)'
        },
        series:[{
          name:'累计确诊',
          label:{
            position:'center',
            fontSize:30,
            show:false
          },
          type:'pie',
          emphasis:{
            scaleSize:12,
            itemStyle:{
              borderColor:'#e3d8d8',
              borderWidth: 2
            },
            label:{
              show:true,

            }
          },
          radius:['50%','80%'],
          data:[
            {
              name:'黑龙江省',
              value:[]
            },{
              name:'吉林省',
              value:[]
            },{
              name:'辽宁省',
              value: []
            },{
              name:'内蒙古',
              value: []
            },{
              name:'新疆维吾尔自治区',
              value: []
            },{
              name:'西藏自治区',
              value: []
            },{
              name:'青海省',
              value: []
            },{
              name:'甘肃省',
              value: []
            },{
              name:'四川省',
              value: []
            },{
              name:'云南省',
              value: []
            },{
              name:'山西省',
              value: []
            },{
              name:'陕西省',
              value: []
            },{
              name:'河北省',
              value: []
            },{
              name:'北京市',
              value: []
            },{
              name:'天津市',
              value: []
            },{
              name:'河南省',
              value: []
            },{
              name:'山东省',
              value: []
            },{
              name:'安徽省',
              value: []
            },{
              name:'江苏省',
              value: []
            },{
              name:'湖北省',
              value: []
            },{
              name:'湖南省',
              value: []
            },{
              name:'重庆市',
              value: []
            },{
              name:'贵州省',
              value: []
            },{
              name:'广东省',
              value: []
            },{
              name:'广西省',
              value: []
            },{
              name:'浙江省',
              value: []
            },{
              name:'江西省',
              value: []
            },{
              name:'福建省',
              value: []
            },{
              name:'台湾',
              value: []
            },{
              name:'海南省',
              value: []
            },{
              name:'上海市',
              value: []
            },{
              name:'澳门',
              value: []
            },{
              name:'香港',
              value: []
            },{
              name:'宁夏省',
              value: []
            }]
        }]
      }
    }
  },
  mounted() {
    this.getData(this.resq)
    this.getChart()
  },
  methods:{
    getChart(){
      this.chart = echarts.init(document.getElementById('mychart3'))
      this.chart.setOption(this.options)
    },
    getData(resq) {
      for (var i = 0; i < 34; i++)
      {
        this.options.series[0].data[i].value = resq[Province[i]]
      }
    }
  }
}
</script>

<style scoped>

</style>