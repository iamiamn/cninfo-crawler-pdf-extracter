from dir.readExcel import *
from dir.searchingTool import *
import io,sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding = 'gb18030')






def Match23(fileName):
    cols = getExcelCols(fileName=, 2,3)
    mubiaoCol = cols[0]
    shougouCol = cols[1]



if __name__ == "__main__":
    trainFile = "fixed_Training_Data.xlsm"
    cols = getExcelCols(trainFile, 2,3)
    mubiaoCol = cols[0]
    shougouCol = cols[1]
    # print(cols)
    printDict(mubiaoCol)
    printDict(shougouCol)
    # for i in range(len(mubiaoCol)):
        # print(mubiaoCol[i])
    # print(fixContent('广东合利金融科技服务有限公司/深圳前海传奇互联'))
    # text = "1、杭州好望角禹航投资合伙企业（有限合伙）；2、北京祺创投资管理中心（有限合伙）；3、张桔洲；4、吴瑞敏；5、朱春良；6、李薇；7、萍乡亚海资产管理合伙企业（有限合伙）；8、张耀东；9、北京易车信息科技有限公司；10、苟剑飞；11、汤雪梅；12、张彬；13、北京一百动力科技中心（有限合伙）；14、于辉；15、杭州好望角引航投资合伙企业（有限合伙）"
    print(fixContent(text))
