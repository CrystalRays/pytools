import requests
import json
import os

cookies=input("请输入Cookie：")

headers={"accept": "application/json, text/plain, */*",
"content-type": "application/json;charset=UTF-8",
"cookie": cookies,
"origin": "https://manga.bilibili.com",
"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36 Edg/88.0.705.56"}
def post(url,data):
    res=requests.post(url=url,headers=headers,json=data)
    return json.loads(res.text)
mangaid=input("请输入漫画id（例如https://manga.bilibili.com/detail/mc29226即为29226）:")

savepath=f"bilimangaimages/{mangaid}"
# 获取每一话id
res=post(url="https://manga.bilibili.com/twirp/comic.v1.Comic/ComicDetail?device=pc&platform=web",data={"comic_id":int(mangaid)})
chapterids=[(each["id"],each["ord"]) for each in  res["data"]["ep_list"]]
def getchapter(chapterid):
    res=post(url="https://manga.bilibili.com/twirp/comic.v1.Comic/GetImageIndex?device=pc&platform=web",data={"ep_id":chapterid})
    return [each["path"] for each in res["data"]["images"]]
def gettoken(path):
    res=post(url="https://manga.bilibili.com/twirp/comic.v1.Comic/ImageToken?device=pc&platform=web",data={"urls":f"[\"{path}\"]"})
    return res["data"][0]["url"]+"?token="+res["data"][0]["token"]
def getimage(url,chapterid,imageid):
    res=requests.get(url)
    open(f"{savepath}/{chapterid}/{imageid}.jpg","wb").write(res.content)
    print(url)
for chapterid,ordid in chapterids:
    print(chapterid)
    os.makedirs(f"{savepath}/{j}")
    images=tuple(map(gettoken,getchapter(chapterid)))
    i=0
    for url in images:
        i+=1
        getimage(url,ordid,i)