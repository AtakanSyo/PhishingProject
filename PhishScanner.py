import requests
import time
import pymysql

connection = pymysql.connect(user='root', 
												password= "", 
												host='localhost',
												database = 'pW'
												)
print(connection)

cursor = connection.cursor()

url_openphish = "https://openphish.com/feed.txt"
req = requests.get(url_openphish)
html = req.content

html = html.decode('utf-8')
urls=html.splitlines()

Url_List=list(urls)
# Start adding comments.
while(True):
	for i in range(len(Url_List)): 
		try:
			print(i)
			sql = "INSERT IGNORE INTO pW (url) VALUES (%s)"
			value = (str(Url_List[i]))
			print(value)
			cursor.execute(sql, value);
			print(cursor.rowcount, "record inserted.")
			connection.commit()
		except Exception as fnf_error:
			print(fnf_error)
			print(fnf_error.__class__.__name__)
	time.sleep(3600)