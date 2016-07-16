import spider
# s = spider.SegmentfaultQuestionSpider('1010000002542775')
# print (s.url)
# print (s.title)
# print (s.content)


s = spider.SegmentfaultTagSpider('微信')
question1 = s.questions[0]
question_spider = spider.SegmentfaultQuestionSpider(question1.split('/')[-1])
print(question_spider.title)
print(s.tag_name)
print(s.page)
s.next_page()
print(s.page)