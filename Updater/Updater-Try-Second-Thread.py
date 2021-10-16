import geoip2.database
import socket
import pymysql
import urllib.parse 
from urllib.parse import urlsplit, urlparse
import hashlib
import requests
from Wappalyzer import WebPage
from Wappalyzer import Wappalyzer
import time
import json
import _thread

# Implement remedy. Solve problems if there is in Google Drive refresh token structure.

PYTHONHASHSEED=0

def refreshToken(client_id, client_secret, refresh_token): # Function for refreshing Google Drive access every 1 hour.
        params = {
                "grant_type": "refresh_token",
                "client_id": client_id,

                "client_secret": client_secret,
                "refresh_token": refresh_token
        }

        authorization_url = "https://www.googleapis.com/oauth2/v4/token"

        r = requests.post(authorization_url, data=params)

        if r.ok:
                return r.json()['access_token']
        else:
                return None

geoIndex = 0

def geoLiteUpdater():
	print("Beginning of geoLite loop.")
	with geoip2.database.Reader('GeoLite2-City.mmdb') as reader:
		for record in records:
			country, accuracy_radius = None, None
			try: # Try MaxMind
				theIP = socket.gethostbyname(parsed[1]) 
				response = reader.city(theIP);
				country = response.country.name
				accuracy_radius = response.location.accuracy_radius
				IP = response.traits.ip_address # Request library kullan.
			except Exception as error:
				print("MaxMind Error: ")
				print(error)

			if( country != None):
				sql = """UPDATE pW SET Country = {0} WHERE url = {1}""".format("'"+str(country)+"'", str(url_for_sql))
				cursor.execute(sql)
				connection.commit()
				print("Updated.")
			else:
				print("No country for old men.")

			if (accuracy_radius != None):
				sql = """UPDATE pW SET accuracy_radius = {0} WHERE url = {1}""".format(int(accuracy_radius), str(url_for_sql))
				cursor.execute(sql)
				connection.commit()
				print("Updated.")
			else:
				print("No accuracy_radius for old men.")


connection = pymysql.connect(user='root', 
												password= "", 
												host='localhost',
												database = 'pW'
												)
print(connection)

cursor = connection.cursor()

# Add new URL'S.

url_openphish = "https://openphish.com/feed.txt"

while(True): 

	sql = """SELECT url FROM pW WHERE remedy = 0"""

	cursor.execute(sql);

	records = cursor.fetchall()

	index = 0

	_thread.start_new_thread( geoLiteUpdater , ())

	with geoip2.database.Reader('GeoLite2-City.mmdb') as reader:
		for record in records:
			print("Beginning of loop.")
			index = index + 1

			country, IP, accuracy_radius, req = None, None, None, None

			URL = record
			url = str(URL)[2:-3]
			url_for_sql = str(URL)[1:-2]
			print(url)

			# to check if the variables hold, print all of them at the beginning of the loop and at the end. If 

			parsed = urlparse(url)



			# General updater. Delete uptime_cycles increment from here.

			# if( country != None):
			# 	sql = """UPDATE pW SET Country = {0} WHERE url = {1}""".format("'"+str(country)+"'", str(url_for_sql))
			# 	cursor.execute(sql)
			# 	connection.commit()
			# 	print("Updated.")
			# else:
			# 	print("No country for old men.")

			# if (accuracy_radius != None):
			# 	sql = """UPDATE pW SET accuracy_radius = {0} WHERE url = {1}""".format(int(accuracy_radius), str(url_for_sql))
			# 	cursor.execute(sql)
			# 	connection.commit()
			# 	print("Updated.")
			# else:
			# 	print("No accuracy_radius for old men.")

			# IMPORTANT NOTE ABOUT UPTIME CYCLES: if 16 uptime cycles, it means a minimum of 15 hours. It is a range, such as this (1,16 ].

			print("End of Loop.")

	print("Taking a nap for ten seconds. Testing purposes.")
	time.sleep(10)

