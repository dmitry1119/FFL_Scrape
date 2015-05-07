import requests
from bs4 import BeautifulSoup
import urllib2
import urlparse
import time
urlSnippet = 'http://grabagun.com/firearms/'
url = 'http://grabagun.com/firearms/'

urls = [url]
visited = [url]
products = []
prices = []
print 'Length of urls = ' + str(len(urls))
while len(urls)>0:
    try:
        html = requests.get(urls[0])
    except:
        print urls[0]
    
    print 'visiting = ' + urls[0]

    
    soup = BeautifulSoup(html.text, 'html5lib')
    urls.pop(0)
    print 'Length of urls = ' + str(len(urls))

    tag = soup.findAll('h2', {'class':'product-name'})
    for i in tag:
        product = i.text
        if product not in products:
            products.append(product)

    money = soup.findAll('span', {'class':'price'})
    for i in money:
        price = i.text
        if price not in prices:
            prices.append(price)

    for tag in soup.findAll('a',href=True):
        tag = urlparse.urljoin(url,tag['href'])
        if urlSnippet in tag and tag not in visited:
            print tag
            urls.append(tag)
            visited.append(tag)
           
print products
