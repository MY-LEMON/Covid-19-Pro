<template>
  <div id="mychart6" style="width: 600px;height: 400px"></div>
</template>

<script>
import * as echarts from "echarts";

export default {
  name: "piechart_foreign",
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
          data: this.resq['country'],
          type:'scroll',
          left:'right',
          orient:'vertical'
        },
        title:{
          text:'各国确诊人数占比'
        },
        tooltip:{
          trigger:'item',
          formatter:'{a}</br>{b} : {c}人</br>全国占比 : {d}%',
          backgroundColor:'rgba(119,167,215,0.6)'
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
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },
            {
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
            },{
              name:'',
              value:[]
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
      this.chart = echarts.init(document.getElementById('mychart6'))
      this.chart.setOption(this.options)
    },
    getData(resq) {
      for (var i = 0; i < 100; i++)
      {
        this.options.series[0].data[i].name = resq['country'][i]
        this.options.series[0].data[i].value = resq['data'][i]
      }
    }
  }
}
</script>

<style scoped>

</style>
