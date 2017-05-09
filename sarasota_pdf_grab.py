import urllib
import urllib.request
import os
import sys
import re
import requests
import pprint

from http.cookiejar import CookieJar



try:
        from bs4 import BeautifulSoup
except ImportError:
        print( "[*] Please download and install Beautiful Soup first!")
        sys.exit(0)


date1 = input("Please input a start date (mm-dd-yyy):")
date1 = datetime.datetime.strptime(date1, '%m-%d-%Y')
date2 = input("Please input an end date (mm-dd-yyy):")
date2 = datetime.datetime.strptime(date2, '%m-%d-%Y')


url = "https://clerkpublicrecords.scgov.net/RealEstate/SearchResults.aspx?ctl00_cphNoMargin_f_ddcDateFiledFrom_clientState=%7C0%7C012017-2-8-0-0-0-0%7C%7C"
download_path = "C:/Users/trobart/Desktop/Deeds/output/sarasota/"
prev_id = ''

try:
        #to make it look like a legit user agent for the url request
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0"}
 
        i = 0
 
        request = urllib.request.Request(url, None, headers)
        html = urllib.request.urlopen(request)
        soup = BeautifulSoup(html.read(), "lxml") #to parse the website
 
        for tag in soup.findAll('a', href=True): #find <a> tags with href in it so you know it is for urls
                #so that if it doesn't contain the full url it can the url itself to it for the download
                href = str(tag['href'])

                if "id=" in href and href.split("id=")[1].split("&")[0] != prev_id:
                        id_num = href.split("id=")[1].split("&")[0]

                        request2 = urllib.request.Request("http://clerkpublicrecords.scgov.net/RealEstate/SearchImage.aspx?global_id=" + id_num + '&type=pdf',  None, headers)
                        download = urllib.request.urlopen(request2)

                        
                        print( "\n[*] Downloading: %s" %id_num)
                        prev_id = id_num
                        #print(download.end())
 
                        f = open(download_path + "sarasota_" + id_num +".pdf", "wb")
                        f.write(download.read()) # if chunking, change to 'data'
                        f.close()
                        i+=1
 
        print( "\n[*] Downloaded %d files" %(i+1))
        input("[+] Press any key to exit...")
 
except KeyboardInterrupt:
        print( "[*] Exiting...")
        sys.exit(1)
 
except urllib.error.URLError as e:
        print(e.reason)
        print( "[*] Could not get information from server!!")
        sys.exit(2)
 
except:
        print( "I don't know the problem, sorry!!")
        sys.exit(3)