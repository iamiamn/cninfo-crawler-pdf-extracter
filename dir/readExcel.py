import xlrd
import re

def getExcelCols(fileName, startCol, stopCol):
    '''利用文件名获得关于整个一个列的数据,空数据应该返回"",如果是/分割数据应该'''
    data = xlrd.open_workbook(fileName)
    sheet = data.sheets()[0]
    nRow = sheet.nrows
    nCol = sheet.ncols
    startRow = 3
    result = []
    for colIndex in range(startCol, stopCol + 1):
        col_data = sheet.col_values(colIndex)
        colDict = {}
        # print(col_data)
        for i in range(startRow, len(col_data)):
            content = col_data[i]

            colDict[i - startRow] = fixContent(content)
        result.append(colDict)
    return result

def fixContent(content):
    spliter = re.compile(r'/|、|；')
    if (re.search(spliter, content)):
        result = re.split(spliter, content)
    else:
        result = [content]
    return result
