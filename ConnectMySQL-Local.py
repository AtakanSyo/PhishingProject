import pymysql

connection = pymysql.connect(user='root', 
												password= "", 
												host='localhost',
												database = 'pW',
												)

print(connection)

cursor = connection.cursor()

sql = "SELECT url FROM pW"

cursor.execute(sql);

records = cursor.fetchall()


for record in records:
	record = str(record)[1:-2]
	
	print(record)
	sql = """UPDATE
  pW
SET
  Country = 'nlanlalnas'
WHERE
  url =(
    """ + record + ")"
	print(sql)
	cursor.execute(sql);
	connection.commit()