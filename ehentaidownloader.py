from concurrent.futures import ThreadPoolExecutor,wait,as_completed
from socket import timeout
from turtle import done
from unittest.result import failfast
import requests
import re
import warnings
import os
import traceback
import importlib
warnings.filterwarnings('ignore')
url='https://e-hentai.org'
slist=[]

cookie=input("input your login cookie if any:")
head={
    "Connection": '''keep-alive''',
"Pragma": '''no-cache''',
"Cache-Control": '''no-cache''',
"sec-ch-ua": '''" Not A;Brand";v="99", "Chromium";v="98", "Microsoft Edge";v="98"''',
"sec-ch-ua-mobile": '''?0''',
"sec-ch-ua-platform": '''"Windows"''',
"DNT": '''1''',
"Upgrade-Insecure-Requests": '''1''',
"User-Agent": '''Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.43''',
"Accept": '''text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9''',
"Sec-Fetch-Site": '''same-origin''',
"Sec-Fetch-Mode": '''navigate''',
"Sec-Fetch-User": '''?1''',
"Sec-Fetch-Dest": '''document''',
"Referer": '''https://e-hentai.org/home.php''',
"Accept-Encoding": '''gzip, deflate, br''',
"Accept-Language": '''zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6''',
"Cookie": f"{cookie}"
}

gid=input("example url:https://e-hentai.org/g/2134055/c28c645647/?p=1\nexample gallery id:2134055/c28c645647\ninput the e-hentai gallery id to download:")
try:os.makedirs(gid)
except:pass
res=requests.get(f"{url}/g/{gid}",verify=False,headers=head)
endp=res.text.rfind(f'''</a></td><td onclick="document.location=this.firstChild.href"><a href="{url}/g/{gid}/?p=1" onclick="return false">''')
count=res.text[:endp]
try:count=int(count[count.rfind(">")+1:])
except:count=1

print("pages:",count)

reslist=re.findall('''<a href="https:\/\/e-hentai\.org\/s\/([a-z\d\-/]+?)">''',res.text)
slist.extend(reslist)

def get_limit():
    res=requests.get(f"{url}/home.php",verify=False,headers=head)
    relist=re.findall('''<p>You are currently at <strong>(\d+?)<\/strong>''',res.text)
    return relist[0]

if cookie:
    print("limit used:",get_limit())

def fetch_urls(pid):
    global count,slist
    print(f"fetching page {pid}/{count}...")
    res=requests.get(f"{url}/g/{gid}/?p={pid}",verify=False,headers=head)
    reslist=re.findall('''<a href="https:\/\/e-hentai\.org\/s\/([a-z\d\-/]+?)">''',res.text)
    slist.extend(reslist)

threads=ThreadPoolExecutor(20)
for i in range(1,count):
    threads.submit(fetch_urls,i)
threads.shutdown(True)

sdict={each:None for each in slist}
# finally:
num=len(slist)
print("total images:",num)

def fetch_images(i,key):
    global num,sdict,slist
    print(f"fetching image {i}/{num}...")
    if sdict[key]:
        print(f"cache {key} found!")
        res=requests.get(sdict[key],verify=False,headers=head,timeout=600)
        open(f"{gid}/{key[key.rfind('/')+1:]}.jpg","wb").write(res.content)
    else:
        res=requests.get(f"{url}/s/{key}" ,verify=False,headers=head)
        # print(res.text)
        if cookie:
            ourl=re.findall('''<a href="(https:\/\/e-hentai\.org\/fullimg\.php\?[\w=;&\-]+?)">''',res.text)[0].replace("&amp;","&")
            # print(ourl)
            res=requests.get(ourl,verify=False,headers=head,allow_redirects=False)
            rurl=res.headers["location"]
            print(f"resolving real img url of {key}...",rurl)
            sdict[key]=rurl
            res=requests.get(rurl,verify=False,headers=head,timeout=600)
            open(f"{gid}/{key[key.rfind('/')+1:]}.jpg","wb").write(res.content)
            print("limit used:",get_limit())
        else:
            murl=re.findall('''<img id="img" src="([\w:/;=\.\-]+?)"''',res.text)[0]
            res=requests.get(murl,verify=False,headers=head)
            print(f"not login! download 1280 img url of {key}...",murl)
            open(f"{gid}/{key[key.rfind('/')+1:]}_1280.jpg","wb").write(res.content)
    slist.remove(key)


with ThreadPoolExecutor(max_workers=60) as t: 
    for j in range(int((num+59)//60)):
        all_task = [t.submit(fetch_images,i+j*60,each) for i,each in enumerate(slist[j*60:(j+1)*60])]
        lastundo=[]
        undo=all_task
        while len(lastundo)!=len(undo):
            lastundo=undo
            done,undo=wait(all_task, timeout=300)
            # print(done,undo)

open(f"{gid}/info.py","w").write(f"{sdict}\n{slist}")