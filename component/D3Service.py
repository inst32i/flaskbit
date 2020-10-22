# *-* encoding:utf-8 *-*
# usr/bin/python 2.7
'''
  @author  chenquanbao
  @email  kenybens@gmail.com
  @time: 2018/4/20 上午10:57
  请将关于多层多粒度的服务写在这里
'''
from model.Model import *
import numpy as np
import Queue
from component.Readutil import *


# 获得nodeid值
def getIndexSum():
    templist = []
    res = db.session.execute("SELECT DISTINCT nodeid FROM indexrecord ").fetchall()
    db.session.close()
    for one in res:
        temp = {}
        temp['nodeid'] = one['nodeid']
        templist.append(temp)
    return templist

# 获得每一个动态指标的值
def getDynIndexValue(nodeid):
    templist = []
    res = db.session.execute("SELECT nodeid,indexname,VALUE as indexValue,create_time,update_time FROM indexrecord where nodeid = "+str(nodeid)+" ORDER BY indexname,create_time").fetchall()
    db.session.close()
    for one in res:
        temp = {}
        temp['nodeid'] = one['nodeid']
        temp['indexname'] = one['indexname']
        temp['indexValue'] = one['indexValue']
        temp['create_time'] = one['create_time']
        temp['update_time'] = one['update_time']
        templist.append(temp)
    #print templist,templist
    return templist


# 获得每一个动态指标的平均值峰值
def getAvgAndMaxValue(nodeid):
    templist = []
    res = db.session.execute("SELECT nodeid,indexname,AVG(VALUE) as avgNum ,MAX(VALUE) AS maxNum ,COUNT(nodeid) AS num,MAX(create_time) as maxTime FROM indexrecord WHERE nodeid = "+str(nodeid)+" GROUP BY indexname ORDER BY nodeid,indexname").fetchall()
    db.session.close()
    for one in res:
        temp = {}
        temp['nodeid']=one['nodeid']
        temp['indexname']=one['indexname']
        temp['avgNum']=one['avgNum']
        temp['maxNum'] = one ['maxNum']
        temp['num'] = one['num']
        temp['maxTime'] = one['maxTime']
        templist.append(temp)
    # print 'getAvgAndMaxValue',templist
    return templist

# 获得每一个动态指标评估结果：
def getDynIndeValue(nodeid):
    # 1.该指标值与平均值比较

    #     1.1 比均值大
    #         1.1.1 在最大值左边，处于上升状态，不安全
    #         1.1.2 安全，处于下降状态
    #     1.2 比均值小，安全
    templist = []
    # 获得所有动态指标
    dynIndex = getDynIndexValue(nodeid)
    # 获得每一项指标的平均值和最大值时间
    avgAndmax = getAvgAndMaxValue(nodeid)
    # 指标项个数
    length = len(avgAndmax)
    k = 0
    for i in range(0,length):
        # 第i个指标项对应的动态指标个数、平均值、最大值时间、名字
        security = 0
        unsecurity = 0
        # 动态指标个数
        count = avgAndmax[i]['num']
        # 平均值
        avg = avgAndmax[i]['avgNum']
        # 最大值时间
        maxTime = avgAndmax[i]['maxTime']
        # 指标项名字
        indexName = avgAndmax[i]['indexname']
        for j in range(k,k + count):
            if dynIndex[j]['indexValue'] < avg:
                security = security + 1
            elif dynIndex[j]['create_time'] < maxTime:
                unsecurity = unsecurity + 1
            else:
                security = security + 1
        temp = {}
        temp['indexname'] = indexName
        temp['nodeid'] = avgAndmax[i]['nodeid']
        if security > count/2:
            temp['res'] = 'security'
        else:
            temp['res'] = 'unsecurity'
        templist.append(temp)
        k = k + count
    return templist


# 获得每个主机每个指标的评估结果值
def getDynAllIndexValue():
    templist = []
    nodeids = getIndexSum()
    length = len(nodeids)
    for i in range(0,length):
        nodeid = nodeids[i]['nodeid']
        res = getDynIndeValue(int(nodeid))
        length2 = len(res)
        for j in range(0,length2):
            temp = {}
            temp['nodeid'] = nodeid
            temp['indexname'] = res[j]['indexname']
            temp['value'] = res[j]['res']
            templist.append(temp)
    return templist

# 获得单个节点所有指标度量结果
def getIndexValue(nodeid):
    res = getDynIndeValue(nodeid)
    length = len(res)
    count = 0
    for i in range(0,length):
        if res[i]['res'] == 'security':
            count = count + 1
    if count > length/2:
        return 'security'
    elif count>0 and count <= length/2:
        return 'unsecurity'
    else:
        return 'none'


# 获得整个网络中所有节点的指标评估中
def getNetAllIndex():
    templist = []
    nodeids = getIndexSum()
    length = len(nodeids)
    for i in range(0,length):
        nodeid = int (nodeids[i]['nodeid'])
        res = getIndexValue(nodeid)
        temp = {}
        temp['nodeid'] = nodeid
        temp['value'] = res
        templist.append(temp)
    return templist

# 获得子网中所有节点的指标评估值
def getSubIndexValue():
    templist = []
    network = creatematrinNeiber()
    graphArray = GetALlConnectedZone(network)
    d = graphArray[0][0]

    for i in range(1, d+1):
        net = graphArray[i]
        length = len(net)
        sum = 0
        for j in range(0,length):
            nodeid = net[j]
            if getIndexValue(nodeid) == 'security':
                sum =  sum+1
        if sum > length/2:
            res = 'security'
        else:
            res = 'unsecurity'
        temp = {}
        temp['name'] = 'subnet'+str(i)
        temp['value'] = res
        templist.append(temp)
    return templist


def insertNodeService(filepath):
    '''从文件中读取数据，并插入对应的数据库'''
    #1、读取数据
    nodeser=readxls(filepath,0,'node_service')
    #2. 插入数据库
    db.session.begin(subtransactions=True)
    try:
        db.session.execute("DELETE FROM node_ser where id>0")
        db.session.commit()

        if len(nodeser)==0:
            return

        for one in nodeser:
            # zym 获得节点名字、重要性、服务、服务重要性2018.04.11
            node=Node_ser(one['nodeid'],one['serviceid'],one['importance'],one['port'])
            db.session.add(node)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        raise

    finally:
        if  db.session:
            db.session.close()

def insertNodeVul(filepath):
    '''从文件中读取数据，并插入对应的数据库'''
    #1、读取数据
    nodevul=readxls(filepath,0,'node_vul')
    #2. 插入数据库
    db.session.begin(subtransactions=True)
    try:
        db.session.execute("DELETE FROM node_vul where id>0")
        db.session.commit()

        if len(nodevul)==0:
            return

        for one in nodevul:
            # zym 获得节点名字、重要性、服务、服务重要性2018.04.11
            node=Node_vul(one['nodeid'],one['vulid'])
            db.session.add(node)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        raise

    finally:
        if  db.session:
            db.session.close()


def getnodes():
    templist = []
    res=db.session.execute("select DISTINCT nodeid as id,nodeTypeid as type from nodeindex ").fetchall()
    db.session.close()
    for one in res:
        temp = {}
        temp['id'] = one['id']
        temp['type'] = one['type']
        templist.append(temp)
    return templist

def getLinks():
    templist=[]
    link = db.session.execute("SELECT DISTINCT pid as source ,cid as target ,max(importance) as importance FROM noderelates group by source,target").fetchall()
    for one in link:
        temp={}
        temp['source']=one['source']
        temp['target']=one['target']
        temp['importance'] = one['importance']
        templist.append(temp)

    db.session.close()
    return templist


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

# zym 获得节点名字、重要性、服务、服务重要性2018.04.25
def getnodes2():
    templist = []
    res = db.session.execute("SELECT DISTINCT nodeindex.nodeid,nodeindex.importance,nodetype.name,nodeindex.nodeTypeid "
                             "FROM nodeindex,nodetype "
                             "WHERE nodeindex.nodeTypeid = nodetype.id ").fetchall()

    for one in res:
        temp = {}
        temp['id'] = one['nodeid']
        temp['name'] = one['name']
        temp['importance']=one['importance']
        temp['nodeTypeid']=one['nodeTypeid']
        templist.append(temp)
    db.session.close()
    # print 'nodes',templist
    return templist

def findname(list,key,value):

    if list ==None or len(list)==0 :
        return ''
    for one in list:
        if one['id']==key:
            return one['name']
    return ''

def getLinks2():
    templist=[]
    # link = db.session.execute("SELECT noderelates.cid,noderelates.importance,nodetype.name AS source,nodeindex.importance AS sourceImportance,"
    #                           "noderelates.pid,nodetype2.name AS target,nodeindex2.importance AS targetImportance "
    #                           "FROM noderelates,nodeindex,nodetype,nodeindex AS nodeindex2,nodetype AS nodetype2 "
    #                           "WHERE noderelates.cid=nodeindex.nodeid AND nodetype.id = nodeindex.nodeTypeid AND nodeindex.nodeTypeid = nodetype.id "
    #                           "AND nodeindex2.nodeid = noderelates.pid AND nodetype2.id = nodeindex2.nodeTypeid").fetchall()


    typelist=db.session.execute("""SELECT DISTINCT nodeid as id, nodetype.name
            from nodeindex
            JOIN nodetype on nodeindex.nodeTypeid=nodetype.id""").fetchall()

    link = db.session.execute(
        """SELECT DISTINCT noderelates.cid, noderelates.pid, max(noderelates.importance) as importance, max(nodeindex.importance)
    AS sourceImportance,max(nodeindex2.importance)
    AS targetImportance
    FROM noderelates, nodeindex, nodeindex AS nodeindex2

    WHERE noderelates.cid = nodeindex.nodeid
    AND nodeindex2.nodeid = noderelates.pid
    group by noderelates.cid, noderelates.pid""").fetchall()


    typedict = {}
    for one in typelist:
        typedict[one['id']] = one['name']
    for one in link:
        temp={}
        temp['cid']=one['cid']
        temp['pid'] = one['pid']

        temp['sourceImportance'] = one['sourceImportance']

        temp['targetImportance'] = one['targetImportance']
        temp['importance'] = one['importance']
        temp['source']=typedict[one['pid']]
        temp['target']=typedict[one['cid']]
        templist.append(temp)

    db.session.close()
    return templist

# 进行BFS求连通与否
def BFS(G, edgeNum, root, visited):
    q = Queue.Queue()
    q.put(root)
    visited[root]=True
    a = len(G)
    res = np.zeros([a],np.int)
    for i in range(0,a):
        res[i]=-1
    k = 0
    while not q.empty():
        t = q.get()
        res[k]=t
        k += 1
        for i in range(0,edgeNum):
            if visited[i]==False and G[t][i]==1:
                q.put(i)
                visited[i]=True
    return res

# 获得连通分量个数及子图,res[0][0]存储一共有几个连通分量，res[i](i!=0)存储每一个
def GetALlConnectedZone(G):
    # print '测试连通分量个数以及联通分量子图 '
    # print '\n'
    count = 0
    a = len(G)
    # print 'a',a
    visited = np.zeros([a],dtype=np.bool)
    res = np.zeros([a+1,a],np.int)
    k = 1
    for i in range(0,a):
        if visited[i]==False:
            # print 'i',i
            t = BFS(G,a,i,visited)
            size = len(t)
            for j in range(0,size):
                res[k][j]=t[j]+1
            count += 1
            k += 1
    res[0][0]=count
    # print 'res[0][0]',res[0][0] 1383 1544
    return res

# 获得连通分量个数
def getConnected():
    martrix = creatematrinNeiber()
    # print 'martrix',martrix,'\n'
    res = GetALlConnectedZone(martrix)
    return res[0][0]
# 获得连通分量计算分数
def getConnectedResult():
    V = len(getnodes())
    martrix = creatematrinNeiber()
    # print 'martrix',martrix,'\n'
    res = GetALlConnectedZone(martrix)
    d = res[0][0]
    sum = round((-d+1)*1.0/(V-1)*10.0+10,3)
    return sum

# 获得连通子图中最外层的编号,即根节点
def getConnectedIndex(graphArray):
    # print graphArray,graphArray

    res = db.session.query(Nodeindex).filter(Nodeindex.nodeid.in_(graphArray))\
        .order_by(Nodeindex.nodeTypeid.desc(),Nodeindex.importance).limit(1).all()
    # print 'res,',res[0]['id']
    if res!=None and len(res)>0:
        return res[0]['nodeid']
    return np.max(graphArray)


# 获得子网中节点最大值
def getMaxNodeId(graphArray):
    a = len(graphArray)
    max = -1
    for i in range(0,a):
        if max < graphArray[i]:
            max = graphArray[i]
    return max
def getNodeCount(graphArray):
    sum = 0
    a= len(graphArray)
    for i in range(0,a):
        if graphArray[i]!=0:
            sum += 1
    return sum

# 获得子网的矩阵
def getConnectedLinks(graphArray):
    links = db.session.query(Noderelate).filter(or_(Noderelate.cid.in_(graphArray), Noderelate.pid.in_(graphArray))).all()
    length = getMaxNodeId(graphArray)
    # 1创建0矩阵
    martrix = np.zeros([length+1, length+1], dtype=np.int)
    # 2.将所有的边赋值
    for one in links:
        martrix[one['pid'] ][one['cid'] ] = 1
        martrix[one['cid'] ][one['pid'] ] = 1
    if db.session:
        db.session.close()
    return martrix

# 获得节点层次
def getLevels(G,root):
    # print '测试获得节点层次',' -- ',G,'根节点',root,' -- ','图G',G,'\n'
    martrix = getConnectedLinks(G)
    b = getMaxNodeId(G)+1
    # print 'b最大节点+1',b
    a = len(G)
    # print '图长度',a
    visited = np.zeros([b], dtype=np.int)
    for i in range(0,b):
        visited[i]=1
    for i in range(0,len(G)):
        if G[i]!=0:
            t = G[i]
            visited[t]=0

    res = np.zeros([a,a],dtype=np.int)
    for i in range(0,a):
        for j in range(0,a):
            res[i][j]=-1
    q = Queue.Queue()
    q.put(root)
    visited[root]=1
    level = -1
    while not q.empty():
        size = q.qsize()
        level += 1
        k = 0
        for i in range(0,size):
            t = q.get()
            res[level][k]=t
            k += 1
            for j in range(1,b):
                if visited[j] == 0:
                    if martrix[t][j] == 1:
                        q.put(j)
                        visited[j]=1
    return res
def getNodeService():
    templist =[]
    # services = db.session.execute("SELECT nodeindex.nodeid,nodeindex.nodeTypeid,nodetype.name AS nodeName,nodeindex.importance,"
    #                               "node_ser.serviceid,servicetype.name AS serviceName,node_ser.importance AS serviceImportance "
    #                               "FROM nodeindex,node_ser,nodetype,servicetype "
    #                               "WHERE nodeindex.nodeid = node_ser.nodeid AND nodeindex.nodeTypeid = nodetype.id AND servicetype.id = node_ser.serviceid").fetchall()

    services=db.session.execute("""SELECT nodeindex.nodeid as id,max(nodeindex.importance) as importance,
                                  node_ser.serviceid,max(node_ser.importance) AS serviceImportance 
                                  FROM nodeindex,node_ser
                                  WHERE nodeindex.nodeid = node_ser.nodeid
                                  GROUP by nodeindex.nodeid,node_ser.serviceid""").fetchall()
    typlist = db.session.execute("""SELECT DISTINCT nodeid as id,nodetype.name
               from nodeindex
               JOIN nodetype on nodeindex.nodeTypeid=nodetype.id""").fetchall()
    servicelist = db.session.execute("""SELECT id,name from servicetype""").fetchall()
    servicedict={}
    typedict={}
    for one in servicelist:
        servicedict[one['id']]=one['name']
    for one in typlist:
        typedict[one['id']]=one['name']
    for one in services:
        temp = {}
        temp['id'] = one['id']
        temp['nodeName'] = typedict[one['id']]
        temp['importance']=one['importance']
        temp['serviceid']=one['serviceid']
        temp['serviceName']=servicedict[one['serviceid']]
        temp['serviceImportance']=one['serviceImportance']
        templist.append(temp)

    db.session.close()
    # print 'templist', templist
    return templist
# 计算资源维
# def getResource(G,root):
#     nodes = getnodes2()
#     levels = getLevels(G,root)
#     # print G,root,'\n'
#     sum = 0.0
#     a = len(nodes)
#     b = len(levels)
#     for i in range(0,b):
#         size = len(levels[i])
#         for j in range(0,size):
#             t = levels[i][j]
#             if t !=-1:
#                 for k in range(0,a):
#                     if int(nodes[k].get('id'))==t:
#                         importance = float (nodes[k].get('importance'))
#                         # serviceImportance = float(nodes[k].get('serviceImportance'))
#                         sum += 1.0/(i+1)*importance
#     return sum
  # 计算全网环境维
# def getAllResource():
#     sum = 0.0
#     count = 0
#     templist = []
#     # 获取每个连通分量,
#     network = creatematrinNeiber()
#     graphArray = GetALlConnectedZone(network)
#     # 获取连通分量个数
#     numConnect = graphArray[0][0]
#     # print '连通分量个数',numConnect
#     # print '\n'
#     for i in range(1,numConnect+1):
#         G = graphArray[i]
#         root = getConnectedIndex(graphArray[i])
#         count += getNodeCount(G)
#         aum = round(getResource(G,root)/getNodeCount(G),3)
#         temp = {}
#         temp['value']=aum
#         # print i,'count',count,'aum',aum,'\n'
#         s = str(i)
#         s = 'subnet'+s
#         temp['name']= s
#         templist.append(temp)
#         sum += aum
#         sum = round(sum,3)
#     temp = {}
#     temp['value'] = sum
#     temp['name']='whole network'
#     templist.append(temp)
#     return templist
# 服务维度量
def getServiceResult(G,root):
    nodes = getNodeService()
    # print nodes
    levels = getLevels(G,root)
    a = len(nodes)
    b = len(levels)
    map ={}
    for i in range(0, b):
        size = len(levels[i])
        for j in range(0, size):
            t = levels[i][j]
            if t != -1:
                for k in range(0, a):
                    if int(nodes[k].get('id')) == t:
                        importance = float(nodes[k].get('importance'))
                        serviceImportance = float(nodes[k].get('serviceImportance'))

                        num = 1.0 / (i+1) * importance*serviceImportance
                        key = str(t)+' '+nodes[k].get('nodeName')
                        # print key,t, importance, serviceImportance,num
                        if(map.has_key(key)):
                            map[key] += num
                        else:
                            map[key] = num
    # print 'map'
    # for key in map:
    #     print key,map[key]
    return map

def getAllNodeResult():
    templist = []
    sum = 0.0
    count = 0
    # 获取每个连通分量,
    network = creatematrinNeiber()
    graphArray = GetALlConnectedZone(network)
    # 获取连通分量个数
    numConnect = graphArray[0][0]
    for i in range(1, numConnect + 1):
        G = graphArray[i]
        # print 'G',G
        root = getConnectedIndex(graphArray[i])
        # print 'root',root
        count += getNodeCount(G)
        res = getServiceResult(G, root)
        aum = 0.0
        for key in res:
            temp = {}
            array = key.split()
            temp['id'] = array[0]
            temp['name'] = array[1]
            temp['value'] = round(float(res[key]),3)
            templist.append(temp)
    return templist


# # 计算全网服务维
def getAllServiceResult():
    templist = []
    sum = 0.0
    # 获取每个连通分量,
    network = creatematrinNeiber()
    graphArray = GetALlConnectedZone(network)
    # 获取连通分量个数
    numConnect = graphArray[0][0]
    for i in range(1, numConnect + 1):
        G = graphArray[i]
        root = getConnectedIndex(graphArray[i])
        res = getServiceResult(G, root)
        aum = 0.0
        for key in res:
            aum += float(res[key])
        aum = round(aum/getNodeCount(G),3)
        temp ={}
        temp['name']='subnet'+str(i)
        temp['value']=aum
        templist.append(temp)
        # sum += aum
        if(sum<aum):
            sum = aum
    temp={}
    temp['name']='whole network'
    temp['value']=round(sum,3)
    templist.append(temp)
    return templist


# 保存每一个子网中节点的服务重要性
def getServiceResult2(G,root):
    templist=[]
    nodes = getnodes2()
    levels = getLevels(G,root)
    a = len(nodes)
    b = len(levels)
    for i in range(0, b):
        size = len(levels[i])
        for j in range(0, size):
            t = levels[i][j]
            if t != -1:
                for k in range(0, a):
                    if int(nodes[k].get('id')) == t:
                        importance = float(nodes[k].get('importance'))
                        serviceImportance = float(nodes[k].get('serviceImportance'))
                        temp ={}
                        temp['name']=nodes[k].get('name')
                        temp['value']=round((1.0 / (i+1) * importance*serviceImportance),3)
                        templist.append(temp)

    return templist
# # 获得网络中每一个节点的服务重要性
# def getAllNodeServiceResult():
#     templist = []
#     sum = 0.0
#     # 获取每个连通分量,
#     network = creatematrinNeiber()
#     graphArray = GetALlConnectedZone(network)
#     # 获取连通分量个数
#     numConnect = graphArray[0][0]
#     for i in range(1, numConnect + 1):
#         G = graphArray[i]
#         root = getConnectedIndex(graphArray[i])
#         nodelist = getServiceResult2(G, root)
#         a = len(nodelist)
#         for j in range(0,a):
#             temp ={}
#             temp['name']=nodelist[j].get('name')
#             temp['value']=nodelist[j].get('value')
#             templist.append(temp)
#     return templist
# 获得指标展示
# def getIndexs():
#     indexs = db.session.query(Indexs).all()
#     return indexs

# 获得节点链路结果
def getAllgetLinksResult():
    sum =0.0
    templist = getLinks2()
    list=[]
    a = len(templist)
    for i in range(0,a):
        target = templist[i].get('target')
        source = templist[i].get('source')
        cid = templist[i].get('cid')
        pid = templist[i].get('pid')
        targetImportance = templist[i].get('targetImportance')
        sourceImportance = templist[i].get('sourceImportance')
        importance = templist[i].get('importance')
        sum = round(float(targetImportance)*float(sourceImportance)*float(importance),3)
        temp ={}
        temp['target'] = target
        temp['source'] = source
        temp['value'] = str(sum)
        temp['cid'] =int(cid)
        temp['pid'] =int(pid)
        list.append(temp)
    return list

# 获得环中路径总数
def getsubCycleCount(graphArray):
    sum = 0
    martrix = getConnectedLinks(graphArray)
    a = len(martrix)
    for i in range(0,a):
        for j in range(i,a):
            if martrix[i][j]==1:
                sum += 1
    return sum
# 图中只有一个节点
def isSingleNode(graphArray):
    if len(graphArray)==1:
        return True
    else:
        return False

# 获得子网链路结果
def getSubnetLinksResult():
    templist = []
    network = creatematrinNeiber()
    graphArray = GetALlConnectedZone(network)
    res = getAllgetLinksResult()
    # a = len(res)
    # 获取连通分量个数
    numConnect = graphArray[0][0]
    # print 'numConnect',numConnect,'\n'
    sum = 0.0
    count = 0
    for i in range(1, numConnect + 1):
        aum = 0.0
        # G是矩阵，graphArray[i]是连通区域的节点
        G = getConnectedLinks(graphArray[i])
        # print 'i',i,'G\n',G

        a = len(G)
        for j in range(1,a):
            for k in range(j,a):
                if(G[j][k]==1):
                    for l in range(0,len(res)):
                        cid = int(res[l].get('cid'))
                        pid = int(res[l].get('pid'))
                        # print('cid',cid),('pid',pid),float(res[l].get('value')),'\n'
                        if (cid == j and pid == k) or (pid==j and cid==k):
                            aum += float(res[l].get('value'))
        cycleCount = getsubCycleCount(graphArray[i])
        if cycleCount==0:
            temp = {}
            temp['name'] = 'subnet' + str(i)+' is a single node'
            temp['value'] = 0
            templist.append(temp)
        else:
            count += getsubCycleCount(graphArray[i])
            if(sum<aum/getsubCycleCount(graphArray[i])):
                sum = aum/getsubCycleCount(graphArray[i])
            # sum += aum/getsubCycleCount(graphArray[i])
            temp = {}
            temp['name'] = 'subnet' + str(i)
            temp['value'] = round(aum/getsubCycleCount(graphArray[i]),3)
            templist.append(temp)
    temp = {}
    temp['name'] = 'whole network'
    temp['value'] = round(sum,3)
    templist.append(temp)
    return templist

# 获得节点的漏洞信息
def getNodeVul():
    templist=[]
    nodesVul = db.session.execute("""SELECT  DISTINCT nodeindex.nodeid,vulid,nodeindex.nodeTypeid,vulnerability.name AS vulName,
                                  vulnerability.v2score,vulnerability.v3score,nodeindex.importance 
                                  FROM node_vul,nodeindex,vulnerability 
                                  
                                  WHERE node_vul.nodeid = nodeindex.nodeid AND node_vul.vulid = vulnerability.id 
                                  ORDER BY  nodeindex.nodeid,vulid  DESC""").fetchall()
    typlist = db.session.execute("""SELECT DISTINCT nodeid as id,nodetype.name
                  from nodeindex
                  JOIN nodetype on nodeindex.nodeTypeid=nodetype.id""").fetchall()

    typedict = {}

    for one in typlist:
        typedict[one['id']] = one['name']
    for one in nodesVul:
        temp={}
        temp['nodeid']=one['nodeid']
        temp['nodeTypeid'] = one['nodeTypeid']
        temp['nodeName']=typedict[one['nodeid']]
        temp['vulid'] = one['vulid']
        temp['vulName']=one['vulName']
        temp['v2score'] = one['v2score']
        temp['v3score'] = one['v3score']
        temp['importance'] = one['importance']
        templist.append(temp)

    db.session.close()
    return templist
# 节点漏洞维
def getVulnerabilityScore():
    map={}
    templist = []
    array=[]
    nodes = getNodeVul()
    # nodes.reverse()
    a = len(nodes)
    for i in range(0,a):
        name = nodes[i].get('nodeName')+' '+str(nodes[i].get('nodeid'))+' '
        # print 'name',name
        # vuln = nodes[i].get('vulnerability')
        importance = float(nodes[i].get('importance'))
        v2 = float(nodes[i].get('v2score'))*0.1
        v3 = float(nodes[i].get('v3score'))*0.1
        t = importance * v2
        # name += vuln
        if(map.has_key(name)):
            map[name] = map[name]+t
        else:
            map[name] = t

    for key in map:
        temp={}
        array = key.split()
        temp['nodeid']=array[1]
        temp['nodeName']=array[0]
        # temp['vul']=array[2]
        temp['score']=map[key]
        templist.append(temp)
    return templist

# 子网漏洞维
def getSubVulnerability():
    network = creatematrinNeiber()
    graphArray = GetALlConnectedZone(network)
    count = graphArray[0][0]
    nodeVul = getVulnerabilityScore()
    templist=[]
    for i in range(1,count+1):
        graph = graphArray[i]
        sum = 0.0
        max = 0.0
        size = len(graph)
        # print 'graph',graph,'size',size
        for j in range(0,size):
            id = graph[j]
            # print 'id',id
            for k in range(0,len(nodeVul)):
                # print 'graph[i][j].get(id)',graph[i][j].get('id'),'nodeVul[k].get(nodeid',nodeVul[k].get('nodeid')
                if(int(graph[j])==int(nodeVul[k].get('nodeid'))):
                    sum += float(nodeVul[k].get('score'))
        temp={}
        temp['name']='sunbet'+str(i)
        temp['value']=round(sum,3)
        templist.append(temp)
        if(max<sum):
            max = sum
    temp = {}
    temp['name'] = 'whole network'
    temp['value'] = round(max, 3)
    templist.append(temp)
    return templist

# 获得三个维度下网络中各个子网的度量结果
def getallSubNet():
    templist = []
    # 子网链路维是度量值
    allLink = getSubnetLinksResult()
    # 子网服务维是度量值
    allService = getAllServiceResult()
    # 子网漏洞维是度量值
    allVul = getSubVulnerability()
    length = len(allLink)
    #print 'length',length
    for i in range(0,length-1):
        s1 = float(allLink[i]['value'])
        s2 = float(allService[i]['value'])
        s3 = float(allVul[i]['value'])
        sum = 0.5*s1*0.1 +0.3* s2*0.1 + 0.2*s3*0.1
        temp = {}
        temp['name']='subnet'+str(i+1)
        if sum > 0.6:
            temp['value'] = str('unsecurity')
        else:
            temp['value']=str('security')
        templist.append(temp)
    return templist

# 获得整个网络度量结果
def getAllNet():
    connect = getConnected()
    num = db.session.query(Nodeindex).all()
    db.session.close()
    count = len(num)
    allNet = getallSubNet()
    sum = 0
    for i in range(0,len(allNet)):
        if allNet[i]['value']=='security':
            sum = sum + 1

    #.安全子网的个数大于全部子网的三分之二安全

    if sum > len(allNet)*2.0/3.0:
        res = 'security'
    else:
        res = 'unsecurity'
    return res




# 获得整个网络度量结果
# def getAllnetwork():
#     resource = getAllResource()
#     service = getAllServiceResult()
#     links = getSubnetLinksResult()
#     templist=[]
#     a = len(resource)
#     # print a
#     for i in range(0,a-1):
#         sum = 0.0
#         re = float(resource[i].get('value'))
#         se = service[i].get('value')
#         li = links[i].get('value')
#         sum = re*0.33+se*0.33+0.34*li
#         temp ={}
#         temp['name']='subnet'+str(i+1)
#         temp['value']=round(sum,3)
#         if round(sum,3)<0.6:
#             temp['security']='security'
#         else:
#             temp['security'] = 'insecurity'
#         templist.append(temp)
#     re2 = float(resource[a-1].get('value'))
#     se2 = service[a-1].get('value')
#     li2 = links[a-1].get('value')
#     sum2 = re2 * 0.33 + se2 * 0.33 + 0.34 * li2
#     temp = {}
#     temp['name'] = 'whole network'
#     temp['value'] = round(sum2, 3)
#     if round(sum2, 3) < 0.6:
#         temp['security'] = 'security'
#     else:
#         temp['security'] = 'insecurity'
#     templist.append(temp)
#     return templist


if __name__ == '__main__':

    # basepath=os.path.dirname(__file__)
    # upload_path = os.path.join(basepath, '../static/upload','testdata.xlsx')
    # insertNodeandLink(upload_path)
    creatematrinNeiber()
    getConnectedIndex()
    getNodeService()
    # getAllgetServiceResult()
    # getAllResource()
    # getHostId()
    # getResource()
    # getServiceResult()

