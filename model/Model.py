# *-* encoding:utf-8 *-*
# usr/bin/python 2.7
'''
  @author  chenquanbao
  @email  kenybens@gmail.com
  @time: 2018/3/22 下午2:01
'''
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import time
from sqlalchemy import func,or_
from config import Config
app = Flask(__name__)
app.config['SECRET_KEY']=Config.SECRET_KEY
'''密码和用户名不要改动，在数据库里面请添加这个用户名和密码'''
app.config['SQLALCHEMY_DATABASE_URI']=Config.SQLALCHEMY_DATABASE_URI
#app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:mysqladmin@localhost/manifoldb'
#app.config['SQLALCHEMY_DATABASE_URI']='mysql://manifold:manifold@localhost/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=Config.SQLALCHEMY_TRACK_MODIFICATIONS

db=SQLAlchemy()
db.init_app(app)

class User(db.Model):
    __tablename__='user'
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(80),unique=True)
    email=db.Column(db.String(320),unique=True)
    phone=db.Column(db.String(32),nullable=False)
    def __init__(self,id,username,email='',phone=''):
        self.id=id
        self.username=username
        self.email=email
        self.phone=phone
    def __repr__(self):
        return '<User(id=%s,name=%s)>'%(
            self.id,
            self.username,
        )
class Template(db.Model):
    __tablename__='template'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50),nullable=False)
    path=db.Column(db.String(255),nullable=False)
    isworking=db.Column(db.SmallInteger)
    size=db.Column(db.Integer)
    def __init__(self,name,size,path='',isworking=1):
        self.name=name
        self.size=size
        self.path=path
        self.isworking=isworking
    def insert(self):
        db.session.add(self)
        db.session.commit()
        return self

class Sheet(db.Model):
    __tablename__='sheet'
    id=db.Column(db.Integer,primary_key=True)
    sheetname=db.Column(db.String(50),nullable=False)
    colname=db.Column(db.String(250),nullable=False)
    sortid=db.Column(db.Integer)

    def __getitem__(self, item):
        if item=='id':
            return self.id
        elif item=='sheetname':
            return self.sheetname
        elif item=='colname':
            return self.colname
        elif item=='sortid':
            return self.sortid
        else:
            return None



class Indexintro(db.Model):
    """introduction of index"""
    __tablename__='indexintro'
    id=db.Column(db.Integer,primary_key=True)
    indexname=db.Column(db.String(50),nullable=False)
    description=db.Column(db.String(255),nullable=True)
    isworking=db.Column(db.SmallInteger)

class Indexrecord(db.Model):
    __tablename__='indexrecord'
    id=db.Column(db.Integer,primary_key=True)
    nodeid=db.Column(db.Integer,nullable=False)
    indexname=db.Column(db.String)
    value=db.Column(db.Float)
    create_time = db.Column(db.TIMESTAMP)
    update_time=db.Column(db.TIMESTAMP)
    def __init__(self,nodeid,indexname,value,create_time=time.time()):
        self.nodeid=nodeid
        self.indexname=indexname
        self.value=value
        self.create_time=create_time

# 增加3个属性，zym,2018.04.11
class Nodeindex(db.Model):
    """index of node"""
    __tablename__='nodeindex'
    id=db.Column(db.Integer,primary_key=True)
    nodeid=db.Column(db.Integer,nullable=False)
    nodeTypeid=db.Column(db.Integer,nullable=False)
    importance = db.Column(db.String(32), nullable=True)
    create_time = db.Column(db.TIMESTAMP)

    def __init__(self, id, nodetypeid,create_time=time.time(),importance=0):
        self.nodeid = id
        self.nodeTypeid = nodetypeid
        self.importance=importance
        self.create_time=create_time

    def __getitem__(self,k):
        if k=='id':
            return self.nodeid
        elif k =='nodeTypeid':
            return self.nodeTypeid
        elif k =='importance':
            return self.importance
        elif k=='nodeid':
            return self.nodeid


class Noderelate(db.Model):
    """relationship of nodes"""
    __tablename__='noderelates'
    id=db.Column(db.Integer,primary_key=True)
    pid=db.Column(db.Integer,nullable=False)
    cid=db.Column(db.Integer,nullable=False)
    importance = db.Column(db.String(32), nullable=False)
    update_time=db.Column(db.TIMESTAMP)
    def __init__(self,id,pid,cid,importance,time=time.time()):
        self.id=id
        self.pid=pid
        self.cid=cid
        self.importance = importance
        self.update_time=time
    def __getitem__(self,k):
        if k=='id':
            return self.id
        elif k =='pid':
            return self.pid
        elif k =='cid':
            return self.cid


class NodeType(db.Model):
    __tablename__='nodetype'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(32),nullable=False)
    imgurl=db.Column(db.String(255),nullable=True)
    userid=db.Column(db.String(20),nullable=False)
    def __init__(self,userid,name,imgurl,id=None):
        self.id=id
        self.name=name
        self.imgurl=imgurl
        self.userid
    def insert(self):
        db.session.add(self)
        db.session.commit()
        return self
    def update(self):
        db.session.merge(self)
        db.session.flush()
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Menu(db.Model):
    __tablename__='menu'
    id=db.Column(db.Integer,primary_key=True)
    path=db.Column(db.String(255),nullable=True)
    page=db.Column(db.String(255),nullable=True)
    name=db.Column(db.String(30))
    parentid=db.Column(db.Integer,default=-1)
    imgurl = db.Column(db.String(255), nullable=True)
    isvisible=db.Column(db.Integer,default=1)
    sortid=db.Column(db.Integer)
    def __init__(self,path,page,isvisible,sortid,name,imgurl,id=None,parentid=-1):
        self.path=path
        self.page=page
        self.parentid=parentid
        self.imgurl=imgurl
        self.isvisible=isvisible
        self.id=id
        self.sortid=sortid
        self.name=name
    def insert(self):
        db.session.add(self)
        db.session.commit()
        return self
    def update(self):
        db.session.merge(self)
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()

#增加安全评估表，zch,2018-05-20
class Assessment(db.Model):
    __tablename__='assessment'
    id = db.Column(db.Integer, primary_key=True)
    element = db.Column(db.String(50), nullable=False)
    S1 = db.Column(db.Float, nullable=False)
    S2 = db.Column(db.Float, nullable=False)
    S3 = db.Column(db.Float, nullable=False)
    S4 = db.Column(db.Float, nullable=False)
    S5 = db.Column(db.Float, nullable=False)
    userid=db.Column(db.Integer,nullable=False)
    def __init__(self,element,S1,S2,S3,S4,S5,userid,id=None):
        self.id = id
        self.S1 = S1
        self.S2 = S2
        self.S3 = S3
        self.S4 = S4
        self.S5 = S5
        self.element = element
        self.userid = userid
    def insert(self):
        db.session.add(self)
        db.session.commit()
        return self
    def update(self):
        db.session.merge(self)
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()

#增加判断矩阵表,zch,2018-05-20
class AHPJudgement(db.Model):
    __tablename__ = 'ahpjudgement'
    id = db.Column(db.Integer,primary_key=True)
    indexid = db.Column(db.Integer,nullable=False)
    pid = db.Column(db.Integer,nullable=False)
    cid = db.Column(db.Integer,nullable=False)
    value = db.Column(db.Float,nullable=False)
    def __init__(self,indexid,pid,cid,value,id=None):
        #self.id=id
        self.indexid=indexid
        self.pid=pid
        self.cid=cid
        self.value=value
    def __getitem__(self,k):
        if k=='id':
            return self.id
        elif k =='indexid':
            return self.indexid
        elif k =='pid':
            return self.pid
        elif k =='cid':
            return self.cid
        elif k =='value':
            return self.value


#增加权重树，zch,2018-05-20
class AHPTree(db.Model):
    __tablename_ = 'ahp_tree'
    id = db.Column(db.Integer,primary_key=True)
    pid = db.Column(db.Integer,nullable=False)
    importance = db.Column(db.Float,nullable=False)
    def __init__(self,id,pid,importance):
        self.id=id
        self.pid=pid
        self.importance=importance
    def __getitem__(self,k):
        if k=='id':
            return self.id
        elif k =='pid':
            return self.pid
        elif k =='importance':
            return self.importance


class Config(db.Model):
    __tablename__='config'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(255),unique=True)
    value=db.Column(db.String(255))
    isvisible=db.Column(db.Integer,default=1)
    created_time = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self,name,value,isvisible):
        self.name=name
        self.value=value
        self.isvisible=isvisible

# 节点_漏洞表
class Node_vul(db.Model):
    __tablename='node_vul'
    id = db.Column(db.Integer,primary_key=True)
    nodeid = db.Column(db.Integer,nullable=False)
    vulid = db.Column(db.Integer,nullable=False)

    def __init__(self,nodeid,vulid,id=None):
        # self.id = id
        self.nodeid = nodeid
        self.vulid = vulid
    def __getitem__(self,k):
        if k=='id':
            return self.id
        elif k =='nodeid':
            return self.nodeid
        elif k =='vulid':
            return self.vulid

# 节点_服务表
class Node_ser(db.Model):
    __tablename = 'node_ser'
    id = db.Column(db.Integer, primary_key=True)
    nodeid = db.Column(db.Integer, nullable=False)
    serviceid = db.Column(db.Integer, nullable=False)
    importance = db.Column(db.String(32),nullable=False,default=0.5)
    port = db.Column(db.Integer,nullable=False)

    def __init__(self,nodeid, serviceid,importance,port,id = None):
        # self.id = id
        self.nodeid = nodeid
        self.serviceid = serviceid
        self.importance = importance
        self.port = port

    def __getitem__(self, k):
        if k == 'nodeid':
            return self.nodeid
        elif k == 'serviceid':
            return self.serviceid
        elif k == 'importance':
            return self.importance
        elif k == 'port':
            return self.port
# 漏洞表
class Vulnerability(db.Model):
    __tablename__='vulnerability'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(32),nullable=False)
    v2score = db.Column(db.String,nullable=False)
    v3score = db.Column(db.String,nullable=False)
    def __init__(self,name,v2score,v3score,id=None):
        # self.id=id
        self.name=name
        self.v2score = v2score
        self.v3score = v3score

    def __getitem__(self, k):
        if k == 'name':
            return self.name
        elif k == 'v2score':
            return self.v2score
        elif k == 'v3score':
            return self.v3score
# 服务表
class ServiceType(db.Model):
    __tablename__='servicetype'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(32),nullable=False)
    userid=db.Column(db.String(20),nullable=False)
    def __init__(self,userid,name,id=None):
        self.id=id
        self.name=name
        self.userid=userid
    def insert(self):
        db.session.add(self)
        db.session.commit()
        return self
    def update(self):
        db.session.merge(self)
        db.session.flush()
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()


if __name__ == '__main__':
    db.create_all()

    # inset = User(username='itmin', email='1608500576@qq.com', phone='17801071701')
    #db.session.add(inset)
    #db.session.commit()
