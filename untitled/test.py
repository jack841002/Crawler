"""
#爬蟲 (PTT表特版)

#抓取網頁原始碼
import requests

requests.get("https://www.ptt.cc/bbs/beauty/index.html")
res = requests.get("https://www.ptt.cc/bbs/beauty/index.html")
print(res.text)

#操作HTML
from bs4 import BeautifulSoup
soup = BeautifulSoup(res.text,"html.parser")

tag_name = "div.title a" #拿到所有文章的網址
articles = soup.select(tag_name)

#拿網址和標題
for art in articles:
    print(art["href"], art.text)

paging = soup.select("div.btn-group-paging a")

"""

import requests
from bs4 import BeautifulSoup
import re #抓圖片
from urllib.request import urlretrieve #存照片
import os #為了建立資料夾
import sys #控制抓取文章頁數 system的縮寫
import pymysql #建立資料庫

db = pymysql.connect(host='localhost', port=3306, password='841002', user='jack', db='pttpicture', charset='utf8')
cursor=db.cursor()

if not os.path.isdir("download"): #建立資料夾
    os.mkdir("download")

url = "https://www.ptt.cc/bbs/beauty/index.html"
reg_imgur_file = re.compile("http[s]?://i.imgur.com/\w+\.(?:jpg|png|gif)")
#print(sys.argv)

pages = 3

for round in range(pages):

    res = requests.get(url)
    soup = BeautifulSoup(res.text,"html.parser")
    articles = soup.select("div.title a")
    paging = soup.select("div.btn-group-paging a")
    next_url = "https://www.ptt.cc" + paging[1]["href"]
    url = next_url

    for article in articles:
        print(article["href"], article.text)
        if not os.path.isdir(os.path.join("download", article.text)): #建立每個文章的資料夾
            os.mkdir(os.path.join("download", article.text))

        res = requests.get("https://www.ptt.cc" + article["href"])  #存取網址
        images = reg_imgur_file.findall(res.text) #找出所有圖片的網址
        print(images)
        for image in set(images):
            ID = re.search("http[s]?://i.imgur.com/(\w+\.(?:jpg|png|gif))", image).group(1) #找出圖片的後半段亂碼網址
            #urlretrieve(image, ID) #(網址,檔案名稱)
            urlretrieve( image, os.path.join("download", article.text, ID) )

            sql = "INSERT INTO picture(name, pic) VALUES ('%s', '%s')" #存入資料庫
            try:
                cursor.execute(sql % (ID, image))
                db.commit()

            except:
                db.rollback()


db.close()














