#!/usr/bin/python
# coding = utf-8
from bs4 import BeautifulSoup
import requests
import os
import re
os.makedirs('./image/',exist_ok=True)
ADDRESS = ""
ADDRESSBF = ""
NUM = 0
NO = 0
PAGE = 1
def getImage (ADDRESS,NUM,PAGE,NO):
    headers = {
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    }
    num = 0
    r = requests.get(ADDRESS,headers=headers)
    # print(r)
    soup = BeautifulSoup(r.text,'html5lib') #一个好的解析器能让你少走弯路
    # print(soup)
    section = soup.find_all('img',attrs={"data-width":'750'}) #机制有待改进默认750 640
    # print(section)
    if (str(PAGE) <= str(NUM)):
        print("正在下载第"+str(PAGE)+"页......")
        for j in section:
            print(j['src'])
            with open('./image/img'+str(NO)+'.jpg','wb+') as f:
                r = requests.get(j['src'])
                f.write(r.content)
                NO = NO + 1
                f.close()
        bnum_a = re.findall(r"\d", ADDRESSBF)
        bnum_a = [str(i) for i in bnum_a]
        bnum_b = int(''.join(bnum_a))
        print(ADDRESSBF)
        getImage("http://www.gllmh.com/jqsz/"+str(bnum_b)+"_"+str(PAGE+1)+".html",NUM,PAGE+1,NO)
    else:
        print("下载完成！")
        print("保存位置："+os.path.abspath('./image'))

def getPageNum(ADDRESS):
    ldata = []
    headers = {
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    }
    r = requests.get(ADDRESS, headers=headers)
    # print(r)
    soup = BeautifulSoup(r.text,'html5lib')
    res = soup.find("div",attrs={"class":"pagination"})
    print("获取漫画总页数，请稍后......")
   # print(res)
    for child in res.children:
        # print(child)
        ldata.append(child)
    num = re.findall(r"\d", str(ldata[1]))[0]
    print("本部漫画共获取到"+num+"页") #打印页数
    global NUM #声明全局变量在此处要修改全局变量NUM
    NUM = num

if __name__ == '__main__':
    print("请输入整本漫画的初始地址(不要有多余空格，粘贴网址后务必将光标移动至“请”字前面否则会打开浏览器且无法继续执行程序”)：",end="")
    address = input()
    ADDRESS = address
    ADDRESSBF = address
    getPageNum(ADDRESS)
    getImage(ADDRESS,NUM,PAGE,NO)

#测试地址 http://www.gllmh.com/jqsz/6890.html 宽度750
# http://www.gllmh.com/jqsz/801.html 宽度750
# http://www.gllmh.com/jqsz/1082_2.html 宽度640
