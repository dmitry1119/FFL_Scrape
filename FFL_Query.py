import mysql.connector
from time import sleep

conn = mysql.connector.connect(user = 'patrick', password = 'Password2011!', host = 'localhost', database = 'test')
cursor = conn.cursor()



while True:
    brand = raw_input('what product would you like to search for?\n\n')
    brand = brand.lower()
    if brand == 'q' or brand == 'quit':
        
        print 'Thank you for shopping with vArmory'
        print 'Goodbye'
        sleep(4)
        conn.close()
        break
    else:
        
        cursor.execute('SELECT * FROM inventory WHERE product like "%'+ brand + '%" ORDER BY price ASC LIMIT 100')
        print '\n'
        for i in cursor.fetchall():
            print 'Product:  ' + i[1],'//   Price = ' + i[2]
        print '\n\n'
