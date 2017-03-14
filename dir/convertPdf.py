import sys
import io
# import getopt

from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.pdfdevice import TagExtractor
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import LAParams
# from pdfminer.utils import set_debug_logging



def pdf2html(pdfPath, htmlPath):
    '''按照tool中pdf2txt的方法，写的函数'''
    caching = True
    rsrcmgr = PDFResourceManager(caching=caching)
    scale = 1
    layoutmode = 'noraml'
    laparams = LAParams()
    outdir = None
    debug = False
    outfp = io.open(htmlPath, 'wt', encoding = 'utf-8', errors = 'ignore')
    device = HTMLConverter(rsrcmgr, outfp, scale=scale, layoutmode=layoutmode,
        laparams=laparams, outdir=outdir, debug=debug)
    pagenos = set()
    maxpages = 0
    password = ''
    fp = io.open(pdfPath, 'rb')
    process_pdf(rsrcmgr, device, fp, pagenos, maxpages=maxpages, password=password,
                caching=caching, check_extractable=True)
    fp.close()
    outfp.close()

'''调试用'''
# if __name__ == '__main__':
#     pdfPath = '''merge8_五矿资本控股有限公司_五矿国际信托有限公司_五矿证券有限公司_五矿经易期货有限公司与金瑞科技.pdf'''
#     htmlPath = 'merge8.html'
#     pdf2html(pdfPath, htmlPath)
