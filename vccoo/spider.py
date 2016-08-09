# -*- coding: utf-8 -*-
import requests,time,os # requests作为我们的html客户端
from pyquery import PyQuery as Pq # pyquery来操作dom
# https://segmentfault.com/a/1190000002549756
# 文章详情页 http://www.vccoo.com/v/bf38cd
class Getshow(object):

    def __init__(self, show_id): # 参数为在vccoo上的id
        self.url = 'http://www.vccoo.com/v/{0}'.format(show_id)
        self._dom = None # 弄个这个来缓存获取到的html内容，一个蜘蛛应该之访问一次

    @property
    def dom(self): # 获取html内容
        if not self._dom:
            document = requests.get(self.url)
            document.encoding = 'utf-8'
            self._dom = Pq(document.text)
        return self._dom
    # 标题
    @property
    def title(self): # 让方法可以通过s.title的方式访问 可以少打对括号
        return self.dom('h1.article-title').text() # 关于选择器可以参考css selector或者jquery selector, 它们在pyquery下几乎都可以使用
    # 内容
    @property
    def content(self):
        return self.dom('.article-content').html() # 直接获取html 胆子就是大 以后再来过滤
    # 公众号logo
    @property
    def wxlogo(self):
        return self.dom('.author-name img').attr('src')

    # 公众号名称
    @property
    def wxname(self):
        return self.dom('.author-name strong').text()

    # 发布时间
    @property
    def addtime(self):
        return self.dom('.author-name').text()[-10:] # 获取tags，这里直接用text方法，再切分就行了。一般只要是文字内容，而且文字内容自己没有空格,逗号等，都可以这样弄，省事。
   # 暂时保存成文档
    def save(self):
        sDir='d:/test/'
        if os.path.exists(sDir)==False:
            os.mkdir(sDir)
        sName = sDir+str(int(time.time()))+'.txt'
        print('正在下载'+self.title+'文章')
        m = self.title+'\n'+self.wxlogo+'\n'+self.wxname+'\n'+self.addtime+'\n'+self.content
        with open(sName,'wb') as file:
            file.write(m.encode())
        file.close()

#栏目页 http://www.vccoo.com/category/?id=104&page=2
class Getlist(object):

    def __init__(self, catid, page=1):
        self.url = "http://www.vccoo.com/category/?id=%d&page=%d" % (catid , page)
        self.catid = catid
        self.page = page
        self._dom = None

    @property
    def dom(self):
        if not self._dom:
            document = requests.get(self.url)
            document.encoding = 'utf-8'
            self._dom = Pq(document.text)
            self._dom.make_links_absolute(base_url="http://www.vccoo.com/") # 相对链接变成绝对链接 爽
        return self._dom


    @property
    def urls(self):
        return [url.attr('href') for url in self.dom('.list-con h3 > a').items()]

    @property
    def has_next_page(self): # 看看还有没有下一页，这个有必要
        return bool(self.dom('.pages ul li .next-page')) # 看看有木有下一页

    def next_page(self): # 把这个蜘蛛杀了， 产生一个新的蜘蛛 抓取下一页。 由于这个本来就是个动词，所以就不加@property了
        if self.has_next_page:
            self.__init__(catid=self.catid ,page=self.page+1)
        else:
            return None

    def crawl(self): # 采集当前分页
        sf_ids = [url.split('/')[-1] for url in self.urls]
        con=len(sf_ids)
        print('此页共要采集%s篇文章' %con)
        i=1
        for sf_id in sf_ids:
            print('此页第%d篇文章采集中' %i)
            Getshow(sf_id).save()
            i+=1
            time.sleep(1)

    def crawl_all_pages(self):
        while True:
            print(u'正在抓取栏目:%d, 分页:%d' % (self.catid, self.page))
            self.crawl()
            if not self.has_next_page:
                break
            else:
                self.next_page()

# 测试
# s = Getshow('bf38cd')
# print(s.title)
# print(s.content)
# print(s.wxlogo)
# print(s.wxname)
# print(s.addtime)

# s=Getlist(104)
# for url in s.urls:
#     show =Getshow(url.split('/')[-1])
#     print(show.title+':'+url)


s=Getlist(104)
# if not s.has_next_page:
#     print('没有下一页')
# else:
#     print('有下一页')
s.crawl_all_pages()