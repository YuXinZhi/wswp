import re
from chapter01.download import download

def crawl_sitemap(url):
    count = 1
    sitemap = download(url)
    links = re.findall('<loc>(.*?)</loc>',sitemap)
    for link in links:
        html = download(link)
        print(html)



if __name__ == '__main__':
    crawl_sitemap('http://example.webscraping.com/places/default/sitemap.xml')