import json
import re
import threading
import urllib
from urllib import request
from lxml import etree
import requests
import urllib3


def download_text(url):
    response = requests.get(url)
    response.encoding='utf-8'
    texthtml = etree.HTML(response.text)
    div = texthtml.xpath('//div[@class="vcon"]')[0]
    title = texthtml.xpath('//div[@class="top"]/h1[@class="title"]/text()')[0]
    contents = div.xpath('//p/text()')
    contents.insert(2, title)
    for content in contents[2:]:
        with open('./content/碧血剑全集.txt', 'a', encoding='utf-8') as fp:
            fp.write(content + '\n')
    print('下载完成%s'%(title))


def get_url(url):
    # url = 'http://www.jinyongwang.com/bi/'
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': 'IDE=AHWqTUnLr4_o_cuRfdz-rrwSaKndtWIuxYdN8XETvr8NhNhr9-jXHgbVGSbTQNjB',
        'referer': 'http://www.jinyongwang.com/bi/',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        'x-client-data': 'CJW2yQEIprbJAQjEtskBCKmdygEIqKPKAQixp8oBCOKoygEI8anKAQiXrcoBCM2tygEIy67KAQj3tMoB',
    }
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    xiaoshuo = response.text
    html = etree.HTML(xiaoshuo)
    # 书名
    title = html.xpath('//div/h1[@class="title"]/span/text()')[0]
    # 作者
    author = html.xpath('//div/p[@class="author"]/a/text()')[0]
    # 时间
    time = html.xpath('//div/p[@class="time"]/text()')[0]
    # 章节
    li = html.xpath('//div[@class="main"]/ul[@class="mlist"]/li')
    urlist = []
    threads = []
    for i in li:
        section_url = i.xpath('.//a/@href')[0]
        url1 = 'http://www.jinyongwang.com' + section_url
        download_text(url1)
        # t = threading.Thread(target=download_text, args=(url1,))
        # t.start()
        # threads.append(t)不能开多线程，下载顺序不一样
    #
    # for th in threads:
    #     th.join()#先全部执行完子线程再返回


if __name__ == '__main__':
    url = 'http://www.jinyongwang.com/bi/'
    get_url(url=url)
