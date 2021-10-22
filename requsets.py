#爬虫爬取网页
#获取页面信息
#输入网页（地址定位符）：url
#处理：request库函数获取页面信息，并将网页内容转换成为人能看懂的编码格式
#输出：爬取到的内容。




# coding = utf-8
# import requests  #导入requests数据库
# from bs4 import BeautifulSoup

# url = 'https://www.xbiquge.la/?hpprotid=2a8031d1'
# strHtml = requests.get(url)  #Get方式获取网页数据
# html = strHtml.text
# bf = BeautifulSoup(html,"html.parser")
# texts = bf.find_all('div',class_='showtxt')
# print(texts[0].text.replace('\xa0'*8,'\n\n'))



#爬取网页的通用代码框架：
import requests
from bs4 import BeautifulSoup
import re

def getHTMLText(url):
    try:
        r = requests.get(url,timeout=30)
        r.raise_for_status()    #如果状态码不是200，产生异常(status_code  :HTTP请求的返回状态，200表示连接成功，404表示失败)
        r.encoding = 'utf-8'    #字符编码格式改成 utf-8
        return r.text
    except:
        #异常处理
        return 'error'

def findHTMLText(text):
    soup = BeautifulSoup(text,'html.parser')     #返回BeautifulSoup对象
    return soup.find_all(string=re.compile('百度'))#结合正则表达式，实现字符串片段匹配（相当于关键字提取）


url = 'http://www.baidu.com'
# print(getHTMLText(url))
text = getHTMLText(url)       #获取html文本内容
res = findHTMLText(text)      #匹配结果

print(res)                    #打印输出