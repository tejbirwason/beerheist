# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import pymongo
from pymongo import MongoClient
from scrapy.spider import Spider
from bs4 import BeautifulSoup
import re


class BeerRunSpider(Spider):
    name = "beerrun"
    allowed_domains = ["thebeerstore.ca"]
    start_urls = [
        "http://www.thebeerstore.ca/beers/inventory/154/2371"
    ]

    def parse(self, response):
        soup = BeautifulSoup(response.body)        
        a=[]
        b=[]
        c=[]
        d=[]
        for size in soup.find_all("td","size"):
            text = size.get_text()
            c.append(text)
            m = re.findall(r'\d+',text)
            a.append(int(m[0])*int(m[1]))
        for price in soup.find_all("td","price"):
            price = price.get_text().strip('$')
            if price.find("sale")==-1:
                b.append(float(price))
            else:
                b.append(float(price.split('$')[1]))
        for inventory in soup.find_all("td","inventory"):
            d.append(int(inventory.get_text()))
        
        
        e=[]
        
        assert len(a) == len(b) == len(c)
        

        for i in range(len(a)):
                if d[i]==0:
                    e.append(0)
                else:
                    e.append(a[i]/b[i])
                    
        #maxIndex = e.index(max(e))
        
        print "Get"
        print c[maxIndex]
        print "at a price of"
        print b[maxIndex]
        print "for"
        print e[maxIndex]
        print "ml alcohol/$"
        
        client = MongoClient()
        db = client.mydb
        collection = client.beer
        
        beer = { "list": c }
        
        db.collection.insert(beer)
        
        print beer
        
        for item in c:
            
            print item
        print e
            
            
            
            