def if_contain_all(b,a):#辅助函数
    flag = 1
    for i in range(0,len(b)):
        if b[i] in a:
            flag = 1
        else:
            flag = 0
        if flag == 0:
            return
    else:
        return flag

def judge(self_test):  #判断自检结果

    if if_contain_all([0,1],self_test) or if_contain_all([0,2],self_test) or if_contain_all([0,3],self_test) or if_contain_all([0,4],self_test) or if_contain_all([0,5],self_test) or if_contain_all([0,6],self_test):
        #print('有发热和其他症状')
        #print('您有一定可能感染了新冠病毒')
        #print('建议佩戴外科口罩或N95口罩，至医院发热门诊就诊')
         return  '有发热和其他症状\n您有一定可能感染了新冠病毒\n建议佩戴外科口罩或N95口罩，至医院发热门诊就诊' #返回个值给前端？
    elif if_contain_all([2,3],self_test) or if_contain_all([2,4],self_test) or if_contain_all([2,4],self_test) or if_contain_all([2,5],self_test) or if_contain_all([2,6],self_test):
        #print('有典型症状')
        #print('您存在一定程度的新冠病毒感染风险')
        #print('建议居家医学观察，密切观察症状变化。建议定期评测，频率为每天一次')
        #print('')
        return   '有典型症状\n您存在一定程度的新冠病毒感染风险\n建议居家医学观察，密切观察症状变化。建议定期评测，频率为每天一次' #返回个值给前端？
    elif if_contain_all([3,4],self_test) or if_contain_all([3,5],self_test) or if_contain_all([3,6],self_test):
        #print('有典型症状')
        #print('您存在一定程度的新冠病毒感染风险')
        #print('建议居家医学观察，密切观察症状变化。建议定期评测，频率为每天一次')
        return  '有典型症状\n您存在一定程度的新冠病毒感染风险\n建议居家医学观察，密切观察症状变化。建议定期评测，频率为每天一次' #返回个值给前端？
    elif if_contain_all([4,5],self_test) or if_contain_all([4,6],self_test):
        #print('有典型症状')
        #print('您存在一定程度的新冠病毒感染风险')
        #print('建议居家医学观察，密切观察症状变化。建议定期评测，频率为每天一次')
        return  '有典型症状\n您存在一定程度的新冠病毒感染风险\n建议居家医学观察，密切观察症状变化。建议定期评测，频率为每天一次' #返回个值给前端？
    elif if_contain_all([5,6],self_test):
        #print('有典型症状')
        #print('您存在一定程度的新冠病毒感染风险')
        #print('建议居家医学观察，密切观察症状变化。建议定期评测，频率为每天一次')
        return  '有典型症状\n您存在一定程度的新冠病毒感染风险\n建议居家医学观察，密切观察症状变化。建议定期评测，频率为每天一次' #返回个值给前端？
    elif 1 in self_test or 2 in self_test or 3 in self_test or 4 in self_test or 5 in self_test or 6 in self_test and 8 in self_test and 10 in self_test or 11 in self_test or 12 in self_test or 13 in self_test:
        #print('有典型症状')
        #print('有在疫区的旅行史')
        #print('有可能接触过病毒')
        #print('您存在一定程度的新冠病毒感染风险。建议居家医学观察，密切观察症状变化。建议定期评测，频率为每天一次')
        return   '有典型症状\n有在疫区的旅行史\n有可能接触过病毒\n您存在一定程度的新冠病毒感染风险。建议居家医学观察，密切观察症状变化。建议定期评测，频率为每天一次'#返回个值给前端？
    elif 1 in self_test or 2 in self_test or 3 in self_test or 4 in self_test or 5 in self_test or 6 in self_test and 8 in self_test:
        #print('有典型症状')
        #print('有在疫区的旅行史')
        #print('您存在一定程度的新冠病毒感染风险。建议居家医学观察，密切观察症状变化。建议定期评测，频率为每天一次')
        return   '有典型症状\n有在疫区的旅行史\n您存在一定程度的新冠病毒感染风险。建议居家医学观察，密切观察症状变化。建议定期评测，频率为每天一次'#返回个值给前端？
    elif 1 in self_test or 2 in self_test or 3 in self_test or 4 in self_test or 5 in self_test or 6 in self_test and 10 in self_test or 11 in self_test or 12 in self_test or 13 in self_test:
        #print('有典型症状')
        #print('有可能接触过病毒')
        #print('您存在一定程度的新冠病毒感染风险。建议居家医学观察，密切观察症状变化。建议定期评测，频率为每天一次')
        return  '有典型症状\n有可能接触过病毒\n您存在一定程度的新冠病毒感染风险。建议居家医学观察，密切观察症状变化。建议定期评测，频率为每天一次'#返回个值给前端？
    elif 0 in self_test:
        #print('有典型症状')
        #print('您存在一定程度的新冠病毒感染风险')
        #print('建议居家医学观察，密切观察症状变化。建议定期评测，频率为每天一次')
        return  '有典型症状\n您存在一定程度的新冠病毒感染风险\n建议居家医学观察，密切观察症状变化。建议定期评测，频率为每天一次' #返回个值给前端？
    else:
        #print('根据您提供的信息，您出现了单项症状')
        #print('没有患者或疑似者接触史和疫区相关流行病学史')
        #print('您感染新冠病毒的风险比较低。请密切观察身体状况,建议定期评测，频率为每天一次')
        #print('如果自觉症状较重或有明显加重，建议佩戴口罩，到医院普通专科门诊或急诊就诊')
        return  '根据您提供的信息，您出现了单项症状\n没有患者或疑似者接触史和疫区相关流行病学史\n您感染新冠病毒的风险比较低。请密切观察身体状况,建议定期评测，频率为每天一次\n如果自觉症状较重或有明显加重，建议佩戴口罩，到医院普通专科门诊或急诊就诊'#返回个值给前端？

