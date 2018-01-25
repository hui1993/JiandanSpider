import hashlib   
import base64
from bs4 import BeautifulSoup
import requests
import re
import random
import shutil
import os
import time
def parse (imgHash, constant): 
    q = 4
    hashlib.md5()   
    constant = md5(constant)
    o = md5(constant[0:16])
    n = md5(constant[16:32])    
    l = imgHash[0:q]
    c = o + md5(o + l)
    imgHash = imgHash[q:]
    k = decode_base64(imgHash)
    h =list(range(256))

    b = list(range(256))

    for g in range(0,256):
        b[g] = ord(c[g % len(c)])

    f=0
    for g in range(0,256):
        f = (f+h[g]+b[g]) % 256
        tmp = h[g]
        h[g] = h[f]
        h[f] = tmp
        
    result = ""
    p=0
    f=0
    for g in range(0,len(k)):   
        p = (p + 1) % 256;
        f = (f + h[p]) % 256
        tmp = h[p]
        h[p] = h[f]
        h[f] = tmp
        result += chr(k[g] ^ (h[(h[p] + h[f]) % 256]))
    result = result[26:]
    
    return result

def md5(src):
    m = hashlib.md5()   
    m.update(src.encode("utf8"))  
    return m.hexdigest()

def decode_base64(data):
    missing_padding=4-len(data)%4
    if missing_padding:
        data += '='* missing_padding
    return base64.b64decode(data)

headers={
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.9',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'Host':'jandan.net',
    'Referer':'http://jandan.net/',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
}

def getConstantAndHash(url):
    # page=BeautifulSoup(requests.get('http://jandan.net/ooxx',headers=headers).text,"lxml")
    # preUrl='http:'+page.select('.previous-comment-page')[0]['href']
    # html=requests.get(preUrl,headers=headers).text
    proxies = {"http":"http://27.39.226.123:8123"}
    html = requests.get(url, headers = headers).text
    j=re.search(r'.*<script\ssrc=\"\/\/(cdn.jandan.net\/static\/min.*?)\"><\/script>.*',html)
    jsFileUrl="http://"+j.group(1)
    jsFile=requests.get(jsFileUrl,headers=headers).text

    c=re.search(r'.*f_\w+\(e,\"(\w+)\".*',jsFile)
    constant=c.group(1)

    prePage=BeautifulSoup(html,"lxml")
    hashList=[]
    for item in prePage.select('.img-hash'):
        hashList.append(item.text)
    return constant,hashList

def spider(constant,hashList):
    index = 0
    os.chdir('./picture')
    for imgHash in hashList:
        url='http:'+parse(imgHash,constant)
        replace=re.match(r'(.*\.sinaimg\.cn\/)(\w+)(\/.+\.gif)',url)
        if replace:
            url=replace.group(1)+'large'+replace.group(3)
        e=re.match(r'.*(\.\w+)',url)
        extensionName=e.group(1)
        try:
            with open ("pao67"+str(index)+extensionName, 'wb') as f:
                headers['host']='wx3.sinaimg.cn'
                f.write(requests.get(url,headers=headers).content)
                f.close()
            print("第 %d 页第 %d 张图片写入完成" %(page,index))
        except:
            print('出现异常')
            continue
        time.sleep(1)
        index = index +1

if __name__=='__main__':
    print("start download")
    page = 73;
    url = "https://jandan.net/ooxx/page-"+ str(page) + "#comments"
    result=getConstantAndHash(url)
    constant=result[0]
    hashList=result[1]
    spider(constant,hashList)
