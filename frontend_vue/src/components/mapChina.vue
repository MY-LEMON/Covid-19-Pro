<template>
  <div class="left_map" id="left_map"  @click="showChina" style="width: 900px;height: 700px"></div>
</template>

<script>
import * as echarts from "echarts";
import '/node_modules/echarts/china.js' //地图数据
import axios from 'axios'


var toPy = ['Heilongjiang','Jilin','Liaoning','Neimenggu','Xinjiang','Xizang',
  'Qinghai','Gansu','Sichuan','Yunnan','Shanxi','Shanxi1','Hebei','Beijing',
  'Tianjin','Henan','Shandong','Anhui','Jiangsu','Hubei','Hunan','Chongqing',
  'Guizhou','Guangdong','Guangxi','Zhejiang','Jiangxi','Fujian','Taiwan',
  'Hainan','Shanghai','Aomen','Xianggang','Ningxia']
var province=['黑龙江','吉林','辽宁','内蒙古','新疆','西藏','青海','甘肃','四川','云南','山西','陕西','河北','北京','天津','河南','山东','安徽',
  '江苏','湖北','湖南','重庆','贵州','广东','广西','浙江','江西','福建','台湾','海南','上海','澳门','香港','宁夏']

let chinaData
let provinceData
export default {
  name: "test",
  props:{
    china:{
      type: Object,
      require: true
    },
    province:{
      type:Object,
      require:true
    }
  },
  data(){
    return{
      options:{}
    }
  },
  mounted() {
    this.loadData(this.china,this.province)
    this.initMychart()
  },
  methods:{
    loadData(China,province){
      chinaData = China
      for(var i =0;i<province['Henan'].length;i++) {
        province['Henan'][i].name = province['Henan'][i].name + "市"
      }
      for(var j =0;j<province['Guangdong'].length;j++) {
        province['Guangdong'][j].name = province['Guangdong'][j].name + "市"
      }
      province['Guangdong'].push({"name":"云浮市","value":[2,0,2,0,0]})
      provinceData = province
    },
    //获取一个json对象，动态为series的数据
    getData(place){
      if (place==='china')
      {
        return chinaData
      }
      else{
        return provinceData[place]
      }
    },

    //获取option的方法
    getMapOption(place){
      let option = this.options = {
        title:{
          text:'疫情地图'
        },
//----------地图型-------------
        series:[{
          name:'确诊人数',
          type:'map',
          map:place?place:'china',
          label:{
            show:true,
            color:"#333",
            fontsize:10,
            position:'top'
          },
          itemStyle:{
            areaColor:'#eee',
            borderColor:'rgba(117,164,208,0.8)'
          },
          roam:true,
          zoom:1.2,
          emphasis:{//鼠标cover对应的样式
            label:{
              color:'#fff',
              fontSize:12
            },
            itemStyle:{
              areaColor:'#83b5e7'   //  滑动到哪个地区就显示蓝色
            }
          },
          data:this.getData(place?place:'china')
        }
        ],
//----------------------visualMap--------
        visualMap:{
          type:'piecewise',
          show:true,
          pieces:[           // 分段
            {min:10000},
            {min:1000,max:9999},
            {min:100,max:999},
            {min:10,max:99},
            {min:1,max:9}
          ]
        },
        inRange:{
          symbol:'rect',
          color:['#ffc7b1','#9c0505']   //   浅红~~深红色
        },
        itemWidth:20,
        itemHeight:10,
        tooltip:{
          trigger:'item',
          formatter:function (params){
            return params.name+'</br>累计确诊：'+params.data.value[0]+'</br>疑似人数：'+params.data.value[1]+
                '</br>治愈：'+params.data.value[2]+'</br>死亡人数：'+params.data.value[3]+'</br>现存人数：'+params.data.value[4]
          },
          backgroundColor:'rgba(204,231,187,0.9)',
          borderColor: 'rgb(118,13,222)'
        }
      }
      this.map.setOption(option,true)
      //return option
    },

    //中国地图绘制
    showChina(){
      this.getMapOption()
    },

    //省份地图的绘制
    provincemap(pname){
      console.log(pname)
      let index
      for (let i=0;i<34;i++)
      {
        if(province[i]===pname) {
          index = i
          break
        }
      }
      let provincePy = toPy[index]
      axios.get('/json/province/'+provincePy+'.json').then((s)=>{
        echarts.registerMap(provincePy,s.data)
        this.getMapOption(provincePy)
      })
    },

    //初始化mychart
    initMychart(){

      this.map = echarts.init(document.getElementById('left_map'))
      this.getMapOption()
      this.map.on('click',(param)=>{
        this.provincemap(param.name)
      })
    }
  }
}
</script>

<style scoped>
.left_map {
  width: 100%;
  height: 1000px;
}

</style>