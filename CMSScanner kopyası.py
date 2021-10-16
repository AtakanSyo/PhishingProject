from Wappalyzer import WebPage
from Wappalyzer import Wappalyzer
import requests
import time
import mysql.connector
from mysql.connector.constants import ClientFlag
import pymysql


url_x = "http://kon2-26-11.svserv.net/Mozi.m"


try:
	data  = WebPage(url_x).info()
	print(data)
except Exception as fnf_error:
	print(fnf_error)
	print(fnf_error.__class__.__name__)