import geoip2.database
import socket
import pymysql
import urllib.parse
from urllib.parse import urlsplit, urlparse
import hashlib
import requests

import time
import json



connection = pymysql.connect(user='root', 
												password= "", 
												host='localhost',
												database = 'pW'
												)
print(connection)

cursor = connection.cursor()

while(True): 

	sql = """SELECT url, IP FROM pW WHERE IP is not NULL"""

	cursor.execute(sql);

	records = cursor.fetchall()



	index = 0

	with geoip2.database.Reader('GeoLite2-City.mmdb') as reader:

			for record in records:

				print(index)
				index = index + 1

				url = record[0]


				parsed = urlparse(url)
				country, accuracy_radius = None, None

				try: # Try MaxMind
					theIP = socket.gethostbyname(parsed[1]) 
					response = reader.city(theIP);
					country = response.country.name
					accuracy_radius = response.location.accuracy_radius

				except Exception as error:
					print("MaxMind Error: ")
					print(error)

				if( country != None):
					sql = """UPDATE pW SET Country = {0} WHERE url = {1}""".format("'"+str(country)+"'", "'"+str(url)+"'")
					print(sql)
					cursor.execute(sql)
					connection.commit()
					print("Updated.")
				else:
					print("No country for old men.")

				if (accuracy_radius != None):
					sql = """UPDATE pW SET accuracy_radius = {0} WHERE url = {1}""".format(int(accuracy_radius), "'"+str(url)+"'")
					cursor.execute(sql)
					connection.commit()
					print("Updated.")
				else:
					print("No accuracy_radius for old men.")

			# IMPORTANT NOTE ABOUT UPTIME CYCLES: if 16 uptime cycles, it means a minimum of 15 hours. It is a range, such as this (1,16 ].

				print("End of Loop.")
	print("Sleeping for an hour.")
	time.sleep(3600)


