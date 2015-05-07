import requests
from bs4 import BeautifulSoup
import urllib2
import urlparse

url = 'http://grabagun.com/firearms.html'

urls = [url]
visited = [url]
products = []
prices = []

while len(urls) > 0:
    try:
        htmltext = requests.get(urls[0])
        
    except:
        print urls[0]
    print 'visiting = ' + urls[0]

    
    soup = BeautifulSoup(htmltext.content)
    urls.pop(0)
    print 'Length of urls = ' + str(len(urls))

    tag = soup.find_all('h2', {'class':'product-name'})
    for i in tag:
        product = i.text
        products.append(product)

    money = soup.find_all('span', {'class':'price'})
    for i in money:
        price = i.text
        prices.append(price)

    for tag in soup.find_all('a', href=True):
        tag = urlparse.urljoin(url,tag['href'])
        if url in tag and tag not in visited:
##            print tag['href']
            urls.append(tag)
            visited.append(tag)
           
print products
