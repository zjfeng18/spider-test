# -*- coding: utf-8 -*-
import requests # requests作为我们的html客户端
from pyquery import PyQuery as Pq # pyquery来操作dom


class SegmentfaultQuestionSpider(object):

    def __init__(self, segmentfault_id): # 参数为在segmentfault上的id
        self.url = 'http://segmentfault.com/q/{0}'.format(segmentfault_id)
        self._dom = None # 弄个这个来缓存获取到的html内容，一个蜘蛛应该之访问一次

    @property
    def dom(self): # 获取html内容
        if not self._dom:
            document = requests.get(self.url)
            document.encoding = 'utf-8'
            self._dom = Pq(document.text)
        return self._dom

    @property 
    def title(self): # 让方法可以通过s.title的方式访问 可以少打对括号
        return self.dom('h1#questionTitle').text() # 关于选择器可以参考css selector或者jquery selector, 它们在pyquery下几乎都可以使用

    @property
    def content(self):
        return self.dom('.question.fmt').html() # 直接获取html 胆子就是大 以后再来过滤

    @property
    def answers(self):
        return list(answer.html() for answer in self.dom('.answer.fmt').items()) # 记住，Pq实例的items方法是很有用的

    @property
    def tags(self):
        return self.dom('ul.taglist--inline > li').text().split() # 获取tags，这里直接用text方法，再切分就行了。一般只要是文字内容，而且文字内容自己没有空格,逗号等，都可以这样弄，省事。

#分类页
class SegmentfaultTagSpider(object):

    def __init__(self, tag_name, page=1):
        self.url = 'http://segmentfault.com/t/%s?type=newest&page=%s' % (tag_name, page)
        self.tag_name = tag_name
        self.page = page
        self._dom = None

    @property
    def dom(self):
        if not self._dom:
            document = requests.get(self.url)
            document.encoding = 'utf-8'
            self._dom = Pq(document.text)
            self._dom.make_links_absolute(base_url="http://segmentfault.com/") # 相对链接变成绝对链接 爽
        return self._dom


    @property
    def questions(self):
        return [question.attr('href') for question in self.dom('h2.title > a').items()]

    @property
    def has_next_page(self): # 看看还有没有下一页，这个有必要
        return bool(self.dom('ul.pagination > li.next')) # 看看有木有下一页

    def next_page(self): # 把这个蜘蛛杀了， 产生一个新的蜘蛛 抓取下一页。 由于这个本来就是个动词，所以就不加@property了
        if self.has_next_page:
            self.__init__(tag_name=self.tag_name ,page=self.page+1)
        else:
            return None