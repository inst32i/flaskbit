# *-* encoding:utf-8 *-*
# usr/bin/python 2.7
'''
  @author  zengchonghan
  @email  529970462@qq.com
  @time: 2018/4/11 下午4:52
'''

'''
  函数列表:
  1.AHP评估主流程
  2.对用户输入的判断矩阵进行一致性校验
  3.创建RI对照表
  4.获取数据库中判断矩阵
  5.计算权重向量
  6.判断矩阵一致性校验
  7.获得指标评估等级
  8.获取指标列表
  9.获取指标中文名
  10.按层取指标中文
  11.获取评价表
  12.权重处理模块
  13.计算评估结果
  14. AHP.html获取top层权重值
  15.将计算后的权重值存入数据库中
  16.AHP.html获取指标层权重值
  17.继承Exception类，加入一致性校验
  18.判断安全范围
  19.返回评语
  26.取t时刻的观测值

  20.获取数据库内用户的判断矩阵参数
  21.获取数据库内用户的权重参数
  22.获取数据库内观测数据
  27.获取数据库内t时刻观测数据
  23.获取数据库内指标表
  24.获取数据库内安全评估表
  25.从文件中读取判断矩阵
'''

import sys
import math
import numpy as np
import operator
from model.Model import *
from ManifoldService import *
from functools import reduce

defaultencoding='utf-8'
if sys.getdefaultencoding()!=defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)


###########    1.AHP评估主流程
def AHP():
    assessmentlist = {}
    security_range = {}
    weights = get_index_weights()
    assessmentlist = get_index_assessment()

    AHP_result = compute_AHP_result(assessmentlist, weights)
    security_range = judge_security_range(AHP_result)
    return security_range


############    2.对用户输入的判断矩阵进行一致性校验
def consistency_test():
    TOP1_matrix = get_judgementmatrix(0)
    consistency_top1 = get_consistency_ratio(TOP1_matrix)
    HostSecurity_matrix = get_judgementmatrix(1)
    consistency_HostSecurity = get_consistency_ratio(HostSecurity_matrix)
    NetworkSecurity_matrix = get_judgementmatrix(2)
    consistency_NetworkSecurity = get_consistency_ratio(NetworkSecurity_matrix)
    VulnerabilitySecurity_matrix = get_judgementmatrix(3)
    consistency_VulnerabilitySecurity = get_consistency_ratio(VulnerabilitySecurity_matrix)

    if consistency_top1 == True and consistency_HostSecurity == True and consistency_NetworkSecurity == True and consistency_VulnerabilitySecurity == True:
        consistency_result = True
    else:
        consistency_result = False
    return consistency_result


###########    3.创建RI对照表
def order_to_RI(order):
    switcher = {
        1  : 0,
        2  : 0,
        3  : 0.58,
        4  : 0.9,
        5  : 1.12,
        6  : 1.24,
        7  : 1.32,
        8  : 1.41,
        9  : 1.45,
        10 : 1.49
    }
    #返回RI(default:0)
    return switcher.get(order, 0)


###########    4.获取数据库中判断矩阵
def get_judgementmatrix(layertype):
    judgementmatrix = getjudgementmatrix(layertype)
    length_square = len(judgementmatrix)
    length = int(math.sqrt(length_square))
    #1创建0矩阵
    martrix=np.zeros([length,length],dtype=np.float)
    #2.取初始k
    k = 0
    #3.将所有的边赋值
    for i in range(length):
        for j in range(length):
            martrix[i][j] = judgementmatrix[k]['value']
            k = k + 1
    return martrix


###########    5.计算权重向量
def compute_weights(dataset):
    #对判断矩阵每列进行归一化
    data_shape = dataset.shape
    data_rows = data_shape[0]
    data_cols = data_shape[1]
    weights_1 = np.zeros((data_rows,data_cols))
    for i in xrange(0, data_rows):
        for j in xrange(0, data_cols):
            weights_1[i][j] = dataset[i][j] / sum([dataset[x][j] for x in range(data_rows)])
    #将归一化后的矩阵按行相加
    weights_2 = np.zeros((data_rows,1))
    for i in xrange(0, data_rows):
        for j in xrange(1, data_cols):
            weights_2[i][0] += weights_1[i][j]
    weights_3 = np.zeros((data_rows,1))
    #得到的矩阵再进行归一化处理
    for i in xrange(0,data_cols):
        weights_3[i][0] = weights_2[i][0] / sum([weights_2[x][0] for x in range(data_cols)])
        round(weights_3[i][0],3)
    weights_result = np.around(weights_3, decimals=3)
    return weights_result


###########    6.判断矩阵一致性校验
def get_consistency_ratio(dataset):
    #构建判断矩阵
    judgement_matrix = np.mat(dataset)
    #得到特征值元组
    eigen,eigenvector = np.linalg.eig(judgement_matrix)
    #得到最大特征值
    data_shape = dataset.shape
    data_rows = data_shape[0]
    eigen = sorted(eigen)
    max_eigen = eigen[data_rows-1]
    #得到矩阵阶数
    order = judgement_matrix.shape[0]
    #计算一致性指标CI(consistency index)
    CI = (max_eigen - order) / (order - 1)
    #获取平均一致性随机指标RI(random index)
    RI = order_to_RI(order)
    #计算判断矩阵一致性校验因子
    CR = CI / RI
    #一致性校验
    if RI == 0:
        return True
    else:
        if CR < 0.1:
            return True
        else:
            return False


###########    7.获得指标评估等级
def get_index_assessment():
    observed_data = []
    assessment    = []
    assessmentlist = {}

    #获取观测数据
    observed_data = get_t_observedata(2)
    #获取指标评估表
    assessment = getassessment()
    #按照评估表对观测数据进行评估
    for one in assessment:
        index = one['element']
        for two in observed_data:
            if index == two['indexname']:
                if two['value'] < one['S5']:
                    assessmentlist[index] = 5
                elif two['value'] < one['S4']:
                    assessmentlist[index] = 4
                elif two['value'] < one['S3']:
                    assessmentlist[index] = 3
                elif two['value'] < one['S2']:
                    assessmentlist[index] = 2
                else:
                    assessmentlist[index] = 1
                break

    return assessmentlist


###########    8.获取指标列表
def get_indexlist():
    observed_data = []
    assessment    = []
    indexlist     = []

    #获取观测数据
    observed_data = getnodesobserved()
    #获取指标评估表
    assessment = getassessment()
    #按照评估表对观测数据进行评估
    for one in assessment:
        index = one['element']
        for two in observed_data:
            if index == two['indexname']:
                temp = ()
                temp = index
                indexlist.append(temp)
                break
    return indexlist


###########    9.获取指标中文名
def get_indexdescription(indexlist,layertype):
    indexdescription = []
    indexintro = []
    index = {}

    #获取指标表
    indexintro = getindexintro()
    #获取父节点
    pidlist = getjudgementmatrix(layertype)

    #获取中文名
    for one in indexlist:
        for two in indexintro:
            if one == two['indexname'].strip():
                temp = {}
                temp['id'] = two['id'] - 4
                temp['index'] = two['indexname']
                temp['description'] = two['description']
                for three in pidlist:
                    if two['id'] == three['indexid']:
                        temp['pid'] = three['pid']
                        break
                indexdescription.append(temp)
                break
    return indexdescription

###########    10.按层取指标中文
def get_indexdescription_eachlayer(indexlist,weights_E,layertype):
    templist = []

    index = get_indexdescription(indexlist,4)
    #获取权重
    matrix = get_judgementmatrix(layertype)
    weights_Q = compute_weights(matrix)
    weights = weights_E[layertype-1] * weights_Q
    weights = np.around(weights,4)

    i = 0
    for one in index:
        if one['pid'] == layertype:
            temp = {}
            temp['index'] = one['index']
            temp['description'] = one['description']
            temp['weight'] = weights[i]
            i = i + 1
            templist.append(temp)
    return templist

###########    11.获取评价表
def get_assessment(degree):
    observed_data = []
    assessment    = []
    assessmentlist     = []

    #获取观测数据
    observed_data = getnodesobserved()
    #获取指标评估表
    assessment = getassessment()
    #按照评估表对观测数据进行评估
    if degree == 1 :
        for one in assessment:
            index = one['element']
            for two in observed_data:
                if index == two['indexname']:
                    temp = ()
                    temp = one['S1']
                    assessmentlist.append(temp)
                    break
    elif degree == 2 :
        for one in assessment:
            index = one['element']
            for two in observed_data:
                if index == two['indexname']:
                    temp = ()
                    temp = one['S2']
                    assessmentlist.append(temp)
                    break
    elif degree == 3 :
        for one in assessment:
            index = one['element']
            for two in observed_data:
                if index == two['indexname']:
                    temp = ()
                    temp = one['S3']
                    assessmentlist.append(temp)
                    break
    elif degree == 4 :
        for one in assessment:
            index = one['element']
            for two in observed_data:
                if index == two['indexname']:
                    temp = ()
                    temp = one['S4']
                    assessmentlist.append(temp)
                    break
    else:
        for one in assessment:
            index = one['element']
            for two in observed_data:
                if index == two['indexname']:
                    temp = ()
                    temp = one['S5']
                    assessmentlist.append(temp)
                    break
    return assessmentlist

###########    12.权重处理模块
def deal_weights(weights_E, weights_Q_11, weights_Q_22, weights_Q_33):
    weights_Q_1 = weights_E[0] * weights_Q_11
    weights_Q_1 = np.around(weights_Q_1,4)
    weights_Q_2 = weights_E[1] * weights_Q_22
    weights_Q_2 = np.around(weights_Q_2,4)
    weights_Q_3 = weights_E[2] * weights_Q_33
    weights_Q_3 = np.around(weights_Q_3,4)
    weights = np.append(weights_Q_1,weights_Q_2)
    weights = np.append(weights,weights_Q_3)
    return weights


###########    13.计算评估结果
def compute_AHP_result(assessmentlist, weights):
    assessment_R_list = assessmentlist.values()
    assessment_R = np.array(assessment_R_list)
    assessment_R_T = assessment_R.T
    result =  np.dot(weights, assessment_R_T)
    result = round(result,4)
    return result


#############   14. AHP.html获取top层权重值
def get_top1_weights():
    TOP1_matrix = get_judgementmatrix(0)
    weights_top1 = compute_weights(TOP1_matrix)
    return weights_top1


###########    15.将计算后的权重值存入数据库中
def upload_weights():
    templist = []
    res = db.session.execute("select indexid,pid from ahpjudgement group by indexid,pid ").fetchall()
    db.session.close()
    for one in res:
        temp = {}
        temp['id'] = one['indexid']
        temp['pid'] = one['pid']
        templist.append(temp)

    weights = get_top1_weights()
    weights = weights.T.tolist()
    weights = reduce(operator.add, weights)
    Q_weights = get_index_weights()
    weights.extend(Q_weights)
    i = 0
    for one in templist:
        one['importance'] = weights[i]
        i = i + 1

    db.session.begin(subtransactions=True)
    try:
        db.session.execute("DELETE FROM ahp_tree where id>0")
        db.session.commit()

        for one in templist:
            weights = AHPTree(one['id'],one['pid'],one['importance'])
            db.session.add(weights)
        db.session.commit()
    except Exception:
        db.session.rollback()

        raise
    finally:
        if  db.session:
            db.session.close()

###########    16.AHP.html获取指标层权重值
def get_index_weights():
    TOP1_matrix = get_judgementmatrix(0)
    weights_top1 = compute_weights(TOP1_matrix)
    HostSecurity_matrix = get_judgementmatrix(1)
    weights_HostSecurity = compute_weights(HostSecurity_matrix)
    NetworkSecurity_matrix = get_judgementmatrix(2)
    weights_NetworkSecurity = compute_weights(NetworkSecurity_matrix)
    VulnerabilitySecurity_matrix = get_judgementmatrix(3)
    weights_VulnerabilitySecurity = compute_weights(VulnerabilitySecurity_matrix)

    weights = deal_weights(weights_top1, weights_HostSecurity, weights_NetworkSecurity, weights_VulnerabilitySecurity)

    return weights

############      17.继承Exception类，加入一致性校验
class Exception_consistency(Exception):
    def __init__(self,result,err):
        self.result = result

    def Input_err(self):
        try:
            result = consistency_test()
            assert result == False ,"Sorry, the judgement matrix cannot pass the consistency test. "
        except:
            print"Success"

############        18.判断安全范围
def judge_security_range(result):
    security_range = {'value':0, 'value_max':0, 'value_min':0}
    security_range['value'] = result
    security_range['value_max'] = int(math.ceil(result))
    security_range['value_min'] = int(math.floor(result))
    return security_range

############         19.返回评语
def get_review(result):
    if result < 5 and result > 4:
        Review = "很安全"
    elif result < 4 and result > 3:
        Review = "安全"
    elif result < 3 and result > 2:
        Review = "基本安全"
    elif result < 2 and result > 1:
        Review = "不安全"
    else:
        Review = "很不安全"
    return Review


##############       26.取t时刻的观测值
def get_t_observedata(t):
    templist = []
    observed_data = []
    data = get_t_nodesobserved()

    index = data[0]['indexname']
    i = 0
    for unit in data:
        temp = {}
        temp['create_time'] = unit['create_time']
        temp['time'] = i
        i = i + 1
        if index != unit['indexname']:
            break
        templist.append(temp)

    for one in templist:
        if t == one['time']:
            create_time = one['create_time']
            break

    for one in data:
        temp = {}
        if create_time == one['create_time']:
            temp['indexname'] = one['indexname']
            temp['value'] = one['value']
            observed_data.append(temp)
    return observed_data

#################    数据库操作      ####################
##########      20.获取数据库内用户的判断矩阵参数，zch,2018-04-12
def getjudgementmatrix(layertype):
    templist = []
    if layertype == 0:
        #TOP1层#
        res=db.session.execute("select * from ahpjudgement where pid=0 ").fetchall()
        for one in res:
            temp = {}
            temp['id'] = one['id']
            temp['indexid'] = one['indexid']
            temp['pid'] = one['pid']
            temp['cid'] = one['cid']
            temp['value'] = one['value']
            templist.append(temp)
        db.session.close()
    elif layertype == 1:
        #主机层#
        res=db.session.execute("select * from ahpjudgement where pid=1 ").fetchall()
        for one in res:
            temp = {}
            temp['id'] = one['id']
            temp['indexid'] = one['indexid']
            temp['pid'] = one['pid']
            temp['cid'] = one['cid']
            temp['value'] = one['value']
            templist.append(temp)
        db.session.close()
    elif layertype == 2:
        #网络层#
        res=db.session.execute("select * from ahpjudgement where pid=2 ").fetchall()
        for one in res:
            temp = {}
            temp['id'] = one['id']
            temp['indexid'] = one['indexid']
            temp['pid'] = one['pid']
            temp['cid'] = one['cid']
            temp['value'] = one['value']
            templist.append(temp)
        db.session.close()
    elif layertype == 3:
        #漏洞层#
        res=db.session.execute("select * from ahpjudgement where pid=3 ").fetchall()
        for one in res:
            temp = {}
            temp['id'] = one['id']
            temp['indexid'] = one['indexid']
            temp['pid'] = one['pid']
            temp['cid'] = one['cid']
            temp['value'] = one['value']
            templist.append(temp)
        db.session.close()
    else:
        res=db.session.execute("select * from ahpjudgement ").fetchall()
        for one in res:
            temp = {}
            temp['id'] = one['id']
            temp['indexid'] = one['indexid']
            temp['pid'] = one['pid']
            temp['cid'] = one['cid']
            temp['value'] = one['value']
            templist.append(temp)
        db.session.close()
    return templist

###########      21.获取数据库内用户的权重参数,zch,2018-04-12
def getweightindex():
    templist = []
    res=db.session.execute("select id, pid, importance from ahptree ").fetchall()
    for one in res:
        temp = {}
        temp['id'] = one['id']
        temp['pid'] = one['pid']
        temp['importance'] = one['importance']
        templist.append(temp)

    db.session.close()
    return data

###########       22.获取数据库内观测数据,zch,2018-04-17
def getnodesobserved():
    observed_data = []
    res=db.session.execute("select indexname,avg(value) as value_avg from indexrecord group by indexname ").fetchall()
    for one in res:
        temp = {}
        temp['indexname'] = one['indexname']
        temp['value'] = one['value_avg']
        observed_data.append(temp)
    db.session.close()
    return observed_data

###########       27.获取数据库内t时刻观测数据,zch,2018-05-29
def get_t_nodesobserved():
    observed_data = []
    res=db.session.execute("select indexname,avg(value) as value_avg,create_time from indexrecord group by indexname,create_time ").fetchall()
    for one in res:
        temp = {}
        temp['indexname'] = one['indexname']
        temp['value'] = one['value_avg']
        temp['create_time'] = one['create_time']
        observed_data.append(temp)
    db.session.close()
    return observed_data


###########        23.获取数据库内指标表,zch,2018-05-26
def getindexintro():
    templist = []
    res=db.session.execute("select * from indexintro ").fetchall()
    for one in res:
        temp = {}
        temp['id'] = one['id']
        temp['indexname'] = one['indexname']
        temp['description'] = one['description']
        templist.append(temp)

    db.session.close()
    return templist


###########         24.获取数据库内安全评估表,zch,2018-05-20
def getassessment():
    templist = []
    res=db.session.execute("select id,element,S1,S2,S3,S4,S5 from assessment ").fetchall()
    for one in res:
        temp = {}
        temp['id'] = one['id']
        temp['element'] = one['element']
        temp['S1'] = one['S1']
        temp['S2'] = one['S2']
        temp['S3'] = one['S3']
        temp['S4'] = one['S4']
        temp['S5'] = one['S5']
        templist.append(temp)
    db.session.close()
    return templist

############        25.从文件中读取判断矩阵
def insertJudgementMatrix(filepath):
    '''从文件中读取数据，并插入对应的数据库'''
    #1、读取数据
    judgement_matrix = readxls(filepath,0,'judgementmatrix')
    if len(judgement_matrix)==0:
        return
    #2. 插入数据库
    db.session.begin(subtransactions=True)

    try:
        db.session.execute("DELETE FROM ahpjudgement where id>0")
        db.session.commit()

        for one in judgement_matrix:
            matrix = AHPJudgement(one['indexid'],one['pid'],one['cid'],one['value'])
            db.session.add(matrix)
            db.session.commit()
    #except Exception_consistency as e:
    except Exception as e:
        db.session.rollback()

    #    raise e.Input_err()
        raise
    finally:
        if  db.session:
            db.session.close()



if __name__ == '__main__':
    basepath=os.path.dirname(__file__)
    upload_path = os.path.join(basepath, '../static/upload','testdata.xlsx')
    insertJudgementMatrix(upload_path)
    print('Done!')
