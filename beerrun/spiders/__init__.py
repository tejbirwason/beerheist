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
        #"http://www.thebeerstore.ca/beers/inventory/574/4004"
    ]


    def parse(self, response):
        soup = BeautifulSoup(response.body)  

        ## mongo stuff
        client = MongoClient()
        db = client.mydb
        beerrun = client.beerrun


        for storelink in soup.find_all("a","store-link"):
            extractStoreName = storelink.get_text() 
            extractID = re.findall(r'\d+',str(re.findall(r'# \d+',str(storelink.parent()))))[0]
            if (extractID=="4616"): #will be removed later
                showcaseURL = "http://www.thebeerstore.ca/sites/all/modules/custom/tbs_api/modules/tbs_api_stores/json.php?store_id="+extractID
                soup = BeautifulSoup((requests.get(showcaseURL)).text)
                for link in soup.find_all("a","brand-link teaser"):
                    beerinventoryURL = "http://www.thebeerstore.ca"+link.get('href')
                    imageURL = (link.find_all("img","image-style-none")[0]).get('src')
                    beername = (link.find("span","brand-name")).get_text()
                    print beername
                    soup2 = BeautifulSoup((requests.get(beerinventoryURL)).text)  
                    for row in soup2.find_all("tr",["odd","even"]):
                        size = (row.find("td","size")).get_text()
                        price = (row.find("td","price")).get_text()
                        inventory = (row.find("td","inventory")).get_text()
                        temp = re.findall(r'\d+',size)
                        quantity = int(temp[0])*int(temp[1])
                        temp2 = price.strip('$')
                        if temp2.find("sale")==-1:
                            strippedPrice = (float(temp2))
                            onSale = 0
                        else:
                            strippedPrice = (float(temp2.split('$')[1]))
                            onSale = 1
                        if inventory == "0":
                            apd = 0
                        else:
                            apd = quantity/strippedPrice

                        beer = { "store_name": extractStoreName,
                            "store_id": extractID,
                            "showcase_url":showcaseURL,
                            "beer_invetory_url": beerinventoryURL,
                            "brand_image_url": imageURL,
                            "beer_name": beername,
                            "size": size,
                            "volume": quantity,
                            "price": strippedPrice,
                            "inventory":inventory,
                            "onSale":onSale,
                            "apd":apd}
                        db.beerrun.insert(beer)