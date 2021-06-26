import pymysql

connection = pymysql.connect(user='root', 
												password= "", 
												host='localhost',
												database = 'pW',
												)

print(connection)

cursor = connection.cursor()

sql = "INSERT INTO pW (url, apps, title) VALUES (%s, %s, %s)"
val = ("a", "b", "c")

cursor.execute(sql, val);

connection.commit()

records = cursor.fetchall()

for record in records:
	print(record)