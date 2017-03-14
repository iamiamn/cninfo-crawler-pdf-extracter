
from dir.searchingTool import *




def loopSearch(pathName, contentPath, spliter, querys):
    docs = getDict(contentPath, spliter)
    for searchKey in querys:
        parseResults1 = paragraphParser(docs, searchKey, pathName)
        print(searchKey, ":" , len(parseResults1))
        docs = result2strDict(parseResults1)
        # printDict(docs)

    return docs






if __name__ == '__main__':
    pathName = u"merge0"#不知道有什么用，每个add_document多一个标签？？？
    contentPath = 'fixed_0_.txt'
    spliter = r'------------\n'
    querys = [ u"股东大会", u"资产重组"]##在前面的搜索结果中继续搜索下一个词
    docs = loopSearch(pathName, contentPath, spliter, querys)
    printDict(docs)
