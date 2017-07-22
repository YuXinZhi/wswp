from urllib import parse
import datetime
import time

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
