import mysql.connector
from mysql.connector.constants import ClientFlag

config = {
    'user': 'root',
    'password': '',
    'host': '34.134.226.251',
    'client_flags': [ClientFlag.SSL],
    'ssl_ca': 'ssl/server-ca.pem',
    'ssl_cert': 'ssl/client-cert.pem',
    'ssl_key': 'ssl/client-key.pem'
}

config['database'] = 'phishingdb'  # add new database to config dict

cnxn = mysql.connector.connect(**config)

print(cnxn)

cursor = cnxn.cursor()

try:
	cursor.execute("DELETE FROM phishingwebsites")
except Exception as error:
	print(error)
	print(error.__class__.__name__)