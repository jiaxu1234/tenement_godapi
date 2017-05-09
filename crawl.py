#-*- coding:utf-8 -*-
from bs4 import BeautifulSoup
from urlparse import urljoin
import requests
import csv
from lxml import etree
import re

url = "http://bj.58.com/pinpaigongyu/pn/{page}/?minprice=1000_4000"


#已完成的页数序号，初时为0
page = 0

csv_file = open("rent.csv","wb")
csv_writer = csv.writer(csv_file, delimiter=',')

while True:
    page += 1
    print "fetch: ", url.format(page=page)
    response = requests.get(url.format(page=page))
    response = requests.get(url)
    html = BeautifulSoup(response.text)
    house_list = html.select(".list > li")
    if not house_list:
        break
    if page == 2:
        break

    for house in house_list:
        house_title = house.select("h2")[0].string.encode("utf8")
        house_url = urljoin(url, house.select("a")[0]["href"])
        house_info_list = house_title.split()

        # 如果第二列是公寓名则取第一列作为地址
        if "公寓" in house_info_list[1] or "青年社区" in house_info_list[1]:
            house_location = house_info_list[0]
        else:
            house_location = house_info_list[1]

        house_money = house.select(".money")[0].select("b")[0].string.encode("utf8")
        house_title = house_title.decode('utf-8')
        house_location = house_location.decode('utf-8')

        try:
            response = requests.get(house_url)
            content = response.content
            tree = etree.HTML(content)
            lon = re.search("json4fe.lon = '(.*?)'",content)
            lat = re.search("json4fe.lat = '(.*?)'", content)
            if lon:
                lon = lon.group(1)
            if lat:
                lat = lat.group(1)
        except:
            pass

        print 'house_title', house_title
        print 'house_location', house_location
        print 'house_money', house_money
        print 'house_url', house_url
        print 'lon', lon
        print 'lat', lat

        csv_writer.writerow([house_title.encode("utf8"), house_location.encode("utf8"), house_money, house_url,lon,lat])

csv_file.close()