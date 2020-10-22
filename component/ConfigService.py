# *-* encoding:utf-8 *-*
# usr/bin/python 2.7
'''
  @author  chenquanbao
  @email  kenybens@gmail.com
  @time: 2018/4/20 上午10:58 
  请将配置服务的函数写在这里
'''
from model.Model import *
import numpy as np
from component.Readutil import *
import Queue
import os
import math


def getMenu():
    return db.session.query(Menu).filter(Menu.isvisible==1).order_by(Menu.sortid).all()
def getallmenu():
    return db.session.query(Menu).order_by(Menu.sortid).all()

def queryallnodetype(id):
    return NodeType.query.filter(NodeType.userid==id).all()
def getNodetype():
    templist={}
    res=db.session.execute("select id,name,imgurl  from nodetype").fetchall()
    db.session.close()
    for one in res:
        templist[one['id']]={'id':one['id'],'name':one['name'],'imgurl':one['imgurl']}
    return templist



def queryallservicetype(id):
    return ServiceType.query.filter(ServiceType.userid==id).all()

def getServiceType():
    templist = {}
    res = db.session.execute("select id,name,userid  from servicetype").fetchall()
    db.session.close()
    for one in res:
        templist[one['id']] = {'id': one['id'], 'name': one['name'], 'userid':one['userid']}
    return templist


def queryalljudgement(id):
    return judgementmatrix.query.filter(judgementmatrix.userid == id).first()

def getjudgement():
    templist = {}
    res = db.session.execute("select E1thanE2,E1thanE3,E2thanE3,Q1thanQ2,Q1thanQ3,Q1thanQ4,Q2thanQ3,Q2thanQ4,Q3thanQ4,Q5thanQ6,Q5thanQ7,Q5thanQ8,Q5thanQ9,Q6thanQ7,Q6thanQ8,Q6thanQ9,Q7thanQ8,Q7thanQ9,Q8thanQ9,Q10thanQ11,userID,id  from JudgementMatrix").fetchall()
    db.session.close()
    for one in res:
        templist[one['id']] = {'id': one['id'], 'E1thanE2':one['E1thanE2'],'E1thanE3':one['E1thanE3'],'E2thanE3': one['E2thanE3'],'Q1thanQ2': one['Q1thanQ2'], 'Q1thanQ3': one['Q1thanQ3'], 'Q1thanQ4': one['Q1thanQ4'], 'Q2thanQ3': one['Q2thanQ3'],'Q2thanQ4': one['Q2thanQ4'],'Q3thanQ4': one['Q3thanQ4'],'Q5thanQ6': one['Q5thanQ6'],'Q5thanQ7': one['Q5thanQ7'],'Q5thanQ8': one['Q5thanQ8'],'Q5thanQ9': one['Q5thanQ9'],'Q6thanQ7': one['Q6thanQ7'],'Q6thanQ8': one['Q6thanQ8'],'Q6thanQ9': one['Q6thanQ9'],'Q7thanQ8': one['Q7thanQ8'],'Q7thanQ9': one['Q7thanQ9'],'Q8thanQ9': one['Q8thanQ9'],'Q10thanQ11': one['Q10thanQ11'],'userid':one['userid']}
    return templist


def queryallAssessment(id):
    return Assessment.query.filter(Assessment.userid == id).all()


def getAssessment():
    templist = {}
    res = db.session.execute("select id,S1,S2,S3,S4,S5,element,userid  from assessment").fetchall()
    db.session.close()
    for one in res:
        templist[one['id']] = {'id': one['id'], 'S1':one['S1'],'S2':one['S2'],'S3':one['S3'],'S4':one['S4'],'S5':one['S5'],'element':one['element'], 'userid':one['userid']}
    return templist


if __name__ == '__main__':
    print('Hello World')