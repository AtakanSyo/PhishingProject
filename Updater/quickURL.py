import socket
import pymysql
import requests
import time
import codecs
from bs4 import UnicodeDammit

url = 'http://amcgardiennage.com/p2w9yszpptjiofu4tjjtmdq5ea=='

codec_array = ['utf-8','latin_1']

r = requests.get(url)

dammit = UnicodeDammit(r.content)

print(dammit.original_encoding)

print(dammit.unicode_markup)

	
