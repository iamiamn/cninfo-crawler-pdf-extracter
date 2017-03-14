# coding=utf-8
import os
from whoosh.index import create_in
from whoosh.fields import *
# from jieba.analyse import ChineseAnalyzer
import jieba
import jieba.analyse
# import json
import re
# from dir.pruneText import *#即使跟prunText在同一文件夹，仍然需要通过dir package去调用另一个py文件的全部函数

def fixAllText(dirName, saveName):
    dirInfo = next(os.walk(dirName))
    root = dirInfo[0]
    files = dirInfo[2]
    # print(root, '--', files[0])
    for file in files:
        splitName = os.path.splitext(file)
        if splitName[1] == '.txt':
            fixText(os.path.join(root, file), saveName)

def staAnalysis(ansList):
    '''传入字符串的list, 统计选中字符串r长度的分布'''
    stringLens = [len(x) for x in ansList]
    box = {}
    for i in stringLens:
        box[i] = box.get(i, 0) + 1
    threshold = 34
    selectedStrs = [x for x in ansList if (len(x) < threshold)]
    # for x in selectedStrs:
    #     print(x)
    for (k, v) in box.items():
        print(k, ": ", v)

def seperateTitle(string):
    '''   采用了 spliter = r------------\n(.*[\d,]{1,10}.*\n)|(\n.*[\d,]{1,10}.*)\n------------ 后必须
    分割数字型的标题，主要是不要让整一段太长, 但是也怕分割了一些小句子。选择10个字符比较合适'''

    spliter =r'\n([\d]{1,2}、.{1,10})\n'
    def func(m):
        return '\n------------\n'+ m.group(1) + '\n------------\n'
    p = re.compile(spliter)
    ans = p.sub(func, string)
    return ans

def getTitle(content):
    allLines = re.split(r'\n', content)
    counter = 1
    result = []
    spliter = '\n------------'
    if (len(allLines) <5):
        print(allLines)
    thisLine = allLines[counter]
    if (re.search(r'代码', thisLine)):
        result.append('股票代码行-----' + thisLine + spliter)
        counter += 1

    while (True):
        thisLine = allLines[counter]
        counter += 1
        if (thisLine == '------------'):
            continue
        elif (re.search(r'草案|预案',thisLine)):
            result.append('标题行-----' + thisLine + spliter)
            break
        elif (re.search(r'公司|资产|股份', thisLine)):
            result.append('标题行-----' + thisLine)
            continue
        else:
            break
    string = '\n'.join(result+allLines[counter::])
    return string






def cutPage(content):
    '''匹配删除所有的页码1-d 和page d型，翻页融合'''
    content = getTitle(content)
    spliter = r'''Page\s[\d]+------------\n.+?\n------------[\n]+|
    Page\s[\d]+------------\n|1-[\d]+\n------------\n|Page\s[\d]+------------\n.+?\n'''
    results = re.split(spliter, content)
    joinedResult = ''.join(results)
    return fixPage(joinedResult)

def fixPage(joinedContent):
    '''进一步融合自然段，防止出现分隔符隔断语义，可以容忍分段数的下降
        一般都是因为某一行具有'''
    # spliter = r'''([\d]+\n)------------\n|------------\n([\d,]{2,4})|(\n[\d,]{2,4}.+\n)------------\n'''
    # spliter = r'''([^。]\n)------------\n(.*[\d,]{1,4}[\s\u4e00-\u9fa5]*[年月日元股].*\n)|(.*[\d,]{1,4}[\s\u4e00-\u9fa5]*[年月日元股].*\n)------------\n'''
    spliter = r'''------------\n(.*[\d,]{1,10}.*\n)|(\n.*[\d,]{1,10}.*)\n------------'''
    results = re.split(spliter, joinedContent)
    #这里居然会返回none type.只能取出了
    ansList = [x for x in results if (x is not None and len(x) > 0)]
    # staAnalysis(ansList)
    while (len(ansList) > 1):
        # print(len(ansList))
        results = re.split(spliter, ''.join(ansList))
        #这里居然会返回none type.只能取出了
        ansList = [x for x in results if x is not None]
    # ans = ''.join(ansList)
    ans = ansList[0]
    ans = seperateTitle(ans)


    return ans

def write2store(strings, fileName):
    fhand = open(fileName, 'w', encoding = 'utf-8')
    if (len(strings) == 1):
        fhand.write(strings)
    else:
        fhand.write(''.join(strings))
    fhand.close()


def getList(fileName, spliter):
    '''通过访问文件进行句子分隔'''
    # print(prunedContent)
    fhand = open(fileName, 'r', encoding='utf-8')
    pContent = fhand.read()
    fhand.close()
    # addedSpliter = spliter + r'|。'
    strings = re.split(spliter, pContent)
    #不删除page页码
    # strings = re.split(spliter, pContent)

    return strings

def fixText(fileName, preName):
    '''传入文件名，去除文件的page标签'''
    fhand = open(fileName, 'r', encoding='utf-8')
    pContent = fhand.read()
    fhand.close()

    #txt文档删除page页码
    prunedContent = cutPage(pContent)
    num = re.findall(r'merge([\d_]+.txt)', fileName)[0]
    write2store(prunedContent, preName+'fixed_'+num)


def getDict(fileName, spliter):
    # print(strings)
    strings = getList(fileName, spliter)
    docs = {}
    numStrings = len(strings)
    print("totalParagraph: ", numStrings)
    for i in range(numStrings):
        docs[str(i)] = strings[i]#必须转为str,不然add_document的title需要string
    return docs


def result2strDict(results):
    strDict = {}
    for result in results:
        strDict[result["title"]] = result["content"]
    return strDict
# def segParagraph(content, spliter):
    # '''spliterOption = 1按段分割，2为按页分割'''
    # if (spliterOption ==1 ):
    #     spliter = r'------------\n'# 因为有如下的情况
    #     # Page 12------------
    #     # 马鞍山鼎泰稀土新材料股份有限公司重大资产置换及发行股份购买资产并募集配套资金暨关联交易预案
    #     # ------------
    # else:#
    #     spliter = r'Page\s[\d]+'
    # # return content.split(content, spliter)#split不能用re
    # return re.split(spliter, content)

#导入自定义词典
# jieba.load_userdict(u"customDict.txt")#x显示ValueError: dictionary file customDict.txt must be utf-8
def paragraphParser(docs, searchKey, pathName, customDictOrNot = 1):

    # if (customDictOrNot == 1):
    #     fhand = open("customDict.txt", 'w', encoding = 'utf-8')
    #     fhand.write(searchKey)
    #     fhand.close()
    #     jieba.load_userdict("customDict.txt")#必须通过python进行utf-8编码写入才能成功
    jieba.load_userdict("customDict.txt")#必须通过python进行utf-8编码写入才能成功

    # 使用结巴中文分词
    analyzer = jieba.analyse.ChineseAnalyzer()

    # 创建schema, stored为True表示能够被检索
    schema = Schema(title=TEXT(stored=True, analyzer=analyzer), path=ID(stored=False),
                    content=TEXT(stored=True, analyzer=analyzer))

    # 存储schema信息至'indexdir'目录下
    indexdir = 'indexdir/'
    if not os.path.exists(indexdir):
        os.mkdir(indexdir)
    ix = create_in(indexdir, schema)


    # docs = segParagraph(prunedContent, spliter)#默认为1：按段分割

    writer = ix.writer()
    for (dIndex, dContent) in docs.items():
        # 按照schema定义信息，增加需要建立索引的文档
        # 注意：字符串格式需要为unicode格式
        writer.add_document(title=dIndex, path=pathName, content=dContent)
    writer.commit()
    # 创建一个检索器
    searcher = ix.searcher()
    results = searcher.find("content", searchKey)#属于自定义词，直接找不到的，必须添加自定义词典
    return results
    # printSearch(results)

def printSearch(results, option = 1):
    print("following is search result:")
    '''option == 1按照search返回的字典的结果输出，2代表是正常的list'''
    if (option == 1):
        #http://whoosh.readthedocs.io/en/latest/releases/1_0.html?highlight=print
        # 检索出来的第一个结果，数据格式为dict{'title':.., 'content':...}
        for hit in results:
            print(hit["title"], ':')
            # test = hit.highlights("content")
            # print(test)
            print(hit["content"])
            # print(type(test))#属于str类
    elif (option == 2):
        for result in results:
            print(result)
def printDict(docs):
    for (k,v) in docs.items():
        print(k,'\n', v)
