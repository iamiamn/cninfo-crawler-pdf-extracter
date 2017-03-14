#处理excel。获得pdf自动下载地址
import xlrd
import re
import socket
from bs4 import BeautifulSoup
import urllib.request
import time
#记录所有在excel中取得的数据
def getList():
    data = xlrd.open_workbook('./Testing Data.xlsm')
    sheet = data.sheets()[0]
    allListFile = open('./allList.txt', 'w', encoding = 'utf-8')

    # 注意忽略前三行时，所有列都要忽略前三行
    startNum = 3;
    nRows = sheet.nrows
    col2 = sheet.col_values(1)
    urlList = col2[startNum:nRows]
    # col3 = sheet.col_values(2)
    # comp1List = col3[startNum:nRows]
    # col4 = sheet.col_values(3)
    # comp2List = col4[startNum:nRows]


    allListFile.write('\n'.join(urlList))
    allListFile.close()



    #处理数据
    pageList = []
    pageName = []
    #记录获得的pdf下载地址，用于自动下载
    downloadName = []
    downloadList = []
    #记录pdf下载失败的地址，手动下载
    notOkList = []
    notOkName = []
    totalNumUrl = len(urlList)
    patternIllegal = r'[^\\/\*\?"<>|]+'#必须加上+不然变成每个字断开
    for index in range(totalNumUrl):
        temp = re.findall(r'^http.+', urlList[index])
        if not (temp):
            continue
        else:
            url = temp[0]
        #删除文件名中的非法字符
        tempName = 'testmerge' + str(index) + '.pdf'
        nameResults = re.findall(patternIllegal, tempName)
        saveName = '_'.join(nameResults)
        #如果直接是pdf下载地址直接存入dllist
        pattern1 = r'(http.+?PDF)'
        finded = re.findall(pattern1, url)
        if (finded):
            downloadList.append(url)
            downloadName.append(saveName)
        else:
            pageList.append(url)
            pageName.append(saveName)
    print(len(pageList), ' ', len(pageName))

    # 非直接下载地址，从页面获取下载地址到oklist，获取失败放入failList
    socket.setdefaulttimeout(20)#设置超时时间
    numPageList = len(pageList)
    for index in range(numPageList):
        url = pageList[index]
        # print(index, url)
        name = pageName[index]
        # print('i am try' + str(index))
        try:
            html = urllib.request.urlopen(url)
            # print('i am hear' + str(index))
            content = html.read()
            soup = BeautifulSoup(content, 'html.parser')
            getContent = soup.find(attrs = {'class' : r'btn-blue bd-btn'})
            tags = getContent('a')
            pattern = r'"/(cninfo-new.+?)"'
            stringFinded = re.findall(pattern, str(tags))#用search的结果难处理，用findall得到list
            dlAddress = 'http://www.cninfo.com.cn/' + stringFinded[0]
            downloadList.append(dlAddress)
            downloadName.append(name)
            time.sleep(5)
        except:
            notOkList.append(url)
            notOkName.append(name)
            time.sleep(10)
            continue

    print(len(downloadList), ' ', len(downloadName))

    downloadFile = open('downloadFile.txt', 'w', encoding = 'utf-8')
    downloadFile.write('\ndownloadList\n')
    downloadFile.write('\n'.join(downloadList))
    downloadFile.write('\ndownloadName\n')
    downloadFile.write('\n'.join(downloadName))
    downloadFile.close()

    notOkFile = open('notOkFile.txt', 'w', encoding = 'utf-8')
    notOkFile.write('\nnotOkList\n')
    notOkFile.write('\n'.join(notOkList))
    notOkFile.write('\nnotOkName\n')
    notOkFile.write('\n'.join(notOkName))
    notOkFile.close()

def checkFail():
    '''检查notOkFile的情况，返回剩余的未成功获取下载地址数'''
    fhand = open('notOkFile.txt', 'r', encoding = 'utf-8')
    content = fhand.read()
    fhand.close()
    patternUrl = r'notOkList\n(.+?)\nnotOkName'
    patternName = r'notOkName\n(.+)'
    try:
        urlPart = (re.findall(patternUrl, content, re.S))[0]#匹配多行记得加re.S
        namePart = (re.findall(patternName, content, re.S))[0]
    except:
        return 0
    print(urlPart)
    print(namePart)
    pageList = urlPart.splitlines()
    pageName = namePart.splitlines()
    numPageList = len(pageList)
    if (numPageList == 0):return 0
    downloadList = []
    downloadName = []
    notOkList = []
    notOkName = []
    for index in range(numPageList):
        url = pageList[index]
        # print(index, url)
        name = pageName[index]
        # print('i am try' + str(index))
        try:
            html = urllib.request.urlopen(url)
            # print('i am hear' + str(index))
            content = html.read()
            soup = BeautifulSoup(content, 'html.parser')
            getContent = soup.find(attrs = {'class' : r'btn-blue bd-btn'})
            tags = getContent('a')
            pattern = r'"/(cninfo-new.+?)"'
            stringFinded = re.findall(pattern, str(tags))#用search的结果难处理，用findall得到list
            dlAddress = 'http://www.cninfo.com.cn/' + stringFinded[0]
            downloadList.append(dlAddress)
            downloadName.append(name)
            print('get download address', index)
            print(dlAddress)
            print(name)
            time.sleep(5)
        except:
            print('fail to get download address', index)
            notOkList.append(url)
            notOkName.append(name)
            time.sleep(10)
            continue
    downloadFile = open('downloadFile.txt', 'r', encoding = 'utf-8')
    previousDL = downloadFile.read()
    downloadFile.close()
    patternUrl = r'downLoadList\n(.+?)\ndownloadName'
    patternName = r'downloadName\n(.+)'
    urlPart = re.findall(patternUrl, previousDL, re.S)[0]
    namePart = re.findall(patternName, previousDL, re.S)[0]
    downloadList.append(urlPart)
    downloadName.append(namePart)
    downloadFile = open('downloadFile.txt', 'w', encoding = 'utf-8')
    downloadFile.write('\ndownloadList\n')
    downloadFile.write('\n'.join(downloadList))
    downloadFile.write('\ndownloadName\n')
    downloadFile.write('\n'.join(downloadName))
    downloadFile.close()
    notLen = len(notOkList)
    notOkFile = open('notOkFile.txt', 'w', encoding = 'utf-8')
    if (notLen > 0):
        notOkFile.write('\nnotOkList\n')
        notOkFile.write('\n'.join(notOkList))
        notOkFile.write('\nnotOkName\n')
        notOkFile.write('\n'.join(notOkName))
    else:
        notOkFile.write('')
    notOkFile.close()
    return notLen
