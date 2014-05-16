# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import pymongo
from pymongo import MongoClient
from scrapy.spider import Spider
from scrapy.spider import Request
from bs4 import BeautifulSoup
import re
import requests


class BeerRunSpider(Spider):
    name = "beerrun"
    allowed_domains = ["thebeerstore.ca"]
    start_urls = [
        "http://www.thebeerstore.ca/stores"
    ]


    def parse(self, response):
        soup = BeautifulSoup(response.body)  
        store_name=[]
        store_id=[]

        ## mongo stuff
        client = MongoClient()
        db = client.mydb
        beerrun = client.beerrun


        for link in soup.find_all("a","store-link"):
            extractStoreName = link.get_text() 
            store_name.append(extractStoreName)
            extractID = re.findall(r'\d+',str(re.findall(r'# \d+',str(link.parent()))))[0]
            store_id.append(extractID)
            
            #print beer
            showcaseURL = "http://www.thebeerstore.ca/sites/all/modules/custom/tbs_api/modules/tbs_api_stores/json.php?store_id="+extractID
            soup = BeautifulSoup((requests.get(showcaseURL)).text)
            count = 0
            for link in soup.find_all("a","brand-link teaser"):
                beerinventoryURL = "http://www.thebeerstore.ca"+link.get('href')
                imageURL = (link.find_all("img","image-style-none")[0]).get('src')
                #print(link.get('href'))
                beer = { "store_name": extractStoreName,
                    "store_id": extractID,
                    "showcase_url":showcaseURL,
                    "beer_invetory_url": beerinventoryURL
                    "brand_image_url": imageURL}
                #db.beerrun.insert(beer)
            #print re.findall(r'\d+',str(re.findall(r'# \d+',str(link.parent()))))[0]

        #print db.collection.find()
        #break
        #print store_name
        #print store_id

        #for storeIdAppendLink in store_id:
            #beerlist = []
           # returned = requests.get("http://www.thebeerstore.ca/sites/all/modules/custom/tbs_api/modules/tbs_api_stores/json.php?store_id="+str(storeIdAppendLink))
          #  soup = BeautifulSoup(returned.text)
            #for link in soup.find_all("a","brand-link teaser"):
                #print(link.get('href'))



    def here(self, response):
        print "here"

        #r = requests.get("http://www.thebeerstore.ca/sites/all/modules/custom/tbs_api/modules/tbs_api_stores/json.php?store_id=4607")
        #print(r.text)
        #print(r.status_code)
        #soup.find_all('a',)

        #tryin = Request(url="http://www.thebeerstore.ca/sites/all/modules/custom/tbs_api/modules/tbs_api_stores/json.php?store_id=4607",
                              # cookies={'currency': 'USD', 'country': 'UY'})
        #print(soup.prettify())

    def parse2(self, response):
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
                    
        maxIndex = e.index(max(e))
        
        print "\n"
        print "Get"
        print c[maxIndex]
        print "at a price of"
        print b[maxIndex]
        print "for"
        print e[maxIndex]
        print "ml alcohol/$"
        print "\n"
        
        
        for item in c:
            print item
        print e
            
            
            
            