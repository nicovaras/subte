#!/usr/bin/env python
import requests
from BeautifulSoup import BeautifulSoup

text = requests.get('http://www.metrovias.com.ar').text
b = BeautifulSoup(text)
res = ""
for line in "ABCDEH":
    text = b.find(id=("status-line-%s" % line)).text
    if text == 'Normal' or 'habitual' in text:
        res += "\033[42m"
    elif "emora" in text or "obras" in text:
        res += "\033[43m"
    else:
        res += "\033[41m"
    res += "\033[1m|" + line + "|\033[0m "
print res
