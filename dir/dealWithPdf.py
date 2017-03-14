# -*- conding:utf-8 -*-
from dir.htmlFixer import dealHtml
from dir.convertPdf import pdf2html
import os
import re
def file_name(file_dir):
    '''返回的字典，key为字符串形式的序号，value为文件地址'''
    d = {}
    L2 = []
    info = next(os.walk(file_dir))
    # print(info)
    root = info[0]
    files = info[2]
    # print(files)
    # print(root)
    # print(os.walk(file_dir).files)
    patternIndex = r'merge([\d_]+)'
    for file in files:
        splitName = os.path.splitext(file)
        print(splitName)
        suffix = splitName[1]
        if ((suffix == '.pdf') or (suffix == '.PDF')):
            key = re.findall(patternIndex, splitName[0])[0]
            # print(key)
            d[key] = (os.path.join(root, file))
    return d



# htmlPath = 'merge8.html'
# saveTextPath = 'merge8.txt'
# saveTablePath = 'merge8.xls'
# dealHtml(htmlPath, saveTextPath, saveTablePath)

if __name__ == '__main__':
    fileDict = file_name('./pdfStores1/')
    print(fileDict)
    prefix = './pdfStores1/merge'
    counter = 0
    exceptionList = []
    # for (k, v) in fileDict.items():
    #     print(k)
    for (index, pdfPath) in fileDict.items():
        print(counter)
        counter += 1
        htmlPath = prefix + index + '.html'
        saveTextPath = prefix + index + '.txt'
        saveTablePath = prefix + index + '.xls'
        try:
            pdf2html(pdfPath, htmlPath)
            dealHtml(htmlPath, saveTextPath, saveTablePath)
        except:
            exceptionList.append(pdfPath)
            continue
    fhand = open('./exceptionList.txt', 'w', encoding = 'utf-8')
    fhand.write('\n'.join(exceptionList))
    fhand.close()
