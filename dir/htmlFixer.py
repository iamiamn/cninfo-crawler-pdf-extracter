# -*- coding: utf-8 -*-

'''用BeautifulSoup 处理每个pdf转换成的html文件，提取excel文件'''
import re
from bs4 import BeautifulSoup
import io
import sys
import xlwt
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')
# def printDict(dict,keyList, spliter):
#     '''用来打印字典'''
#     for key in keyList:
#         print(key, ' :', dict[key][5], spliter)

def saveDict(dict, keyList, spliter, path):
    '''传入的keyList是排好序的'''
    content = [dict[key][5] for key in keyList]
    fhand = open(path, 'w', encoding = 'utf-8')
    fhand.write(spliter.join(content))
    fhand.close()

def getSoup(filePath):
    '''传入html文件的地址，用BS读取出soup数据'''
    fhand = open(filePath, 'r', encoding = 'utf-8')
    htmlContent = fhand.read()
    fhand.close()
    soup = BeautifulSoup(htmlContent, 'html.parser')
    return soup

def prettyPrintHtml(soup, savePath):
    '''把html内容排列整齐后输出到文件'''
    prettyHtml  =soup.prettify()
    # print(type(prettyHtml))
    fwrite = open(savePath, 'w', encoding = 'utf-8')
    fwrite.write(prettyHtml)
    fwrite.close()

#利用正则匹配标签值找到特定内容
# patternStyle = re.compile(r'.+top:.+;')
# results = soup.find('div', attrs = {'style':patternStyle
def getDict(soup):
    '''由soup中匹配得到文本以及换页码所构成的dict'''
    tagDict = {}
    patternPageNum = re.compile(r'.+top:.+;')
    results = soup.findAll('div', attrs = {'style':patternPageNum})#find可以找到
    for result in results:
        numRs = re.findall(r'(\d+)px', str(result))
        textFound = result.get_text()
        if (len(numRs) == 1):
            key = int(numRs[0])
            #left,top,width,height,fone
            value =  [0,int(numRs[0]), 100,10,10]
        else:
            key = int(numRs[2])
            value = [int(x) for x in numRs[1:6]]
        value.append(textFound)
        if (key in tagDict.keys()):#说明top一样的情况，这时候就把list结合，用加法不能用append
            tagDict[key] += value#如果存在就在后面补充
        else:
            tagDict[key] = value
    return tagDict


def joinText(dict):
    '''按照top排序后，如果当前键值对的height+top包含了下一个top，则认为这两个属于同一行内容，属于table'''
    # print('rawDictNum:', len(dict))
    #按照key排序,keys()获得的是dict_key类，比如用下面的或者[i for i in dict.keys()]
    keyList = sorted(list(dict.keys()))
    numTotalKey = len(keyList)
    counter = 0
    currValue = dict[keyList[counter]]
    currTop = keyList[counter]# top就是key
    currHeight = currValue[3]
    while (counter < numTotalKey - 1):
        nextTop = keyList[counter + 1]
        nextValue = dict[nextTop]

        extendedTop = currTop+ currHeight
        if (extendedTop >= nextTop ):
            #说明属于同一行的内容，属于表格类, 应该+不能append
            dict[currTop] += nextValue
            del(dict[nextTop])
        else:
            currTop = nextTop
            currValue = nextValue
            currHeight = currValue[3]
        counter += 1

    tableKeyList = []#记录可能是table的key
    for item in dict.items():
        if (len(item[1]) > 6):
            tableKeyList.append(item[0])
    tableKeyList = list(set(tableKeyList))
    dict['table'] = tableKeyList
    return dict
    #按key排序，返回的是列表，每个元素是2元tuple，key和value
    # tagSortedList = sorted(tagDict.items(), key = lambda d:d[0])

def fixText(dict, spliter, path):
    '''把有多列内容的行，按照表格的形式写到excel中去'''
    wbk = xlwt.Workbook(encoding = 'utf-8', style_compression = 0)
    sheet = wbk.add_sheet('sheet1', cell_overwrite_ok = True)
    tableKeyList = sorted(dict['table'])
    currRow = 0
    for key in tableKeyList:
        value = dict[key]
        # print(value)#!!!!
        left = value[0]
        top = value[1]
        width = value[2]
        height = value[3]
        font = value[4]
        string = value[5]
        counter = 6
        tempDict={}
        tempDict[left] = string
        while (counter < len(value)):
            currValue = value[counter:counter + 6]
            # print(value)#!!!!
            currLeft = currValue[0]
            currString = currValue[5]
            tempDict[currLeft] = currString
            counter += 6
        sortedList = sorted(tempDict.items(), key = lambda d:d[0])
        finalString = spliter.join([i[1] for i in sortedList])
        #其实这里可以对finalString进行美化
        sheet.write(currRow, 0, str(top))
        counter = 1
        for subString in sortedList:
            sheet.write(currRow, counter, subString[1])
            counter += 1
        currRow += 1
        assembleValue = [left, top, width, height, font, finalString]
        # print(assembleValue)
        dict[key] = assembleValue
    wbk.save(path)    ##该文件名必须存在
    return dict

def joinParagraph(dict, tableKeySet):
    '''key为top, value 为列表：left,top,width,height,fone，string
    传入的dict的key全部为整数'''
    allKeySet = set(dict.keys())
    notTableKeyList = sorted(list(allKeySet - tableKeySet))
    numKey = len(notTableKeyList)
    counter = 0
    currTop = notTableKeyList[counter]
    currFont = dict[currTop][4]
    while (counter < numKey - 1):
        nextTop = notTableKeyList[counter + 1]
        nextFont = dict[nextTop][4]
        nextString = dict[nextTop][5]
        if (nextFont == currFont):
            dict[currTop][5] += nextString
            del(dict[nextTop])
        else:
            currFont = nextFont
            currTop = nextTop
        counter += 1
    return dict

def dealHtml(htmlPath, saveTextPath, excelSavePath, passageSpiter = '------------\n'):
    '''把html分解为table和正常的text部分'''

    soup = getSoup(htmlPath)
    tagDict = getDict(soup)
    joinedDict = joinText(tagDict)
    print('joinedDict:',len(joinedDict))
    tableKeyList = joinedDict['table']#这些是有列表的
    fixedTextDict = fixText(joinedDict, '---/---\n', excelSavePath)
    tableKeySet = set(fixedTextDict['table'])
    del(fixedTextDict['table'])#不删除会排序错误
    resultDict = joinParagraph(fixedTextDict, tableKeySet)
    allKeySet = set(resultDict.keys())
    notTableKeyList = sorted(list(allKeySet - tableKeySet))
    saveDict(resultDict, notTableKeyList, passageSpiter, saveTextPath)



'''下面是调试用'''
# if __name__ == '__main__':
#     htmlPath = './merge2.html'
#     saveTextPath = './merge2saveFile.txt'
#     excelSavePath = './merge2Table.xls'
#     passageSpliter = '------------------\n'
#     soup = getSoup(htmlPath)
#     tagDict = getDict(soup)
#     joinedDict = joinText(tagDict)
#     print('joinedDict:',len(joinedDict))
#     tableKeyList = joinedDict['table']#这些是有列表的
#     fixedTextDict = fixText(joinedDict, '---/---\n', excelSavePath)
#     tableKeySet = set(fixedTextDict['table'])
#     del(fixedTextDict['table'])#不删除会排序错误
#     resultDict = joinParagraph(fixedTextDict, tableKeySet)
#     allKeySet = set(resultDict.keys())
#     notTableKeyList = sorted(list(allKeySet - tableKeySet))
#     saveDict(resultDict, notTableKeyList, '\n-------------\n', saveTextPath)
