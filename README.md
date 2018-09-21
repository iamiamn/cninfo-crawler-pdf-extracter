# cninfo-crawler-pdf-extracter

1. this is a crawler for pdf about information of securities from cninfo.com.cn. In this project
2. I first crawl pdf document from cninfo.com.cn.
3. Secondly, I use pdfminer3k package to transform pdf into html and separate paragraphs and tables. 
4. Finally I use whoosh+jieba to build up a chinese text search engine.


## Details:
PROJECT_EXPLANATION_CHN.docx  : Contest definition

useDownloadList.py            : Use PROJECT_EXPLANATION_CHN.docx to extract download List

researchControl.py            : Main function for extracting infromation from document

searchControl.py              : Main function for extracting infromation from document

dir                           : Tool Function Repositary 

fixedTrainingTxt;pdfStores;txtAndXls  : Data storage

