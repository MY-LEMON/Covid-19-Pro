<template>
  <div>
    <div ref="myPage" style="height:calc(100vh - 50px);">
      <SeeksRelationGraph
          ref="seeksRelationGraph"
          :options="graphOptions"
          :on-node-click="onNodeClick"
          :on-line-click="onLineClick">
        <div slot="node" slot-scope="{node}" @mouseover="showNodeTips(node, $event)" @mouseout="hideNodeTips(node, $event)">
          <div style="color: rgb(255,255,255);letter-spacing:1pt;line-height:100%;font-weight:bold;text-align:center;vertical-align:middle;
          font-size: 22px;border-radius: 32px;cursor: pointer;
          width: 80px;
            margin-top:10px; /*上边界*/
            margin-bottom:10px; /*下边界值*/
            /*border: 1px solid red;*/
            padding: 0.1px 0.1px;
          ">
<!--            <i style="font-size: 30px;" :class="node.data.myicon" />-->
            {{ node.data['label_zh'] }}
          </div>
<!--          <div style="color: rgb(255,255,255);font-size: 16px;position: absolute;width: 160px;height:25px;line-height: 25px;margin-top:5px;margin-left:-48px;text-align: center;background-color: rgba(7,23,83,0.85);">-->
<!--            {{ node.data['症状'] }}-->
<!--          </div>-->
        </div>
        <div slot="bottomPanel" style="border-top:#efefef solid 1px;height:60px;line-height: 60px;text-align: center;font-size: 18px;background-color: #ffffff;">
          知识图谱与精准问答
        </div>
      </SeeksRelationGraph>
    </div>
    <div v-if="isShowNodeTipsPanel" :style="{left: nodeMenuPanelPosition.x + 'px', top: nodeMenuPanelPosition.y + 'px' }" style="z-index: 999;padding:10px;background-color: #ffffff;border:#eeeeee solid 1px;box-shadow: 0px 0px 8px #cccccc;position: absolute;">
      <div style="line-height: 25px;padding-left: 10px;color: #888888;font-size: 12px;">名称：{{currentNode.text}}</div>

      <!--eslint-disable-next-line-->
      <div v-for="(item,key) of currentNode.data" class="c-node-menu-item">{{key}} : {{item}}</div>
    </div>
  </div>
</template>

<script>
import SeeksRelationGraph from 'relation-graph';
// import {doSearch} from "@/apis/search";

export default {
  name: 'kgraph',
  components: { SeeksRelationGraph },
  props:{
    graph_json_data:{
      type: Object,
      require: true
    },
  },
  data() {
    return {

      isShowCodePanel: false,
      isShowNodeTipsPanel: false,
      allowShowMiniToolBar:false,
      allowShowMiniNameFilter:true,
      moveToCenterWhenResize:false,
      nodeMenuPanelPosition: { x: 0, y: 0 },
      currentNode: {},
      graphOptions: {
        allowSwitchLineShape: true,
        allowSwitchJunctionPoint: true,
        'layouts': [
          {
            'label': '自动布局',
            'layoutName': 'force',
            'layoutClassName': 'seeks-layout-force'
          }
        ],
        defaultJunctionPoint: 'border',
        defaultNodeColor:'rgb(34,69,168)',
        defaultNodeBorderColor:'rgba(94,130,238,0.77)',
        // 这里可以参考"Graph 图谱"中的参数进行设置
      }
    }
  },
  mounted() {
    // doSearch("https://b2f65068-d22f-4c9e-81c6-2faa7d5cb2bd.mock.pstmn.io/qna").then(resp=>{
    //   var graphdata = resp.data.data[1]
    //   // console.log(graphdata)
    //   // var content = resp.data.data[1]
    //   this.load(graphdata)
    // }).then(()=>{})

    // this.load(temp)
    // this.load()

    console.log(this.graph_json_data)
    console.log("kgraph mounted")
    this.showSeeksGraph()
  },
  // updated() {
  //   this.showSeeksGraph()
  // },
  methods: {
    load(data){
      this.graph_json_data = data
    },
    showSeeksGraph() {
          this.$refs.seeksRelationGraph.setJsonData(this.graph_json_data, () => {
        // 这些写上当图谱初始化完成后需要执行的代码
      })
    },
    onNodeClick(nodeObject) {
      console.log('onNodeClick:', nodeObject)
    },
    onLineClick(lineObject) {
      console.log('onLineClick:', lineObject)
    },
    showNodeTips(nodeObject, $event) {
      this.currentNode = nodeObject
      var _base_position = this.$refs.myPage.getBoundingClientRect()
      console.log('showNodeMenus:', $event, _base_position)
      this.isShowNodeTipsPanel = true
      this.nodeMenuPanelPosition.x = $event.clientX - _base_position.x + 10
      this.nodeMenuPanelPosition.y = $event.clientY - _base_position.y + 10
    },
    hideNodeTips() {
      this.isShowNodeTipsPanel = false
    }
  }
}
</script>

<style lang="scss">
</style>

<style lang="scss" scoped>
.c-node-menu-item{
  line-height: 30px;padding-left: 10px;cursor: pointer;color: #444444;font-size: 14px;border-top:#efefef solid 1px;
}
.c-node-menu-item:hover{
  background-color: rgba(66, 110, 187, 0.2);
}
</style>
