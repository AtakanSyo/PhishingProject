import pymysql

connection = pymysql.connect(user='root', 
												password= "", 
												host='34.134.226.251',
												database = 'phishingdb',
												ssl_ca = 'ssl/server-ca.pem',
												ssl_cert =  'ssl/client-cert.pem',
												ssl_key = 'ssl/client-key.pem'
												)

print(connection)

cursor = connection.cursor()

sql = """SELECT * FROM phishingwebsites"""

cursor.execute(sql);

records = cursor.fetchall()

for record in records:
	print(record)