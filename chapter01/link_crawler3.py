from queue import Queue
from urllib import robotparser,parse,error
import urllib.request       #???为啥from urllib import request就用不了???
import time
import datetime


def link_crawler(seed_url,link_regex=None,delay=5,max_depth=-1,max_urls=-1,headers=None,user_agent='wswp',proxy=None,num_retries=1):
    '''
    爬取seed_url中匹配link_regex的链接
    '''
    #待爬取的URL队列
    crawl_queue = Queue.deque([seed_url])
    #爬过的URL的深度
    seen = {seed_url:0}
    #记录有多少链接被下载
    num_urls = 0
    rp = get_robots(seed_url)
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
            link = []

            depth = seen[url]
            if depth != max_depth:
                #可以继续爬
                if link_regex:
                    link = normalize(seed_url,link)



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
    
    """