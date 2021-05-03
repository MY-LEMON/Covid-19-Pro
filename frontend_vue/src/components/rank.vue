<template>
  <div id="mychart5" style="width: 600px;height: 400px"></div>
</template>

<script>
import * as echarts from "echarts";

export default {
  name: "rank",
  props:{
    resq:{
      type: Object,
      require:true
    }
  },
  data(){
    return {
      options:{
        title:{
          text:'现存确诊前十省份'
        },
        tooltip:{
          trigger:'item',
          formatter: "{b}:</br>{a}{c}人"
        },
        xAxis:{
          show:false
        },
        yAxis:{
          inverse:true,
          type:'category',
          data:[],
          axisTick:{show:false},
          axisLine:{show:false}
        },
        series:[{
          name:'现存确诊',
          type:'bar',
          barWidth:'70%',
          itemStyle:{
            normal: {
              color: new echarts.graphic.LinearGradient(1,
                  0, 0, 1, [{
                    offset: 0,
                    color: '#2A6BCD'
                  }, {
                    offset: 1,
                    color: '#34F6F8'
                  }])
            }
          },
          data:[],
          label:{
            show:true,
            position:'right',
            formatter:'{c}',
            color:'black'
          },
          emphasis:{
            itemStyle:{
              opacity:0.4//透明度
            }
          }
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
      this.chart = echarts.init(document.getElementById('mychart5'))
      this.chart.setOption(this.options)
    },
    getData(resq){
      this.options.yAxis.data = resq['country'].slice(0,10)
      this.options.series[0].data = resq['data'].slice(0,10)
    }
  }
}
</script>

<style scoped>

</style>