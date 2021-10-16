import pymysql
import requests

connection = pymysql.connect(user='root', 
												password= "", 
												host='localhost',
												database = 'pW'
												)

url = 'https://www.whoisxmlapi.com/whoisserver/WhoisService'
payload = {'domainName': 'www.telescopestobuy.com', 'apiKey': 'at_FwDbXP10L8oe8jXKQ17dRoYhXhCJ3', 'outputFormat':'JSON'}
r = requests.get(url, params=payload)

print(r.headers.get('Content-Type'))
print(r.json()['WhoisRecord']['nameServers']['hostNames'])

print(connection)

cursor = connection.cursor()

sql = """SELECT url FROM pW"""

cursor.execute(sql);

records = cursor.fetchall()

for record in records:
	URL = record
	url = str(URL)[2:-3]
	print(url)