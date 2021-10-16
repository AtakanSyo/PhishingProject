import requests

url_openphish = "http://95.179.203.220:80"
req = requests.get(url_openphish)
html = req.content

html = html.decode('utf-8')
print(html)