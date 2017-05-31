 #    © Tanner Robart 2017

#    This file is part of Scrapy-McScrapeface. It is owned and licensed by Proplogix. Any use of this code must be explicitly negotiated with Proplogix.
#    Any use of this code must be explicitly negotiated with Proplogix.

import urllib
import urllib.request
import os
import sys
import datetime 
from easygui import *


try:
        from bs4 import BeautifulSoup
except ImportError:
        print( "[*] Please download and install Beautiful Soup first!")
        sys.exit(0)
 


def manatee_scrape(begin_date = "", end_date = ""):

    if begin_date == "":

        date1 = input("Please input a start date (mm-dd-yyy):")
        begin_date = datetime.datetime.strptime(date1, '%m-%d-%Y')
        date2 = input("Please input an end date (mm-dd-yyy):")
        end_date = datetime.datetime.strptime(date2, '%m-%d-%Y')



    url = "https://records.manateeclerk.com/OfficialRecords/Search/InstrumentType/11/{0}/{1}/1/10000".format(begin_date.date().isoformat(), end_date.date().isoformat())
    download_path = "C:/Users/trobart/Desktop/Deeds/scraped_pdfs/manatee/"

    try:
            #to make it look legit for the url
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0"}
     
            i = 0
     
            request = urllib.request.Request(url, None, headers)
            html = urllib.request.urlopen(request)
            soup = BeautifulSoup(html.read(), "lxml") #to parse the website
     
            for tag in soup.findAll('a', href=True): #find <a> tags with href in it so you know it is for urls
                    #so that if it doesn't contain the full url it can the url itself to it for the download

                    tag['href'] = urllib.request.urljoin('https://records.manateeclerk.com', tag['href'])

                    if "DisplayInstrument" in tag['href']:
                            current = urllib.request.urlopen("https://records.manateeclerk.com/OfficialRecords/DisplayInstrument/InstrumentResultFile/" + os.path.basename(tag['href']) + '/1')
                            print(current)
                            print( "\n[*] Downloading: %s" %(os.path.basename(tag['href'])))
     
                            f = open(download_path + 'manatee_' + os.path.basename(tag['href']) + date1.date().isoformat() + '--' + date1.date().isoformat() + '.pdf', "wb")
                            f.write(current.read())
                            f.close()
                            i+=1
     
            print( "\n[*] Downloaded %d files" %(i+1))
            input("[+] Press any key to exit...")
     
    except KeyboardInterrupt:
            print( "[*] Exiting...")
            sys.exit(1)
     
    except urllib.error.URLError as e:
            print( "[*] Could not get information from server!!")
            sys.exit(2)
     
    except:
            print( "I don't know the problem but sorry!!")
            sys.exit(3)