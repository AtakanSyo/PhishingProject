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
from bs4 import UnicodeDammit
import _thread

# Implement remedy. Solve problems if there is in Google Drive refresh token structure.

connection = pymysql.connect(user='root', 
												password= "", 
												host='localhost',
												database = 'pW'
												)
print(connection)

cursor = connection.cursor()

# Add new URL'S.

while(True): 

	sql = """SELECT url FROM pW"""

	cursor.execute(sql);

	records = cursor.fetchall()

	index = 0

	for record in records:

		print("Beginning of loop.")
		index = index + 1

		url, apps, title= None, None, None

		URL = record
		url = str(URL)[2:-3]
		url_for_sql = str(URL)[1:-2]
		print(url)



		# to check if the variables hold, print all of them at the beginning of the loop and at the end. If 

		print(index)

		parsed = urlparse(url)

		try: # Try Wappalyzer
			WappalyzerData = WebPage(url).info() 
			apps = str(WappalyzerData['apps'])

			title = str(WappalyzerData['title'])
			title = title.replace("'",' ')

		except Exception as error:
			print("Wappalyzer Error: ")
			print(error)

		# General updater. Delete uptime_cycles increment from here.

		if (apps != None and apps != ''):
			sql = """UPDATE pW SET apps = {0} WHERE url = {1}""".format( "'"+apps+"'", str(url_for_sql))
			cursor.execute(sql)
			connection.commit()
			print("Updated.")
		else:
			print("No apps for old men.")

		if (title != None and title != 'None'):
			sql = """UPDATE pW SET title = {0} WHERE url = {1}""".format( "'"+title+"'", str(url_for_sql))
			cursor.execute(sql)
			connection.commit()
			print("Updated.")
		else:
			print("No title for old men.")	

		# IMPORTANT NOTE ABOUT UPTIME CYCLES: if 16 uptime cycles, it means a minimum of 15 hours. It is a range, such as this (1,16 ].

		print("End of Loop.")
	print("Sleeping for an hour.")
	time.sleep(3600)
