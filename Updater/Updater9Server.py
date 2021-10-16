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

	# Send remedy URL's to the remedy table.

	sql = """ UPDATE pW SET remedy = 1 WHERE changed_content = 1 """

	print("Changed contents are remedied.")
	cursor.execute(sql)
	connection.commit()

	print("-------------------------------------------")

	#Adding the urls. 
	# OpenPhish


	req = requests.get(url_openphish)
	html = req.content

	html = html.decode('utf-8')
	urls=html.splitlines()

	Url_List=list(urls)

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




	# url = 'https://urlhaus-api.abuse.ch/v1/urls/recent/'
	# r = requests.get(url)

	# print(r.headers.get('Content-Type'))
	# print(r.json()['urls'][0]['url'])

	# urlHaus = r.json()['urls']

	# for x in urlHaus:
	# 	print(x['url'])

	# 	url = x['url']

	# 	try:
	# 		sql = "INSERT IGNORE INTO pW (url) VALUES (%s)"
	# 		value = url
	# 		print(value)
	# 		cursor.execute(sql, value);
	# 		print(cursor.rowcount, "record inserted.")
	# 		connection.commit()
	# 	except Exception as fnf_error:
	# 		print(fnf_error)
	# 		print(fnf_error.__class__.__name__)

	sql = """SELECT url FROM pW WHERE remedy = 0"""

	cursor.execute(sql);

	records = cursor.fetchall()

	index = 0

	for record in records:
		print("Beginning of loop.")
		index = index + 1

		IP, req = None, None
		url, hashPhish, phish_status_code, encodingGuess = None, None, None, ""

		URL = record
		url = str(URL)[2:-3]
		url_for_sql = str(URL)[1:-2]
		print(url)

		sql = """UPDATE
		  pW
		SET
		  uptime_cycles = uptime_cycles + 1
		WHERE
		  url ={0} AND changed_content = 0""".format(str(url_for_sql))

		cursor.execute(sql)
		connection.commit()

		print("------------------------------------------")



		# to check if the variables hold, print all of them at the beginning of the loop and at the end. If 

		print(index)

		parsed = urlparse(url)

		try: # Try basic HTTPS request.
			req = requests.get(url, timeout = 15)

			IP = socket.gethostbyname(parsed[1]) 

			phish_status_code = req.status_code
			html = req.content

			UnicodeDammitObject = UnicodeDammit(html)

			htmlString = UnicodeDammitObject.unicode_markup # Content encoding is guessed.

			print("Encoding: ")

			encodingGuess = UnicodeDammitObject.original_encoding

			print(encodingGuess)

			hashPhish = hashlib.sha256(req.content).hexdigest()

			# Update the DB.
			sql = """UPDATE
			  pW
			SET
			  changed_content = 1, remedy_reason = "ChangedContent"
			WHERE
			  url ={0} AND contentHash != {1} AND uptime_cycles >= 0""".format(str(url_for_sql),"'" + str(hashPhish) + "'")
			cursor.execute(sql)
			connection.commit()

			print("-------------------------------------------")

			file1 = open("yalama.txt", "w+")
			# print(str(html))
			file1.write(str(html))
			file1.close()

			# File and content is ready. Upload on Google drive.

			client_id = "835124988936-dn2kuh7722eb3pqtj8bv51keg32dhs15.apps.googleusercontent.com"
			client_secret = "G8oLWgxB1Z6eK-XUmKCQBNpT"
			refresh_token = "1//042ho09qIcm-WCgYIARAAGAQSNwF-L9IrUPjYED8tA4DgIxUMkQg_cpPjyv45l62CCvGRj94O0LOntaQtlBXz500_BmYLPMnaWIw"

			x = refreshToken(client_id, client_secret, refresh_token)

			x = None # Testing Purposes.

			if x != None:

				headers = {"Authorization": "Bearer "+x}

				sql = """ SELECT changed_content FROM pW WHERE url = {0}""".format(url_for_sql)

				cursor.execute(sql)

				contentStatus = cursor.fetchall()[0][0]

				sql = """ SELECT uptime_cycles FROM pW WHERE url = {0}""".format(url_for_sql)

				cursor.execute(sql)

				uptime_status = cursor.fetchall()[0][0]

				if uptime_status == 0:
					
					para = {
					    "name": url,
					    "parents": ["1qYiwd9fJtEACga-1XujlH2gtne6-eOTi"] # Before folder.
					}
					files = {
					    'data': ('metadata', json.dumps(para), 'application/json; charset=UTF-8'),
					    'file': open("yalama.txt", "rb")
					}
					r = requests.post(
						    "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
						    headers=headers,
						    files=files
						)
					print(r)

				if contentStatus == 1:
					para = {
					    "name": url,
					    "parents": ["1uUsQZJLRbcSquqnZmIBaARItrPGl9TsM"] # After folder.
					}
					files = {
					    'data': ('metadata', json.dumps(para), 'application/json; charset=UTF-8'),
					    'file': open("yalama.txt", "rb")
					}
					r = requests.post(
					    "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
					    headers=headers,
					    files=files
					)

			else:
				print("Refresh token is null.")

			# File Uploaded.


		except Exception as error:
			print("HTTPS Error: ")
			print(error)
			print(type(error))
			if type(error) == requests.exceptions.ConnectionError:
				print("Connection Error. Flagging as remedy and breaking the update.")
				sql = """ UPDATE pW SET remedy = 1 WHERE url = {0}""".format(str(url_for_sql))
				cursor.execute(sql)
				connection.commit()
				sql = """ UPDATE pW SET remedy_reason = "ConnectionError" WHERE url = {0}""".format(str(url_for_sql))
				cursor.execute(sql)
				connection.commit()
				continue
			elif type(error) == requests.exceptions.ConnectTimeout:
				print("Connection Timeout. Flagging as remedy and breaking the update.")
				sql = """ UPDATE pW SET remedy = 1 WHERE url = {0}""".format(str(url_for_sql))
				cursor.execute(sql)
				connection.commit()
				sql = """ UPDATE pW SET remedy_reason = "ConnectTimeout" WHERE url = {0}""".format(str(url_for_sql))
				cursor.execute(sql)
				connection.commit()
				continue
			elif type(error) == requests.exceptions.SSLError:
				print("SSL certificate is not verified. Flagging as remedy and breaking the update.")
				sql = """ UPDATE pW SET remedy = 1 WHERE url = {0}""".format(str(url_for_sql))
				cursor.execute(sql)
				connection.commit()
				sql = """ UPDATE pW SET remedy_reason = "SSLError" WHERE url = {0}""".format(str(url_for_sql))
				cursor.execute(sql)
				connection.commit()
				continue
			elif type(error) == requests.exceptions.ReadTimeout:
				print("Read timeout error. Flagging as remedy and breaking the update.")
				sql = """ UPDATE pW SET remedy = 1 WHERE url = {0}""".format(str(url_for_sql))
				cursor.execute(sql)
				connection.commit()
				sql = """ UPDATE pW SET remedy_reason = "ReadTimeout" WHERE url = {0}""".format(str(url_for_sql))
				cursor.execute(sql)
				connection.commit()
				continue
				# Flag as remedy. skip loop.


		# General updater. Delete uptime_cycles increment from here.

		if (IP != None):
			sql = """UPDATE pW SET IP = {0} WHERE url = {1}""".format("'"+str(IP)+"'", str(url_for_sql))
			cursor.execute(sql)
			connection.commit()
			print("Updated.")
		else:
			print("No IP for old men.")

		if (hashPhish != None):
			sql = """UPDATE pW SET contentHash = {0}, encoding_guess = {1} WHERE url = {2}""".format("'"+str(hashPhish)+"'","'"+str(encodingGuess)+"'" ,str(url_for_sql))
			cursor.execute(sql)
			connection.commit()
			print("Updated.")
		else:
			print("No hash for old men.")

		if (phish_status_code != None):
			sql = """UPDATE pW SET status_code = {0} WHERE url = {1}""".format(int(phish_status_code), str(url_for_sql))
			cursor.execute(sql)
			connection.commit()
			print("Updated.")
		else:
			print("No status code for old men.")

		# IMPORTANT NOTE ABOUT UPTIME CYCLES: if 16 uptime cycles, it means a minimum of 15 hours. It is a range, such as this (1,16 ].

		print("End of Loop.")

	print("Taking a nap for an hour.")
	time.sleep(3600)

