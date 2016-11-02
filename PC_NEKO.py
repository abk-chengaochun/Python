import urllib.request
import os
import re
import sys

def url_open(url):
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.65 Safari/537.36')
    response = urllib.request.urlopen(url)
    html = response.read()
    return html

def find_imgs(url):
    html = url_open(url).decode('gbk')
    img_addrs = []
    back = 0
    reg = r'http://tupian.qqjay.com/u/\d\d\d\d/\d\d\d\d/[0-9][0-9]?[0-9]?_[0-9][0-9][0-9][0-9]?[0-9]?[0-9]?[0-9]?_[0-9][0-9]?.jpg'
    for each in re.findall(reg,html):
        url = each
        urllib.parse.quote(url)
        img_addrs.append(url)
    print(img_addrs)
    return img_addrs

def save_imgs(folder, img_addrs):
    for each in img_addrs:
        name = each
        filename = each.split('/')[6]
        print(name)
        with open(filename, 'wb') as f:
            img = url_open(each)
            f.write(img)

            
def download_mm(folder='neko',maolist=2):
    try:
        os.mkdir(folder)
        os.chdir(folder)
    except:
        os.chdir(folder)
    for i in range(1,int(maolist)):
        url = 'http://www.qqjay.com/html/fzl/mao/list_123_'+str(i)+'.html'
        print(url)
        reg = '[0-9][0-9][0-9][0-9]?[0-9]?[0-9]?[0-9]?.html'
        pages = re.findall(reg, url_open(url).decode('gbk'))
        print(pages)
        for page in pages:
            url = "http://www.qqjay.com/html/fzl/mao/"+str(page)
            print(url)
            img_addrs = find_imgs(url)
            save_imgs(folder, img_addrs)

if __name__ == '__main__':
    download_mm()
