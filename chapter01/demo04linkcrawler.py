import re
from chapter01.download import download
from urllib import parse

def link_crawler(seed_url,link_regex):
    crawl_queue = [seed_url]
    #把已经遍历的链接放到集合seen中
    seen = set(seed_url)
    while crawl_queue:
        url = crawl_queue.pop()
        html = download(url)
        for link in get_links(html):
            print(link)
            if re.match(link_regex,link):
                link = parse.urljoin(seed_url,link)
                if link not in seen:
                    seen.add(link)
                    crawl_queue.append(link)

def get_links(html):
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']',re.IGNORECASE)
    return webpage_regex.findall(html)

if __name__ == '__main__':
    link_crawler('http://example.webscraping.com/places/default','/(index|view)')