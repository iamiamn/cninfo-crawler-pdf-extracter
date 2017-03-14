#设置分句的标志符号；可以根据实际需要进行修改
import os
# import sys


#检查某字符是否分句标志符号的函数；如果是，返回True，否则返回False
def FindToken(cutlist, char):
    if char in cutlist:
        return True
    else:
        return False

#进行分句的核心函数
def Cut(cutlist, string):
              #参数1：引用分句标志符；参数2：被分句的文本，为一行中文字符
    L = []




    return l

#以下为调用上述函数实现从文本文件中读取内容并进行分句。
if __name__ == '__main__':
    lines = open("../tempResult.txt", 'r', encoding = 'utf-8').read().split('\n------------\n')
    cutlist = u"[。！？]"
    l = Cut(list(cutlist),lines)
    for line in lines:
       print('--', line)
