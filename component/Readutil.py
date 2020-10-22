# *-* encoding:utf-8 *-*
# usr/bin/python 2.7
'''
  @author  chenquanbao
  @email  kenybens@gmail.com
  @time: 2018/3/22 下午6:49 
'''

import xlrd
import csv
from datetime import datetime
from xlrd import xldate_as_tuple
import os
import shutil
import xlwt

def readCSV(filename):
    csvfile=open(filename,'r')
    reader=csv.reader(csvfile)
    result={}
    for item in reader:
        if item==1:
            continue
        result[item[0]]=item[1]
    csvfile.close()
#    print result
    return result
def open_excel(filename):
    try:
        data=xlrd.open_workbook(filename)
        return data
    except Exception as e:
        print str(e)


def readxls(filename,colnameindex=0,by_name=u'Sheet1'):
    data=open_excel(filename)

    table=data.sheet_by_name(by_name)
    nrows=table.nrows
    colnames=table.row_values(colnameindex)
    list=[]
    for rownum in range(2,nrows):
        row=table.row_values(rownum)
        if row:
            app={}
            for i in range(len(colnames)):

                ctype=table.cell(rownum,i).ctype
                cell=row[i]
                if ctype==2 and cell%1==0:
                    cell=int(cell)
                elif ctype==3:
                    date=datetime(*xldate_as_tuple(cell,0))
                    cell=date.strftime('%Y-%d-%m %H:%M:%S')
                elif ctype==4:
                    cell=True if cell==1 else False
                app[colnames[i]]=cell
            list.append(app)
    return list

def copyfile(srcfile,dstfile):
    if not os.path.isfile(srcfile):
        print "%s not exist!"%(srcfile)
    else:
        fpath,fname=os.path.split(dstfile)    #分离文件名和路径
        if not os.path.exists(fpath):
            os.makedirs(fpath)                #创建路径
        shutil.copyfile(srcfile,dstfile)      #复制文件
        print "copy %s -> %s"%( srcfile,dstfile)


def savexls(dictsheet,filepath):
    workbook = xlwt.Workbook(encoding='ascii')
    for key in dictsheet.keys():
        sheetunit=workbook.add_sheet(key)
        for index in range(len(dictsheet[key])):

            sheetunit.write(0,index,dictsheet[key][index])
    try:
        workbook.save(filepath)
        return True
    except IOError as e:
        return False

if __name__ == '__main__':
    # tables=readxls('originalDDOS.xlsx')
    # for row in tables:
    #     print row
    result=readCSV('originalDDOS.csv')
    print result



