from bs4 import BeautifulSoup
import requests
import mysql.connector




conn = mysql.connector.connect(user = 'patrick', password = 'Password2011!', host = 'localhost', database = 'test')
cursor = conn.cursor()
cursor.execute('DROP TABLE IF EXISTS Inventory')
    
cursor.execute(
    """CREATE TABLE inventory(
        gunId  INT(10) PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(100),
        price VARCHAR(20))""")
urls = {1 : 'hot-deals/',2 : 'pistols/',3:'pistols/index3.html?sort_direction=1', 4:'pistols/index2.html?sort_direction=1'}
for i in range(1,len(urls)+1):
    guns = []
    prices = []
    
    r = requests.get('http://www.hyattgunstore.com/'+urls[i])

    soup = BeautifulSoup(r.content)
    arm = soup.select('a strong')
    price = soup.find_all('span', {'class':'price-value'})

    for i in price:
        price = i.text
        prices.append(price)
    print 'Length of prices = ' + str(len(prices))

    for i in arm:
        gun = i.text
        guns.append(gun)
    print 'Length of guns = ' + str(len(prices))


    ##class inventory:
    ##
    ##    storeName = 'Hyatt Gun Shop'
    ##
    ##    def __init__(self, gun='', price=''):
    ##        self.gun = gun
    ##        self.price = price
    ##
    ##    def __str__(self):
    ##        gunStr = 'The gun %s costs %s /n' %(self.gun, self.price)
    ##        return gunStr







    for i in zip(guns, prices):
        cursor.execute(" INSERT INTO inventory(name, price) VALUES(%s, %s)", (i))
    conn.commit()

while True:
    brand = raw_input('what brand of gun would you like to search for?')
    brand = brand.lower()
    if brand != 'q' or brand != 'quit':           
        cursor.execute('SELECT * FROM inventory WHERE name like "%'+ brand + '%"')
        for i in cursor.fetchall():
            print i[1], i[2]
    else:
        print 'Thank you for shopping with vArmory'
        conn.close()
        break


 


    



    

