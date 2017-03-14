from dir.searchingTool import *
# from dir.reSearchControl import *

if __name__ == '__main__':
    textStoreDir = 'txtAndXls/'
    saveDir = 'fixedTrainingTxt/'
    if not os.path.exists(saveDir):
        os.mkdir(saveDir)
    fixAllText(textStoreDir, saveDir)
