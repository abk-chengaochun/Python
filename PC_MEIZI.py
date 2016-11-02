import urllib.request
import os
import re
from urllib.error import URLError, HTTPError
import random
import time
def get_daili():
    url_daili = 'http://api.xicidaili.com/free2016.txt'
    req = urllib.request.Request(url_daili)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.65 Safari/537.36')
    
    response = urllib.request.urlopen(url_daili)
    html = response.read().decode('ascii') 
    
    try:
        ip = html.split()[random.randint(1,50)]
        return ip
    except:
        print('换线')


def url_open(url):                                #通用设置，将爬虫伪装为浏览器访问,并调用外部IP地址   
    #ip = get_daili()
    
    #proxy_support = urllib.request.ProxyHandler({'http': ip})
    #opener = urllib.request.build_opener(proxy_support)
    #opener.addheaders=[('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.65 Safari/537.36')]
    #urllib.request.install_opener(opener)   
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.65 Safari/537.36')
    response = urllib.request.urlopen(url)
    html = response.read()
    
    return html

def get_totalpages(url):                          #通过版块地址获得该版块所有页数（每页有50个系列），返回值为数字
    html = url_open(url).decode('gbk')
    reg = r'共 <strong>(.*?)</strong>页'
    totalpages = re.findall(reg,html)[0]
    
    return int(totalpages)

def get_sercoverurl(pageurl):                    #通过页面地址获得该页面下所有系列的封面地址，返回值为列表
    html = url_open(pageurl).decode('gbk')
    reg = r'<p><a href="(.*?)"'
    sercoverurl = re.findall(reg, html)
    
    return sercoverurl                          #各个系列的封面 列表

def get_serurl(sercoverurl):                  #通过封面获得该系列的所有图片所在的页面地址 (每个页面有一张图片，其地址待下一步获取)
    html = url_open(sercoverurl).decode('gbk')   #
    reg1 = r'<li><a>共(.*?)页'
    totalsheets = int(re.findall(reg1, html)[0])  # 获得该系列图片总张数
    serurls = []
    serurls.append(sercoverurl)
    for eachsheet in range(2,totalsheets+1):
        serurl = sercoverurl[:-5] + '_' + str(eachsheet) + sercoverurl[-5:]
        serurls.append(serurl)
    return serurls

def get_picurl(serurl):
    html = url_open(serurl).decode('gbk')
    reg = r"<img src='(.*?)'"
    picurl = re.findall(reg,html)[0]

    return picurl     #只有一个地址，即封面地址

def get_subname(serurl):
    html = url_open(serurl).decode('gbk')
    reg = r'title="(.*?)"'
    name = re.findall(reg,html)[0][2:]
    
    return name     #各个系列的封面名称

def set_folder(ori_folder): #设置当前目录
    try:
        os.mkdir(ori_folder)
        os.chdir(ori_folder)
    except:
        os.chdir(ori_folder)

def download_cl(folder = '爬虫youmzi改'):             #主程序
    
    set_folder(folder)
    url = 'http://www.youmzi.com/meinv.html'
    totalpages = get_totalpages(url)
    
    for eachpage in range(1,totalpages+1):
        pageurl = url[:-5] + '_'+ str(eachpage) + url[-5:]
        sercoverurl = get_sercoverurl(pageurl)       #获得系列的封面地址 列表
        print('第%s页共有%s个系列。'%(str(eachpage),len(sercoverurl)))

        for eachsercover in sercoverurl:
            try:
                sub_start = time.clock()
                sub_name = get_subname(eachsercover)
                set_folder(sub_name)
                serurl = get_serurl(eachsercover)    #返回系列的所有地址 列表
                print('%s内有%s张图片。'%(sub_name,len(serurl)))
                counter = 1
                for oneser in serurl:
                    print('正在下载第%d张图片...' % (counter))
                    picurl = get_picurl(oneser)
                    filename = picurl.split('/')[-1]
                    urllib.request.urlretrieve(picurl, filename)
                    counter += 1
                    
                return_folder = os.path.abspath(os.path.join(os.path.dirname("__file__"),os.path.pardir))#返回上一级目录
                set_folder(return_folder)
                sub_end = time.clock()
                print("该系列下载花费: %.01f 秒" %(sub_end-sub_start))
            except HTTPError as e:
                print('HTTPError:',e.reason)
                return_folder1 = os.path.abspath(os.path.join(os.path.dirname("__file__"),os.path.pardir))
                set_folder(return_folder1)
                continue
            time.sleep(1)
    
if __name__ == '__main__':
    download_cl()
