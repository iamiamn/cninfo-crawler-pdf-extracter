from dir.searchingTool import *
import re,os
import jieba
import jieba.analyse
import jieba.posseg
# test = {"1":"2、2016年5月20日，顺丰控股股东大会通过决议，批准本次重大资产重组的\n"}
# string = test["1"]
#
# searchKey = u"股东大会"
# pathName = u"a"
# parseResults1 = paragraphParser(test, searchKey, pathName)
# print(result2strDict(parseResults1))
# print(parseResults1)
#
# reResult = re.search(r'股东大会', string)
# print(reResult)


def parallelRe(docs, docTitle, spliter, query):
    '''利用map函数并发（并行）docs，docs是中文自然段组成的列表,其实就是一个字符串列表'''
    results = list(map(reSearch(query), docs))
    resultDict = {}
    for index in range(len(results)):
        if (results[index]):
            resultDict[docTitle[index]] = docs[index]

    # print(resultDict)
    # getSentence(resultsDict)
    return resultDict

    # resultDict = {}
    # for
def loopReSearch(docs, docTitle, querys, printOption = 0):
    '''按querys中关键词的顺序，迭代筛选出含有关键词的字符串段,并且统计包含该关键词的自然段个数'''
    # docs = getList(contentPath, spliter)
    # docTitle = list(range(len(docs)))
    for query in querys:
        resultDict = parallelRe(docs, docTitle, spliter, query)
        docs = []
        docTitle = []
        for (t, s) in resultDict.items():
            docs.append(s)
            docTitle.append(t)
        # printDict(resultDict)
        print(query, ":", len(docs))
    if printOption:  printDict(resultDict)

    return resultDict




def reSearch(pattern):
    '''re.search找到则返回1否返回0'''
    def f(doc):
        if (re.search(pattern, doc, re.S)):
            # print(doc)
            return 1
        else:
            return 0
    return f



def walkAll(spliter, querys, storDir):
    '''对于每个在storeDir中的文件，进行搜索匹配：返回的是由字典组成的列表，每个字典都是一个文件的搜索结果'''
    dirInfo = next(os.walk(storeDir))
    root = dirInfo[0]
    files = dirInfo[2]
    results = []
    for file in files:
        splitName = os.path.splitext(file)
        if splitName[1] == '.txt':
            contentPath = os.path.join(root, file)
            docs = getList(contentPath, spliter)
            docTitle = list(range(len(docs)))
            resultDict = loopReSearch(docs, docTitle, querys)
            rearrangedDict = rearrangeStr(resultDict)

            docs = []
            docTitle = []
            for (t, s) in rearrangedDict.items():
                docs.append(s)
                docTitle.append(t)
            resultDict = loopReSearch(docs, docTitle, querys)

            #进行分句后再loop一次

        results.append(resultDict)
    return results

def jiebaFindKey(dict, pOption = 1):
    # dict = rearrangeStr(dict)
    topNum = 30
    resultDict = {}
    for (index, string) in dict.items():
        tags = jieba.analyse.extract_tags(string, topNum)
        if (pOption == 1): print(index, '\n', string, '\n关键词\n', tags)
        resultDict[index] = tags
    return resultDict

def jiebaTag(dict, pOption = 1):
    resultDict = {}
    for (index, string) in dict.items():
        words = jieba.posseg.cut(string)
        tags = []
        for i in words:
            tags.append((i.word, i.flag))
        resultDict[index] = tags
    if (pOption == 1): printDict(resultDict)

    return resultDict



def rearrangeStr(dictIn):
    '''把分号的句子重新分割,1:1, 1:2,'''
    printOption = 0
    if printOption:
        print('before rearrange:')
        printDict(dictIn)
    spliter = r'；|：|:|;'
    newDict = {}
    for (index, string) in dictIn.items():
        matchResult = re.search(r':|：', string)
        # print(matchResult)
        if (matchResult):
            subSent = re.split(spliter, string + '；')
            # print(len(subSent))
            # print(subSent)
            lenSS = len(subSent)
            for sentIndex in range(1, lenSS):
                newDict[index + sentIndex/100] = subSent[0] + subSent[sentIndex]
        else:
            newDict[index] = string
    if printOption:
        print('after rearrange:')
        printDict(dictIn)
    return newDict


if __name__ == '__main__':
    # contentPath = 'Merge0_.txt'
    spliter = re.compile(r'------------\n|。')
    # querys = [ u'股东大会', u'资产重组', r'[\d\s]+年[\d\s]+月[\d\s]+日']
    # querys = [ u'董事会', u'资产重组', r'[\d\s]+年[\d\s]+月[\d\s]+日']
    # querys = [ u'证监会', u'资产重组']
    querys = [u"交易对方", u"明德控股", u"交易日", u"锁定期"]#检测分号分割情况
    # querys = [u'收购']


    # querys = [u'中国证监会']
    '''选择一个txt文件放在storeDir,就可以观察搜索结果，'''
    storeDir = 'fixedTrainingTxt/'
    results = walkAll(spliter, querys, storeDir)

    '''对最后的搜索结果，进行jieba分词和提取关键词'''
    for result in results:
        jiebaFindKey(result, 0)#0代表不输出结果，1代表输出结果
        jiebaTag(result, 1)





    # 修复所有的text
    # textStoreDir = 'txtAndXls/'
    # saveDir = 'fixedTrainingTxt/'
    # if not os.path.exists(saveDir):
    #     os.mkdir(saveDir)
    # fixAllText(textStoreDir, saveDir)
