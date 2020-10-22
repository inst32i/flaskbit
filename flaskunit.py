#*_* encoding=utf-8
import json
import sys
from datetime import datetime
from flask import render_template, request, jsonify, session, redirect,send_from_directory
from werkzeug.utils import secure_filename

from component.ManifoldService import *
from component.ConfigService import *
from component.D3Service import *
from model.Model import User, Config
from component.AHP_compute import *


defaultencoding='utf-8'
if sys.getdefaultencoding()!=defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)
app = Flask(__name__)
app.config.from_object('config.ProductConfig')

db=SQLAlchemy()
db.init_app(app)

def login_require(func):
    def decorator(*args,**kwargs):
        #现在是模拟登录，获取用户名，项目开发中获取session
        if 'username' not in session:
            return redirect("/login")
        else:
            return func(*args,**kwargs)
    decorator.func_name=func.func_name
    return decorator

@app.before_request
def before_request():
    ip = request.remote_addr
    url = request.url

    #print 'before request',ip,url


################   api     ##################

@app.route('/nodesmap')
def jsonodemap():
    node = getNode_Links()
    return jsonify(node)
@app.route('/nodetype')
def jsonodetype():
    nodetype=getNodetype()
    return jsonify(nodetype)
@app.route('/download/<filename>',methods=['GET'])
def downtemplate(filename):
    dirpath = os.path.join(app.root_path, 'static/template')  # 这里是下在目录，从工程的根目录写起，比如你要下载static/js里面的js文件，这里就要写“static/js”

    return send_from_directory(dirpath, filename, as_attachment=True)

@app.route('/heatmap/<series>',methods=['GET'])
def showheatmap(series):
    resultseries = computeSingleNodeValue()
    key=resultseries.keys()[int(series)]
    mat=resultseries[key]['weimat']
    return jsonify(mat.tolist())
@app.route('/evalresult',methods=['GET'])
def evalresult():
    resultseries = computeSingleNodeValue()
    result={}
    result['x']=[]
    result['y']=[]

    resultlist=[]
    for key in resultseries :
        resultlist.append({'x':key,'y':resultseries[key]['indexsum']})

    resultlist.sort(key=lambda x: x["x"])

    for one in resultlist:
        result['x'].append(one['x'])
        result['y'].append(one['y'])
    return jsonify(result)



@app.route('/servicetype')
def jsonservicetype():
    servicetype=getServiceType()
    return jsonify(servicetype)

#################        page ####################
@app.route('/')
# # @login_require
def rootpage():
    return render_template('index.html',menu=getMenu())
@app.route('/login')
def login():
   return render_template('index.html',menu=getMenu())
 #  return render_template('login.html')
@app.route('/loginout')
def loginout():
    if 'username' in session:
        session.pop('username')
    return render_template('login.html')
@app.route('/config')
# # @login_require
def config():
    username = session.get('username', '')
    userid = session.get('userid')
    return render_template('config.html', menu=getMenu(), menuall=getallmenu(), nodetype=queryallnodetype(userid),servicetype=queryallservicetype(userid),assessment = queryallAssessment(userid),asslen = len(queryallAssessment(userid)))

@app.route('/manifold')
# # @login_require
def manifold():

    manifold=Config.query.filter_by(name='compute_martix').first()
    data={}
    data['manifold']=manifold.value
    neibor=creatematrinNeiber()
    data['martixneibor']=neibor
    data['neiborlen']=len(neibor)

    indexseries= computeSingleNodeValue()

    # col,row=nodeindex.shape
    # data['index'] =nodeindex
    indexsum=[]
    for key in indexseries:
        indexsum.append({'x':key,'y':indexseries[key]['indexsum']})
    indexsum.sort(key=lambda x:x['x'])
    data['result'] = indexsum
    # data['index_col']=col
    # data['index_row']=row
    keys=indexseries.keys()
    keyone=keys[3]
    #第一个时刻的计算值
    example=indexseries[keyone]
    #第一个时刻的主机值
    examplekeys=example.keys()
    keyunit=examplekeys[1]
    examhost=example[keyunit]
    indexmatrix=examhost['index'].tolist()
    examhost['index']=indexmatrix

    return render_template('manifold_show.html',data=data,menu=getMenu(),example=example,examhost=examhost)

@app.route('/templatecreate')
def templatecreate():
    servicetype=db.session.query(ServiceType).all()
    indexintrolist=db.session.query(Indexintro).filter(Indexintro.isworking == "1").all()
    userid=session.get('userid')
    data={}
    data['indexlist']=indexintrolist
    data['servicelist']=servicetype
    data['nodetypelist']=queryallnodetype(userid)
    return render_template('templatecreate.html',menu=getMenu(),data=data)
@app.route('/d3mhl')
# # @login_require
def d3mhl():
    nodes = getnodes2()
    links = getLinks2()
    connectedCount = getConnected()
    # sum = getAllResource()
    # 节点服务展示
    services = getNodeService()
    # 计算节点服务
    nodesService = getAllNodeResult()
    # 子网服务
    serviceAll = getAllServiceResult()
    # nodesService = getAllNodeServiceResult()
    # 节点链路
    linksResult = getAllgetLinksResult()
    # 子网链路
    subLinks = getSubnetLinksResult()
    # allnetwork=getAllnetwork()
    # 连通分量个数
    connectResult = getConnectedResult()
    # indexs = getIndexs()
    # 节点漏洞
    vulnerabilities = getVulnerabilityScore()
    # 节点漏洞展示
    node_vul = getNodeVul()
    # 计算子网漏洞
    subVulnerability = getSubVulnerability()
    # 获得每一个节点每一指标度量值
    allDynIndex = getDynAllIndexValue()
    # 获得每一个节点所有指标度量值
    allNetIndex  = getNetAllIndex()
    # 获得子网指标度量值
    subIndexValue = getSubIndexValue()
    # 网络度量结果
    allSubNet = getallSubNet()
    allNet = getAllNet()


    # print d1
    return render_template('d3mhl.html', menu=getMenu(), nodes=nodes, connectedCount=connectedCount,
                           services=services, serviceAll=serviceAll, nodesService=nodesService,
                           links=links, linksResult=linksResult, subLinks=subLinks, connectResult=connectResult,
                           node_vul=node_vul, vulnerabilities=vulnerabilities, subVulnerability=subVulnerability,allDynIndex = allDynIndex,allNetIndex=allNetIndex,
                           subIndexValue=subIndexValue,allSubNet=allSubNet,allNet=allNet)

@app.route('/d3mhlinputdata',methods=['POST'])
# # @login_require
def d3mhlinputdata():
    f = request.files['file']
    basepath = os.path.dirname(__file__) # 当前文件所在路径
    upload_path = os.path.join(basepath, 'static/upload', secure_filename(f.filename))#注意：没有的文件夹一定要先创建，不然会提示没有该路径
    f.save(upload_path)

    print upload_path
    data = xlrd.open_workbook(upload_path)
    table = data.sheets()[0]
    nrows = table.nrows
    ncols = table.ncols
    for row in xrange(1, nrows):
        # a = int(table.cell(row, 0).value)
        b = int(table.cell(row, 0).value)
        c = table.cell(row, 1).value
        d = int(table.cell(row, 2).value)
        e = table.cell(row, 3).value
        d3t = D3mhl(b, c, d, e)
        d3t.insert()
        # print a, b, c, d
    return jsonify({})



@app.route('/output')
# # @login_require
def output():
    return render_template('output.html',menu=getMenu())
@app.route('/input')
# # @login_require
def input():
    data={}
    data['templist']=db.session.query(Template).all()
    return render_template('input.html',menu=getMenu(),data=data)



#AHP,zch,2018-05-26
@app.route('/ahp')
# # @login_require
def ahp():
    Top1 = get_judgementmatrix(0)
    E1   = get_judgementmatrix(1)
    E2   = get_judgementmatrix(2)
    E3   = get_judgementmatrix(3)
    S1   = get_assessment(1)
    S2   = get_assessment(2)
    S3   = get_assessment(3)
    S4   = get_assessment(4)
    S5   = get_assessment(5)
    top1_weights = get_top1_weights()
    indexlist = get_indexlist()
    index = get_indexdescription(indexlist,4)
    E1_index = get_indexdescription_eachlayer(indexlist,top1_weights,1)
    E2_index = get_indexdescription_eachlayer(indexlist,top1_weights,2)
    E3_index = get_indexdescription_eachlayer(indexlist,top1_weights,3)
    index_weights = get_index_weights()
    assess_result = get_index_assessment()
    AHP_result = AHP()
    AHP_review = get_review(AHP_result['value'])
    #upload_weights()
    return render_template('ahp.html',Top1=Top1,E1=E1,E2=E2,E3=E3,S1=S1,S2=S2,S3=S3,S4=S4,S5=S5,indexlist=indexlist,index=index,E1_index=E1_index,E2_index=E2_index,E3_index=E3_index,index_weights=index_weights,AHP_result=AHP_result,AHP_review=AHP_review,top1_weights=top1_weights,assess_result=assess_result,menu=getMenu())


@app.route('/inputdata',methods=['POST'])
# # @login_require
def input_POST():
    f = request.files['file']
    basepath = os.path.dirname(__file__)
    upload_path = os.path.join(basepath, 'static/upload', secure_filename(f.filename))
    f.save(upload_path)
    insertNodeandLink(upload_path)
    insertJudgementMatrix(upload_path)
    insertNodeService(upload_path)
    insertNodeVul(upload_path)
    #consistency_test()

    return jsonify({})


@app.route('/changemenu',methods=['POST'])
# # @login_require
def changemenu():
    val=request.get_json()
    menu=Menu(val['path'],val['page'],val['visible'],val['sortid'],val['name'],val['imgurl'],val['id'])
    menu.update()

    return jsonify({'code':200})


@app.route('/addmenu',methods=['POST'])
# # @login_require
def addmenu():
    val=request.form
    menu=Menu(val.get('path'),val.get('page'),val.get('visible'),val.get('sortid'),val.get('name'),val.get('imgurl'))
    menu.insert()

    return jsonify({'code':200})

@app.route('/addtemplate',methods=['POST'])
# # @login_require
def addtemplate():
    val=request.form
    templatename=val.get('templatename',type=str,default='')
    nodesize=val.get('nodesizes',type=int,default=10)
    if templatename=='':
        return jsonify({'code': 500})
    template=Template(templatename,nodesize)
    argslist=val.getlist('args')
    #将argslist作为列保存到xls中，
    sheetlist = db.session.query(Sheet).all()
    sheetdict = {}
    for one in sheetlist:
        key = one['sheetname']
        if not sheetdict.has_key(key):
            sheetdict[key] = []
        sheetdict[key].append(one)
    for key in sheetdict.keys():
        sheetdict[key].sort(key=lambda x: x['sortid'])
    newsheet={}
    for key in sheetdict.keys():
        if not newsheet.has_key(key):
            newsheet[key]=[]
        sheetlist=sheetdict[key]
        for one in sheetlist:
            newsheet[key].append(one['colname'])

    if newsheet.has_key('node'):
        #将新的指标加进模板中
        newsheet['node'].extend(argslist)
    #将写的名字和时间的hash作为名字
    dt = datetime.datetime.now()
    filename=templatename+dt.strftime('%Y%m%d%H%M%S')+'.xls'
    #保存到本地并添加进数据库
    dirpath = os.path.join(app.root_path, 'static/template/')
    if savexls(newsheet,dirpath+filename):
        template.path=filename
        template.insert()
        #返回保存路径
        return jsonify({'code':200,'path':'/download/'+filename})
    else:
        return jsonify({'code': 500})
@app.route('/changeServicetype',methods=['POST'])
# # @login_require
def changeServicetype():
    form = request.form
    userid = session.get('userid')
    service=ServiceType(userid,form.get('name'),form.get('id'))
    service.update()
    return jsonify({'code':200})

@app.route('/addServicetype',methods=['POST'])
# # @login_require
def addServicetype():
    form = request.form
    userid = session.get('userid')
    service = ServiceType(userid,form.get('name'))
    result = service.insert()
    if result:
        return jsonify({'code': 200})
    return jsonify({'code': 500, 'msg': 'change error in server'})

@app.route('/deleteServicetype',methods=['POST'])
# # @login_require
def deleteServicetype():
    form = request.form
#    print form.get('name'),'-----------'
#    userid = session.get('userid')
#    service = ServiceType(userid,form.get('name'),form.get('id'))
#    result = service.delete()
    res = ServiceType.query.filter(ServiceType.id == form.get('id')).first()
    ServiceType.delete(res)
    #deleteServiceType(form.get('id'))
    #result = deleteServiceType()
    return jsonify({'code': 200})


@app.route('/changejudgement',methods=['POST'])
# # @login_require
def changejudgement():
    form=request.form
    userid = session.get('userid')
#    print '------',queryalljudgement(userid)
    if queryalljudgement(userid):
        service = judgementmatrix(form.get('E1thanE2'), form.get('E1thanE3'), form.get('E2thanE3'),
                                  form.get('Q1thanQ2'), form.get('Q1thanQ3'), form.get('Q1thanQ4'),
                                  form.get('Q2thanQ3'), form.get('Q2thanQ4'), form.get('Q3thanQ4'),
                                  form.get('Q5thanQ6'), form.get('Q5thanQ7'), form.get('Q5thanQ8'),
                                  form.get('Q5thanQ9'), form.get('Q6thanQ7'), form.get('Q6thanQ8'),
                                  form.get('Q6thanQ9'), form.get('Q7thanQ8'), form.get('Q7thanQ9'),
                                  form.get('Q8thanQ9'), form.get('Q10thanQ11'), userid,form.get('id'))
        service.update()
        return jsonify({'code': 200})
    else:
        service = judgementmatrix(form.get('E1thanE2'), form.get('E1thanE3'), form.get('E2thanE3'),
                                  form.get('Q1thanQ2'), form.get('Q1thanQ3'), form.get('Q1thanQ4'),
                                  form.get('Q2thanQ3'), form.get('Q2thanQ4'), form.get('Q3thanQ4'),
                                  form.get('Q5thanQ6'), form.get('Q5thanQ7'), form.get('Q5thanQ8'),
                                  form.get('Q5thanQ9'), form.get('Q6thanQ7'), form.get('Q6thanQ8'),
                                  form.get('Q6thanQ9'), form.get('Q7thanQ8'), form.get('Q7thanQ9'),
                                  form.get('Q8thanQ9'), form.get('Q10thanQ11'), userid)
        service.insert()
        return jsonify({'code': 200})
    #else:
    #   return jsonify({'code':500})

@app.route('/changeAssessment',methods=['POST'])
# # @login_require
def changeassessment():
    form=request.form
    userid = session.get('userid')
    service = Assessment( form.get('element'), form.get('S1'), form.get('S2'), form.get('S3'), form.get('S4'), form.get('S5'),userid,form.get('id'))
    service.update()
    return jsonify({'code': 200})

@app.route('/addAssessment',methods=['POST'])
# # @login_require
def addassessment():
    form = request.form
    userid = session.get('userid')
    ele = form.get('element')
    num = filter(str.isdigit,ele.encode("utf-8"))
    numm = int(num)
    if numm > 11:
        return jsonify({'code':300})
    else:
        service = Assessment(form.get('element'),form.get('S1'), form.get('S2'), form.get('S3'), form.get('S4'), form.get('S5'),userid)
        service.insert()
        return jsonify({'code': 200})

@app.route('/deleteAssessment',methods=['POST'])
# # @login_require
def deleteAssessment():
    form = request.form
    res = Assessment.query.filter(Assessment.id == form.get('id')).first()
    Assessment.delete(res)
    return jsonify({'code': 200})

@app.route('/addjudgement',methods=['POST'])
# # @login_require
def addjudgement():
    form = request.form
#    print form
    userid = session.get('userid')
    service = judgementmatrix(userid,form.get('E1thanE2'),form.get('E1thanE3'),form.get('E2thanE3'),form.get('Q1thanQ2'),form.get('Q1thanQ3'),form.get('Q1thanQ4'),form.get('Q2thanQ3'),form.get('Q2thanQ4'),form.get('Q3thanQ4'),form.get('Q5thanQ6'),form.get('Q5thanQ7'),form.get('Q5thanQ8'),form.get('Q5thanQ9'),form.get('Q6thanQ7'),form.get('Q6thanQ8'),form.get('Q6thanQ9'),form.get('Q7thanQ8'),form.get('Q7thanQ9'),form.get('Q8thanQ9'),form.get('Q10thanQ11'))
    result = service.insert()
    if result:
        return jsonify({'code': 200})
    return jsonify({'code': 500, 'msg': 'change error in server'})

@app.route('/deletejudgement',methods=['POST'])
# # @login_require
def deletejudgement():
    form = request.form
    #service = AhpConfig(form.get('id'))
    #result = service.delete()
    res = judgementmatrix.query.filter(judgementmatrix.id == form.get('id')).first()
    judgementmatrix.delete(res)
    return jsonify({'code': 200})

@app.route('/deletenodetype',methods=['POST'])
# # @login_require
def deletenodetype():
    form = request.form
    print form
    #service = AhpConfig(form.get('id'))
    #result = service.delete()
    res = NodeType.query.filter(NodeType.id == form.get('id')).first()
    NodeType.delete(res)
    return jsonify({'code': 200})

@app.route('/changenodetype',methods=['POST'])
# # @login_require
def changenodetype():
    form=request.form
    node=NodeType(form.get('name'),form.get('imgurl'),form.get('id'))
    result=node.update()
    if result:
        return jsonify({'code':200})
    return jsonify({'code':500,'msg':'change error in server'})

@app.route('/addnodetype',methods=['POST'])
# # @login_require
def addnodetype():
    form = request.form
    node = NodeType(form.get('name'), form.get('imgurl'))
    result = node.insert()
    if result:
        return jsonify({'code': 200})
    return jsonify({'code': 500, 'msg': 'change error in server'})

@app.route('/login',methods=['POST'])
def login_post():
    username=request.form['username']
    password=request.form['password']
#    user=User(username)
    userexist=User.query.filter_by(username=username).first()
    if userexist:
        session['username']=username
        session['userid']=userexist.id
        return redirect('/')
    else:
        return render_template('login.html',username=username,password=password,errinfo='用户名密码错误')


@app.route('/test')
def testhtml():
    node = get_t_observedata(0)
    return render_template('test.html',node=node,menu=getMenu())



if __name__ == '__main__':
    app.debug=False
    app.port=8000
    app.run(host='0.0.0.0',port=8000)
