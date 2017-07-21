import urllib.request
import urllib.error
def download(url,user_agent='wswp',num_retries=2):
    print('Downloading:',url)
    headers = {'User-agent':user_agent}
    request = urllib.request.Request(url,headers=headers)
    try:
        html = urllib.request.urlopen(request).read()
        html = html.decode('utf-8')
        print(html)
    except urllib.error.URLError as e:
        print('Downlaod error:',e.reason)
        html = None
        if num_retries > 0:
            if hasattr(e,'code') and 500 <= e.code <600:
                return download(url,user_agent,num_retries-1)
    return html