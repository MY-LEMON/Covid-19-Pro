<template>
      <div class="left_map" id="left_map"  @click="showChina" style="width: 900px;height: 700px"></div>
</template>

<script>
import * as echarts from "echarts";
import '/node_modules/echarts/china.js' //地图数据
import axios from 'axios'


var toPy = ['heilongjiang','jilin','liaoning','neimenggu','xinjiang','xizang',
  'qinghai','gansu','sichuan','yunnan','shanxi','shanxi1','hebei','beijing',
  'tianjin','henan','shandong','anhui','jiangsu','hubei','hunan','chongqing',
  'guizhou','guangdong','guangxi','zhejiang','jiangxi','fujian','taiwan',
  'hainan','shanghai','aomen','xianggang','ningxia']
var province=['黑龙江','吉林','辽宁','内蒙古','新疆','西藏','青海','甘肃','四川','云南','山西','陕西','河北','北京','天津','河南','山东','安徽',
  '江苏','湖北','湖南','重庆','贵州','广东','广西','浙江','江西','福建','台湾','海南','上海','澳门','香港','宁夏']

var chinaData=[{'name': '四川', 'value': [968, 14, 948, 3, 17]},
  {'name': '重庆', 'value': [594, 15, 585, 6, 3]},
  {'name': '江苏', 'value': [717, 3, 708, 0, 9]},
  {'name': '陕西', 'value': [588, 1, 568, 3, 17]},
  {'name': '中国', 'value': [103441, 0, 98052, 4856, 533]},
  {'name': '云南', 'value': [338, 2, 278, 2, 58]},
  {'name': '上海', 'value': [1958, 393, 1892, 7, 59]},
  {'name': '广东', 'value': [2328, 14, 2275, 8, 45]},
  {'name': '台湾', 'value': [1090, 431, 1044, 11, 35]},
  {'name': '香港', 'value': [11727, 176, 11325, 209, 193]},
  {'name': '福建', 'value': [586, 3, 561, 1, 24]},
  {'name': '辽宁', 'value': [408, 0, 406, 2, 0]},
  {'name': '浙江', 'value': [1331, 3, 1320, 1, 10]},
  {'name': '天津', 'value': [383, 50, 372, 3, 8]},
  {'name': '澳门', 'value': [49, 9, 49, 0, 0]},
  {'name': '山西', 'value': [249, 64, 242, 0, 7]},
  {'name': '湖北', 'value': [68157, 0, 63640, 4512, 5]},
  {'name': '河北', 'value': [1317, 0, 1310, 7, 0]},
  {'name': '宁夏', 'value': [75, 0, 75, 0, 0]},
  {'name': '青海', 'value': [18, 0, 18, 0, 0]},
  {'name': '内蒙古', 'value': [379, 34, 376, 1, 2]},
  {'name': '海南', 'value': [187, 0, 165, 6, 16]},
  {'name': '河南', 'value': [1312, 0, 1285, 22, 5]},
  {'name': '湖南', 'value': [1044, 0, 1036, 4, 4]},
  {'name': '山东', 'value': [876, 14, 862, 7, 7]},
  {'name': '黑龙江', 'value': [1610, 394, 1597, 13, 0]},
  {'name': '江西', 'value': [937, 0, 936, 1, 0]},
  {'name': '吉林', 'value': [573, 19, 570, 3, 0]},
  {'name': '甘肃', 'value': [193, 0, 190, 2, 1]},
  {'name': '北京', 'value': [1057, 164, 1038, 9, 10]},
  {'name': '广西', 'value': [270, 0, 265, 2, 3]},
  {'name': '西藏', 'value': [1, 0, 1, 0, 0]},
  {'name': '安徽', 'value': [994, 0, 988, 6, 0]},
  {'name': '新疆', 'value': [980, 0, 977, 3, 0]},
  {'name': '贵州', 'value': [147, 0, 145, 2, 0]}]
var provinceData={'shanxi':[{'name':'太原市','value':[1,2,3,5,6]},{'name':'临汾市','value':[5,6,8,7,9]},{}],'shanxi1':[],'jilin':[{}]}
//var shanxiData=[{'name':'太原市','value':[1,2,3,5,6]}]

export default {
  name: "test",
  data(){
    return{
      options:{}
    }
  },
  mounted() {
    this.loadData()
    this.initMychart()
  },
  methods:{
    loadData(China,province){
      chinaData = China
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
            borderColor:'rgba(185,204,222,0.8)'
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
          //data:this.getData([{name:'北京',value:[1,2,3,5,5]}])
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
          backgroundColor:'rgba(167,157,50,0.9)',
          borderColor: 'rgb(118,13,222)'
        }
      }
      console.log(option.series[0].data)
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
      //console.log(this.provincemap)
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