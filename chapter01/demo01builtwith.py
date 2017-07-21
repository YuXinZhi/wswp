import builtwith
import whois


'''
1.  builtwith
'''
bp = builtwith.parse('http://example.webscraping.com')
print(bp)
'''
{'web-servers': ['Nginx'], 'web-frameworks': ['Web2py', 'Twitter Bootstrap'], 'programming-languages': ['Python'], 'javascript-frameworks': ['jQuery', 'Modernizr', 'jQuery UI']}
'''

'''
2.  whois
'''
print(whois.whois('webscraping.com'))

'''
{
  "domain_name": "WEBSCRAPING.COM",
  "registrar": "GoDaddy.com, LLC",
  "whois_server": "whois.godaddy.com",
  "referral_url": "http://www.godaddy.com",
  "updated_date": "2013-08-20 00:00:00",
  "creation_date": [
    "2004-06-26 00:00:00",
    "2004-06-26 18:01:19"
  ],
  "expiration_date": [
    "2020-06-26 00:00:00",
    "2020-06-26 18:01:19"
  ],
  "name_servers": [
    "NS1.WEBFACTION.COM",
    "NS2.WEBFACTION.COM",
    "NS3.WEBFACTION.COM",
    "NS4.WEBFACTION.COM"
  ],
  "status": [
    "clientDeleteProhibited https://icann.org/epp#clientDeleteProhibited",
    "clientRenewProhibited https://icann.org/epp#clientRenewProhibited",
    "clientTransferProhibited https://icann.org/epp#clientTransferProhibited",
    "clientUpdateProhibited https://icann.org/epp#clientUpdateProhibited",
    "clientTransferProhibited http://www.icann.org/epp#clientTransferProhibited",
    "clientUpdateProhibited http://www.icann.org/epp#clientUpdateProhibited",
    "clientRenewProhibited http://www.icann.org/epp#clientRenewProhibited",
    "clientDeleteProhibited http://www.icann.org/epp#clientDeleteProhibited"
  ],
  "emails": [
    "abuse@godaddy.com",
    "contact@webscraping.com"
  ],
  "dnssec": "unsigned",
  "name": "Richard Penman",
  "org": null,
  "address": "13/815 Leonard St",
  "city": "Melbourne",
  "state": "Victoria",
  "zipcode": "3056",
  "country": "AU"
}

'''