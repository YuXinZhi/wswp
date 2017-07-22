from urllib import robotparser
rp = robotparser.RobotFileParser()
rp.set_url('https://webscraping.com/robots.txt')
url = 'https://example.webscraping.com'
user_agent = 'Badcrawler'
r = rp.can_fetch(user_agent,url)
print(r)