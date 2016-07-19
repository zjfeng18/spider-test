# api爬取图片
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')
import requests

url='http://www.tngou.net/tnfs/api/list'
param={'page':1,'rows':20}
r=requests.get(url,param).json()
# print(r)

def saveImage(imgUrl,imgName):
    response = requests.get(imgUrl,stream = True)
    image=response.content
    dst = 'f:\\girl_photo\\'
    path = dst + imgName
    print('save the file:'+path+'\n')
    with open(path,'wb') as a:
        a.write(image)
    a.close()

def run():
    for line in r['tngou']:
        title=line['title']
        img=line['img']
        src_path='http://tnfs.tngou.net/image'+img
        saveImage(src_path,title+'.jpg')
run()