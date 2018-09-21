#Use websit list provide from Bloomberg Company to find out the file download address
#Use failure-tolerent strategy and collect all these fail-analyzed website and analyze again to extract the download address.
import urllib.request
import re
import socket
socket.setdefaulttimeout(10)
currRound = 1
print(currRound)
while (currRound < 10):
    fhand = open('./downloadFile.txt', 'r', encoding = 'utf-8')
    fContent = fhand.read()
    fhand.close()
    patternUrl = r'downloadList\n(.+?)\ndownloadName'
    patternName = r'downloadName\n(.+)'
    urlList = re.findall(patternUrl, fContent, re.S)
    nameList = re.findall(patternName, fContent, re.S)
    urls = urlList[0].splitlines()
    names = nameList[0].splitlines()
    docAddress = './pdfStores/'

    failUrlList = []
    failNameList = []
    for index in range(len(urls)):
        url = urls[index]
        saveName = docAddress + names[index]
        try:
            print('hi', index)
            urllib.request.urlretrieve(url, saveName)
        except:
            print(url)
            print(saveName)
            failUrlList.append(url)
            failNameList.append(names[index])#不能保存saveName 不然每次都增加了文件夹地址前缀
            continue



    downloadFile = open('downloadFile.txt', 'w', encoding = 'utf-8')
    downloadFile.write('\ndownloadList\n')
    downloadFile.write('\n'.join(failUrlList))
    downloadFile.write('\ndownloadName\n')
    downloadFile.write('\n'.join(failNameList))
    downloadFile.close()
    '''这里可以设置一个当failUrlList比较少，自己手动去完成剩下的下载'''
    if (len(failUrlList) <= 2):
        break
    else:
        time.sleep(500)
    currRound -= 1
