from bs4 import BeautifulSoup
fhand = open('merge0_.html', 'r', encoding = 'utf-8')
content = fhand.read()#因为encoding 是utf-8,这里read到的是utf-8编码的字符串
fhand.close()
soup = BeautifulSoup(content, 'html.parser')
prettyHtml = soup.prettify()
fhand = open('prettyMerge0.html', 'w', encoding = 'utf-8')
fhand.write(prettyHtml)
fhand.close()
