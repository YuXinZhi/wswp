import itertools
from chapter01 import download
for page in itertools.count(1):
    url = 'http://example.webscraping.com/places/default/view/-%d'%page
    html = download(url)
    if html is None:
        break
    else:
        pass
    