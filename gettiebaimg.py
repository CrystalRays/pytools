import requests

# getpage
d_url="https://tieba.baidu.com/p/7004384290?see_lz=1"

url=input("please input url:")

savedir=input("please input savepath:")
if not savedir:savedir="%appdata%/../../desktop/17/"

try:res=requests.get(url)
except:res=requests.get(d_url)
text=res.text

#get jpg url
jpglist=[]
while text.find('<img class="BDE_Image"')!=-1:
    text=text[text.find('<img class="BDE_Image"')+len('<img class="BDE_Image"'):]
    text=text[text.find('src="')+5:]
    jpglist.append(text[:text.find('jpg')+3])

# download jpg

jpglist=["https://imgsa.baidu.com/forum/pic/item/"+each[each.rfind("/")+1:] for each in jpglist]
l=len(jpglist)
for i in range(l):
    res=requests.get(jpglist[i])
    print("%d/%d"%(i,l),end="\r")
    open(savedir+"%d.jpg"%i,"wb+").write(res.content)
