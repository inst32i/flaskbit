# *-* encoding:utf-8 *-*
# usr/bin/python 2.7
'''
  @author  chenquanbao
  @email  kenybens@gmail.com
  @time: 2018/4/4 上午10:15
'''
from model.Model import *
import numpy as np
from component.Readutil import *
import Queue
import os
import math
import re
import datetime

def getLinks():
    templist=[]
    link = db.session.execute("select distinct pid as source,  cid as target, avg(importance) as importance from noderelates group by source,target order by source,target").fetchall()
    for one in link:
        temp={}
        temp['source']=one['source']
        temp['target']=one['target']
        temp['importance'] = one['importance']
        templist.append(temp)

    db.session.close()
    return templist
def getNode_Links():
    '''获取节点和连接线信息'''
    map={}
    map['links']=getLinks()
    map['nodes']=getnodes()


    return map
def creatematrinNeiber():
    '''生成邻接矩阵'''
    links=getLinks()
    nodes=getnodes()
    length=len(nodes)
    #1创建0矩阵
    martrix=np.zeros([length,length],dtype=np.int)
    #2.将所有的边赋值
    for one in links:
        martrix[one['source']-1][one['target']-1]=1
        martrix[one['target']-1][one['source']-1]=1

    return martrix
def insertNodeandLink(filepath):
    '''从文件中读取数据，并插入对应的数据库'''
    #1、读取数据
    nodes=readxls(filepath,0,'node')
    links=readxls(filepath,0,'links')


    #2. 插入数据库
    db.session.begin(subtransactions=True)

    try:
        #将数据库中的旧表中的内容转移到另外两张表,并清空当前表
        if len(nodes) == 0 or len(links) == 0:
            # 只删除当前表记录，并转移到历史数据
            return

        #获取所有指标类型
        indexlist=db.session.query(Indexintro).all()

        Nodeindex.query.delete()
        Noderelate.query.delete()
        Indexrecord.query.delete()
        param=()
        objects=[]
        for one in nodes:
            # zym 获得节点名字、重要性、服务、服务重要性2018.04.11

            keysindex=[n for n in one.keys() if re.match('Q\d+',n)]
            for key in keysindex:


                if key !=None:
                    value=one[key]
                    if value==None:
                        value=0

                    noderecord=Indexrecord(one['id'],key.strip(),value,one['updatetime'])
                    db.session.add(noderecord)
                    db.session.commit()
            node = Nodeindex(one['id'], one['nodetype'], one['updatetime'], one['importance'])
            db.session.add(node)
            db.session.commit()
        for one in links:
            link=Noderelate(one['id'],one['source'],one['target'],one['importance'],one['updatetime'])
            db.session.add(link)
            objects.append(link)
            db.session.commit()

        db.session.flush()
        #db.session.add_all(objects)
        db.session.commit()

    except Exception as e:

        db.session.rollback()

        raise
    finally:
        if  db.session:
            db.session.close()

def getMenu():
    return db.session.query(Menu).filter(Menu.isvisible==1).order_by(Menu.sortid).all()
def getallmenu():
    return db.session.query(Menu).order_by(Menu.sortid).all()


def getnodes():
    templist = []
    res=db.session.execute("select distinct nodeid as id,nodeTypeid as type from nodeindex order by id").fetchall()
    db.session.close()
    for one in res:
        temp = {}
        temp['id'] = one['id']
        temp['type'] = one['type']
        templist.append(temp)
    return templist


def lapulasi(data_matrix):
    '''计算拉普拉斯矩阵L=D-W'''
    data_matrix=np.asarray(data_matrix)
    row,col=data_matrix.shape
    for i in range(row):
        degree=0
        for j in range(col):
            val=data_matrix[i][j]
            degree=val+degree
            data_matrix[i][j]=-1*val
        data_matrix[i][i]=degree
    return data_matrix

def weightneibor(martix,indexos):
    '''给矩阵权重赋值'''
    #martix=np.asmatrix(martix,dtype=int)
    row,col=martix.shape
    #返回第一个时刻的矩阵信息

    for key in indexos:

        realmartrix = np.zeros([row, row], dtype=np.int)
        indexvalue=indexos[key]
        for i in range(row):
            for j in range(col):
                if martix[i][j]==1:

                    nodexin=indexvalue[i+1]
                    nodeyin=indexvalue[j+1]

                    if nodexin!=None and nodeyin!=None:
                        tracei=nodexin['trace']
                        tracej=nodeyin['trace']
                        realmartrix[i][j]=computeweight(tracei,tracej)
        indexsum = round(float(computrace(lapulasi(realmartrix)))/pow(10,17),2)
        indexos[key]['weimat']=0.01*realmartrix
        indexos[key]['indexsum']=indexsum
    return indexos
def z_score(x, axis=0):
    x = np.array(x).astype(float)
    xr = np.rollaxis(x, axis=axis)
    xr -= np.mean(x, axis=axis)
    xr /= np.std(x, axis=axis)
    # print(x)
    return x
def change2dim(x):
    unitone=np.ones(len(x))
    x=np.asmatrix(x).astype(float)

    #x.shape=(len(x),1)
    xtrans=np.transpose(x)
    x2dim=xtrans*unitone
    x2dim=abs(np.transpose(x2dim)-x2dim)
    return x2dim
def computrace(x):
    '''计算矩阵的迹'''
    x=100*x
    a,b=np.linalg.eig(x)
    return pow(10,12)*np.sum(a)
def computeweight(x,y):
    if math.isnan(x ) or math.isnan(y):
        return 0
    return 100*np.e**(-(x-y)**2/2)
def computmethod(x):
    '''将结果压缩到0-100'''
    return 1000*np.e**(-(x**2))
def simplerule(nodes):
    '''将所有的值归一化为0-100之间'''
    result={}
    dictindex={}
    for unit in nodes:
        #将指标进行组合
        keytime=unit.create_time
        if keytime in dictindex.keys():
            dictunit=dictindex.get(keytime)
            if unit.nodeid in dictunit.keys():
                dictunit[unit.nodeid]['typeid']=unit.nodeTypeid
                if  'indexlist' not in dictunit[unit.nodeid].keys():
                    dictunit[unit.nodeid]['indexlist']=[]
                dictunit[unit.nodeid]['indexlist'].append(unit.value)
            else:
                dictunit[unit.nodeid]={}
        else:
            dictindex[keytime]={}

    for key in dictindex:
        for node in dictindex[key]:
            arr=dictindex[key][node]['indexlist']
            standinput=z_score(arr)
            matrix2dim=change2dim(standinput)
            dictindex[key][node]['index']=matrix2dim
            dictindex[key][node]['trace']=computrace(matrix2dim)

    return dictindex
def computeSingleNodeValue():
    '''读取所有节点的指标和参考系的指标，并计算两者之间的差异，并赋值会原来的节点对应的值'''
    #选择的数据要进行排序，
    query='''
        select distinct a.id,a.nodeid,a.indexname,a.value,a.create_time,b.nodeTypeid,b.importance
        from indexrecord as a
        join nodeindex as b
        on a.nodeid=b.nodeid

    '''
    indexnodes =db.session.execute(query).fetchall()
    if db.session:
        db.session.close()
    #indexnodes=db.session.query(Indexrecord).order_by(Indexrecord.create_time,Indexrecord.id,Indexrecord.indexname).all()
    #将指标按照时间和nodeid进行划分

    #1.将参数归一化，构成新的数列
    # 2.将节点的指标组成方阵，并计算得到迹
    indexnodes=simplerule(indexnodes)
    #3. 计算得到所有的邻接矩阵
    resultseries=weightneibor(creatematrinNeiber(),indexnodes)
    return indexnodes




if __name__ == '__main__':

    basepath=os.path.dirname(__file__)
    upload_path = os.path.join(basepath, '../static/upload','testdata.xlsx')
    insertNodeandLink(upload_path)
    #insertJudgementMatrix(upload_path)
