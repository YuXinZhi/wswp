from queue import Queue
from urllib import robotparser,parse,error
import urllib.request       #???为啥from urllib import request就用不了???
import time
import datetime
import re

def link_crawler(seed_url,link_regex=None,delay=5,max_depth=-1,max_urls=-1,headers=None,user_agent='wswp',proxy=None,num_retries=1):
    '''
    爬取seed_url中匹配link_regex的链接
    '''
    #待爬取的URL队列
    crawl_queue = Queue()
    crawl_queue.put(seed_url)

    print('crawl_queue',crawl_queue.get())
    #爬过的URL的深度
    seen = {seed_url:0}
    #记录有多少链接被下载
    num_urls = 0
    rp = get_robots(seed_url)
    print(rp)
    throttle = Throttle(delay)
    headers = headers or {}
    if user_agent:
        headers['User-agent'] = user_agent

    while crawl_queue:
        url = crawl_queue()
        #检查robots.txt的限制
        if rp.can_fetch(user_agent,url):
            throttle.wait(url)
            html = download(url,headers,proxy=proxy,num_retries=num_retries)
            links = []

            depth = seen[url]
            if depth != max_depth:
                #可以继续爬
                if link_regex:
                    #过滤符合正则表达式的链接
                    links.extend(link for link in get_links(html) if re.match(link_regex,link))

                for link in links:
                    link = normalize(seed_url,link)
                    #检查是否爬过相同的域名
                    if same_domain(seed_url,link):
                        #成功，把该链接加入队列
                        crawl_queue.appenf(link)

            #检查是否达到下载的最大深度
            num_urls += 1
            if num_urls == max_urls:
                break
        else:
            print('Blocked by robots.txt:',url)



def get_robots(url):
    #初始化robots解析器
    rp = robotparser.RobotFileParser()
    rp.set_url(parse.urlparse(url,'/robots.txt'))
    rp.read()
    return rp

class Throttle:
    '''
    在相同的域名之间添加延迟
    '''
    def __init__(self,delay):
        #下载每个域名的间隔
        self.delay = delay
        #域名最后访问的时间戳
        self.domains = {}

    def wait(self,url):
        domain = parse.urlparse(url).netloc
        print('domain=',domain)
        last_accessed = self.domains.get(domain)

        if self.delay > 0 and last_accessed is not None:
            sleep_secs = self.delay - (datetime.datetime.now() - last_accessed).seconds
            if sleep_secs > 0:
                #最近访问过该域名，所以需要睡眠一段时间
                time.sleep(sleep_secs)

        #更新域名最后一次访问时间
        self.domains[domain] = datetime.datetime.now()

def download(url,headers,proxy,num_retries,data=None):
    print('Downloading:',url)
    request = urllib.request.Request(url,data,headers)
    opener = urllib.request.build_opener()
    if proxy:
        proxy_params = {parse.urlparse(url).scheme:proxy}
        opener.add_handler(urllib.request.ProxyHandler(proxy_params))
    try:
        response = opener.open(request)
        html = response.read()
        html = html.encode('utf-8')
        code = response.code
    except error.URLError as e:
        print('Download error:',e.reason)
        html = ''
        if hasattr(e,'code'):
            code = e.code
            if num_retries > 0 and 500 <= code < 600:
                #返回5xx错误
                return download(url,headers,proxy,num_retries-1,data)
            else:
                code = None
    return  html


def normalize(seed_url,link):
    """
    通过去除hash和添加域名标准化URL
    """
    link, _ = parse.urldefrag(link) #去除hash避免重复
    return parse.urljoin(seed_url,link)

def get_links(html):
    """
    返回包含html中的链接的链表
    """
    #一个从网页中提取所有链接的正则表达式
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']',re.IGNORECASE)
    #网页中所有的链接
    return webpage_regex.findall(html)

def same_domain(url1,url2):
    #当两个URL属于同一个域名时返回TRUE
    return parse.urlparse(url1).netloac == parse.urlparse(url2).netloc



if __name__ == '__main__':
    link_crawler('http://example.webscraping.com/places/default/index','/(index|view)',delay=0,num_retries=1,user_agent='BadCrawler')
    link_crawler('http://example.webscraping.com/places/default/index','/(index|view)',delay=0,num_retries=1,max_depth=1,user_agent='GoodCrawler')