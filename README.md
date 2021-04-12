# Covid-19-Pro

## ”知疫情“ 新冠疫情信息整合系统

项目整体参考：



#### 开发IDE（推荐）：

Pycharm（后端）

Webstorm（前端）

注：jet的账号可以申请学生账号，免费用pro一年

#### 前端开发：

基于Vue 3.0以上，使用Vue-cli进行开发

##### Web快速开发：

bootstrap-vue：页面栅格，主要组件，图标库

echarts：绘制图表，如新冠地图，确诊人数。。。

relation-graph：知识图谱关系图绘制

axios：HTTP库

#### 后端开发：

基于flask框架

##### 数据库：

MySQL：存放新闻信息、用户账密等信息

Neo4j：图数据库，存放知识图谱

##### 数据接口加密：

rsa



### 接口格式：

1.返回的是json数据
2.结构如下
{
    resCode： 0, # 非0即错误 1
    data： # 数据位置，一般为数组
    message： '对本次请求的说明'
}

