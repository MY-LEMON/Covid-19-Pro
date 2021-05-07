# Covid-19-Pro”知疫情“ 新冠疫情信息问答与整合系统

## 1.简介

​	为了对抗蔓延全球的新冠肺炎疫情，开放而全面的数据资源可以帮助研究者、医疗工作者和普通民众更深入地了解病毒和疫情。由此，本系统收集了包括全球新冠肺炎感染者数据，新冠疫情相关新闻，新冠疫情相关信息等数据，并保持持续更新。我们将这些数据构建成了数据库，并在本系统进行可视化的展示。同时我们也收集整理了现有COVID-19开放知识图谱，并进一步融合了它们，构建了一个大规模、结构化新冠知识图谱。其包含了500个概念、400个属性、两万个实例和三万个知识三元组，覆盖了医疗、健康、物资、防控、科研和人物等领域。

​	本web系统采用了vue2.0+flask前后端分离的架构模式设计，主要分为四个模块：分别是：疫情大数据展示，基于知识图谱的疫情信息精准问答，疫情新闻浏览，病情自诊。

## 2.疫情大数据展示

​	首先是疫情大数据展示部分，我们从丁香园爬取了当日疫情数据，并经数据清洗后作为json文件保存到本地，最后通过开放接口的方式提供给前端进行可视化展示。如图，确诊人数较多的省或市，则对其用比较浓重的红色来着色，而人数较少的地区则用浅红来着色。我们可以通过鼠标悬停的方式查看具体信息，通过点击省份查看对应省份的具体信息。

![image-20210507203423054](C:\Users\lizehan\AppData\Roaming\Typora\typora-user-images\image-20210507203423054.png)

![image-20210507203450158](C:\Users\lizehan\AppData\Roaming\Typora\typora-user-images\image-20210507203450158.png)

## 3.疫情新闻浏览

​	接下来是疫情新闻浏览展示部分，新闻模块的参照诸如“今日头条”等新闻门户网站的设计。可以无限滚动，按照“新闻时效性”排序。通过点击标题可以跳转到原页面。我们的数据来源爬取自腾讯新闻疫情专栏，数据实时更新，比如今天是5月7日，显示的就是5月7日的相关新闻。

![image-20210507205103575](C:\Users\lizehan\AppData\Roaming\Typora\typora-user-images\image-20210507205103575.png)

## 4.病情自诊

​	接下来是病情自诊部分，病情自诊模块采取问卷的形式来呈现。用户通过填写问卷提交给后端进行逻辑判断，后端将判断好的结果返回给前端，以message的方式展示给用户。

![image-20210507210113435](C:\Users\lizehan\AppData\Roaming\Typora\typora-user-images\image-20210507210113435.png)

![image-20210507210500924](C:\Users\lizehan\AppData\Roaming\Typora\typora-user-images\image-20210507210500924.png)

## 5.基于知识图谱的疫情信息精准问答

​	接下来是最后一部分，也是本系统最主要的部分——基于知识图谱的疫情信息精准问答。

用户可以在此窗口进行提问：

![image-20210507211847477](C:\Users\lizehan\AppData\Roaming\Typora\typora-user-images\image-20210507211847477.png)

前端问句将传给后端，由后端进行命名实体识别和关系抽取等工作。我们通过人工标注的数据训练了基于TFIDF的机器学习模型，问句将会通过此模型进行短文本分类识别意图，最终转化为CYPHER查询语句，查询NEO4J数据库。后端将查询到的数据写入模板返回给前端，由前端将答案与图谱可视化展示出来。

如：新型冠状病毒肺炎的症状是什么

![image-20210507211059018](C:\Users\lizehan\AppData\Roaming\Typora\typora-user-images\image-20210507211059018.png)

如：新型冠状病毒肺炎如何传播

![image-20210507211300825](C:\Users\lizehan\AppData\Roaming\Typora\typora-user-images\image-20210507211300825.png)

如：新型冠状病毒肺炎是啥

![image-20210507211540631](C:\Users\lizehan\AppData\Roaming\Typora\typora-user-images\image-20210507211540631.png)

如：肩周炎挂什么科

![image-20210507211703979](C:\Users\lizehan\AppData\Roaming\Typora\typora-user-images\image-20210507211703979.png)

如果数据库查询不到将会提示错误信息：

![image-20210507212755672](C:\Users\lizehan\AppData\Roaming\Typora\typora-user-images\image-20210507212755672.png)

此外，我们在此基础上又通过网络爬虫技术采集了广州市卫生健康委员会网站“全力做好新型冠状病毒肺炎疫情防控工作”的“疫情通报”模块的关于境外输入病例的病例信息（由于其他省市由于涉及个人隐私等原因，不便公开数据，故未收集）。在数据清洗后加入到了图数据库中，进一步扩充了此数据库的数据。

如：2月16日有哪些确诊病例

![image-20210507212305728](C:\Users\lizehan\AppData\Roaming\Typora\typora-user-images\image-20210507212305728.png)

如：病例129从哪出发

![image-20210507212347673](C:\Users\lizehan\AppData\Roaming\Typora\typora-user-images\image-20210507212347673.png)

目前，此模块功能还不是非常完善，我们计划在未来的迭代过程中加入点击节点展开数据等功能，以更好地达到可视化效果。

以上就是本系统的全部功能演示，请老师批评指正。