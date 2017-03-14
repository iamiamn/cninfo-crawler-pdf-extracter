#处理excel。获得pdf自动下载地址
import xlrd
import re
import socket
from bs4 import BeautifulSoup
import urllib.request
data = xlrd.open_workbook('./Training Data.xlsm')
sheet = data.sheets()[0]
saveFile = open('./downloadFile.txt', 'w', encoding = 'utf-8')
col2 = sheet.col_values(1)
urlList = col2[3:len(col2)]
saveFile.write('allUrl:\n')
saveFile.write('\n'.join(urlList))
#记录所有在excel中取得的数据
pageList = []
pageName = []
#记录获得的pdf下载地址，用于自动下载
downloadName = []
downloadList = []
#记录pdf下载失败的地址，手动下载
notOkList = []
notOkName = []
totalNumUrl = len(urlList)

for index in range(totalNumUrl):
    url = urlList[index]
    saveName = 'merge' + str(index) + ':' + sheet.cell_value(index + 2,2) + '与' + sheet.cell_value(index + 2, 3) + '.pdf'
    pattern1 = r'(http.+?PDF)'
    finded = re.findall(pattern1, url)
    if (finded):
        downloadList.append(url)
        downloadName.append(saveName)
    else:
        pageList.append(url)
        pageName.append(saveName)
socket.setdefaulttimeout(10)#设置超时时间
numPageList = len(pageList)
for index in range(numPageList):
    url = pageList[index]
    print(index, url)
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
    except TimeO:
        notOkList.append(url)
        notOkName.append(name)
        continue


saveFile.write('\ndownloadList\n')
saveFile.write('\n'.join(downloadList))
saveFile.write('\ndownloadName\n')
saveFile.write('\n'.join(downloadName))
saveFile.write('\nnotOkList\n')
saveFile.write('\n'.join(notOkList))
saveFile.write('\nnotOkName\n')
saveFile.write('\n'.join(notOkName))


saveFile.close()
