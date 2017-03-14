#使用parallel获得的down
import urllib.request
import re
import socket
import time
def startDL(docAddress):
    socket.setdefaulttimeout(10)
    currRound = 0
    maxRound = 10
    print(currRound)
    while (currRound < maxRound):
        fhand = open('./downloadFile.txt', 'r', encoding = 'utf-8')
        fContent = fhand.read()
        fhand.close()
        patternUrl = r'downloadList\n(.+?)\ndownloadName'
        patternName = r'downloadName\n(.+)'
        urlList = re.findall(patternUrl, fContent, re.S)
        nameList = re.findall(patternName, fContent, re.S)
        urls = urlList[0].splitlines()
        names = nameList[0].splitlines()


        failUrlList = []
        failNameList = []
        for index in range(len(urls)):
            time.sleep(11)
            url = urls[index]
            saveName = docAddress + names[index]
            try:
                req = urllib.request.Request(url, headers = {
                    'Connection': 'Keep-Alive',
                    'Accept': 'text/html, application/xhtml+xml, */*',
                    'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
                })
                oper = urllib.request.urlopen(req)
                data = oper.read()
                fhand = open(saveName, 'wb')
                fhand.write(data)
                fhand.close()
                print('good', index)
            except:
                print('fail', index)
                # print(url)
                # print(saveName)
                failUrlList.append(url)
                failNameList.append(names[index])#不能保存saveName 不然每次都增加了文件夹地址前缀
                continue



        downloadFile = open('downloadFile.txt', 'w', encoding = 'utf-8')
        downloadFile.write('\ndownloadList\n')
        downloadFile.write('\n'.join(failUrlList))
        downloadFile.write('\ndownloadName\n')
        downloadFile.write('\n'.join(failNameList))
        downloadFile.close()
        if (len(failUrlList) <= 2):
            break
        else:
            time.sleep(301)
        currRound -= 1
