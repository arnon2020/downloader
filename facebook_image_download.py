#Facebook Web scapping program(image download)

#DOC
#urllib request library
#https://docs.python.org/3/library/urllib.request.html

#cookie jar
#https://docs.python.org/3/library/http.cookiejar.html

#References:https://www.mycodingzone.net/videos/hindi/web-scraping-hindi-6

from http.cookiejar import MozillaCookieJar #pip install cookiejar
import requests  #pip install requests
import bs4       #pip install beautifulsoup4
import uuid      #ไลบารี่รันชุดข้อความ
from urllib.request import urlopen, Request,install_opener,build_opener,HTTPCookieProcessor
import urllib.request
import re #ไลบารี่เกี่ยวกับข้อความ หรือตัวหนังสือ
import time
from datetime import datetime

#เทียบลิงค์ซ้ำ
def LinkCompare(data,link):
	repetitive = False
	for i in data:
		if i == link:
			repetitive = True
			break
	return repetitive
NewLogin = True  #New Login or use cookie login
email    = "Username"
password = "password"
REQUEST_HEADER     = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}

#cookie file name 
cookieFileName     = './cookieFile.txt'

#image link page in mbasic facebook
url = "mbasicfacebook"

if NewLogin:
    authentication_url = "https://mbasic.facebook.com/login.php" #mbasic facebook url
    payload        = {'email':email,'pass':password}      #Username and password
    cj             = MozillaCookieJar(cookieFileName)            #subclasses and co-operation with web browsers
    opener         = build_opener(HTTPCookieProcessor(cj))       #Return an OpenerDirector instance
    install_opener(opener)                                       #Install an OpenerDirector instance as the default global opener
    data           = urllib.parse.urlencode(payload).encode('utf-8')  #สำหรับใช้ทำ parsing URL
    req            = Request(authentication_url, data)           #สำหรับใช้เปิดลิงค์และ request
    resp           = urlopen(req)						         #Open the URL url
    cj.save(ignore_discard=True, ignore_expires=True)            #save cookie
else:
	cj             = MozillaCookieJar()
	cj.load(cookieFileName, ignore_discard=True, ignore_expires=True)


index = 1
state = True
links = []
while state:
    state = False
    try:
        data = requests.get(url, cookies=cj)
        soup = bs4.BeautifulSoup(data.text, 'html.parser')
        for i in soup.find_all('a', href=True):
            if i['href'][0:16] == "/photo.php?fbid=":
                text    = i['href'].split("&")
                text[0] = text[0].split("?")[1]
                link    = "https://www.facebook.com/photo.php?%s&%s&type=3&theater" %(text[0],text[2])
                if LinkCompare(links,link):
                	continue
                links.append(link)
                print('Page : %d'%(index))
                index += 1
                
                try:
                    print('1.Get Link:'+link)
                    data_f    = requests.get(link, cookies=cj)
                    soup_f    = bs4.BeautifulSoup(data_f.text, 'html.parser')
                    soup_f    = str(soup_f)
                    print('2.Find link image in page')
                    timestamp = re.findall('data-utime="(\d\d\d\d\d\d\d\d\d\d)"',soup_f)[0]
                    #print(timestamp)
                    date = str(datetime.fromtimestamp(int(timestamp)))
                    date =  date.replace('-','')
                    date =  date.replace(' ','_')
                    date =  date.replace(':','')
                    #print(date)
                    image_link = re.findall('data-ploi="((http)s?://.*?)" class=',soup_f)[0][0]
                    print('3.Filter link')
                    if len(image_link)>300:
                    	image_link = str(image_link.split()[0])
                    	image_link =  image_link.replace('"','')
                    	print('traget[0]>300')

                    image_link = image_link.replace("&amp", "&")
                    image_link = image_link.replace(';','')

                    print('4.Download:'+image_link)
                    try:
                        image  = urlopen(Request(image_link, headers=REQUEST_HEADER)).read()
                        path  =  './images/'+ date + ".jpg"
                        with open(path, 'wb') as file:
                        	file.write(image)
                    except e:
                    	print('image download error')

                    print('---------------------------------------------------------------------')
                except:
                    print('get facebook page error')
            
        if i.text.lower() == "ดูรูปภาพเพิ่ม":
            url   = "https://mbasic.facebook.com" +i['href']
            state = True
    except:
        print('get mbasic.facebook.com error')