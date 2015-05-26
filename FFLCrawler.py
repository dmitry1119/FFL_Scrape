import requests
from bs4 import BeautifulSoup
import urllib2
import urlparse
import thread
import time

products = []
prices = []
hurl = 'http://www.hyattgunstore.com/'
url = 'http://grabagun.com/firearms/'


def scrapeGrab(url):
    urls = [url]
    visited = [url]
    print 'Length of urls = ' + str(len(urls))
    for i in range(5000):
        try:
            html = requests.get(urls[0])
        except:
            print urls[0]
        
        print 'visiting = ' + urls[0]
        visited.append(urls[0])
        
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
            if url in tag and tag not in visited:
                if tag not in urls:
                    urls.append(tag)
                

scrapeGrab(url)
##def scrapeHyatt(hurl):
##    hurls = [hurl]
##    hvisited = [hurl]
##
##    print 'Length of urls = ' + str(len(hurls))
##    for i in range(10):
##        try:
##            html = requests.get(hurls[0])
##        except:
##            print urls[0]
##        
##        print 'visiting = ' + hurls[0]        
##        soup = BeautifulSoup(html.text, 'html5lib')
##        hurls.pop(0)
##        print 'Length of urls = ' + str(len(hurls))
##
##        tag = soup.select('a strong')
##        for i in tag:
##            product = i.text
##            if product not in products:
##                products.append(product)
##
##        money = soup.findAll('span', {'class':'currency'})
##        for i in money:
##            price = i.text
##            if price not in prices:
##                prices.append(price)
##
##        for tag in soup.findAll('a',href=True):
##            tag = urlparse.urljoin(hurl,tag['href'])
##            if hurl in tag and tag not in hvisited:
##                print tag
##                hurls.append(tag)
##                hvisited.append(tag)


##thread.start_new_thread(scrapeHyatt,(hurl,))
##    time.sleep(1)
##thread.start_new_thread(scrapeGrab, (url,))

           
import mysql.connector
conn = mysql.connector.connect(user = 'patrick', password = 'Password2011!', host = 'localhost', database = 'test')
cursor = conn.cursor()
cursor.execute('DROP TABLE IF EXISTS Inventory')
try:   
    cursor.execute(
        """CREATE TABLE inventory(
            Id  INT(10) PRIMARY KEY AUTO_INCREMENT,
            product VARCHAR(100),
            price VARCHAR(100))""")

    for i in zip(products, prices):
            cursor.execute(" INSERT INTO inventory(product, price) VALUES(%s, %s)", (i))
    conn.commit()
    conn.close()

except Exception as e:
    print e
