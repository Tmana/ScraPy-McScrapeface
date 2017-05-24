 #    © Tanner Robart 2017

 #    This file is part of Scrapy-McScrapeface.

 #    Scrapy-McScrapeface is free software: you can redistribute it and/or modify
 #    it under the terms of the GNU General Public License as published by
 #    the Free Software Foundation, either version 3 of the License, or
 #    (at your option) any later version.

 #    Scrapy-McScrapeface is distributed in the hope that it will be useful,
 #    but WITHOUT ANY WARRANTY; without even the implied warranty of
 #    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 #    GNU General Public License for more details.

 #    You should have received a copy of the GNU General Public License
 #    along with Scrapy-McScrapeface.  If not, see <http://www.gnu.org/licenses/>.


import urllib
import urllib.request
import os
import sys
import re
import requests
import pprint
import datetime
from http.cookiejar import CookieJar
from easygui import *



try:
	from bs4 import BeautifulSoup
except ImportError:
	print( "[*] Please download and install Beautiful Soup first!")
	sys.exit(0)

 
while 1:
	msgbox("Proplogix PDF Scraper V0.1")
	msg ="Which Counties' PDFs do you wish to scrape today?"
	title = "PDF Scraper V0.1"
	county_choices = ["Manatee", "Sarasota", "Pinellas", "Hillsborough"]
	county_choice = multchoicebox(msg, title, county_choices)
   

	msg = "Do you wish to perform an automatic update or define a manual date range?"
	title = "Automatic or Manual?"
	date_range_choices = ["Automatic", "Manual"]
    	if choicebox(msg, title, date_range_choices) == 'Manual':     # show a manual/automatic choice dialog
		msg = "Define a Date range to scrape"
		title = "PropLogix PDF Scraper"
		fieldNames = ["Please input a start date (mm-dd-yyy):", "Please input an end date (mm-dd-yyy):"]
		fieldValues = []
		fieldValues = multenterbox(msg, title, fieldNames)
		while 1:
			if fieldValues == None: break
			errmsg = ""
			for i in range(len(fieldNames)):
				if fieldValues[i].strip() == "":
					errmsg = errmsg + ('"%s" is a required field.\n\n' % fieldNames[i])
			if errmsg == "": break # no problems found
			fieldValues = multenterbox(errmsg, title, fieldNames, fieldValues)

		begin_date = datetime.datetime.strptime(fieldValues[0], '%m-%d-%Y')
		end_date = datetime.datetime.strptime(fieldValues[1], '%m-%d-%Y')
	    else:
		msgbox("Automatic update under development")
		pass
	if 'Hillsborough' in county_choice:
		msgbox("Processing Hillsborough...")
		download_path = "C:/Users/trobart/Desktop/Deeds/scraped_pdfs/hillsborough/"
		prev_id = ''



		delta_date = end_date - begin_date


		for i in range(delta_date.days + 1):
			temp_day = begin_date + datetime.timedelta(days=i)
			temp_day_plus = begin_date + datetime.timedelta(days=i+1)
			url = "http://pubrec3.hillsclerk.com/oncore/search.aspx?bd={0}&ed={1}&bt=O&cfn=2017075349&pt=-1&dt=D%2C%20TAXDEED&st=documenttype".format(temp_day.strftime("%m/%d/%y"), temp_day_plus.strftime("%m/%d/%y"))


			try:
				#to make it look like a legit user agent for the url request
				headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0"}
			 
				i = 0
			 
				request = urllib.request.Request(url, None, headers)
				request.add_header("cookie", "OnCoreWeb=DefaultNumberOfRows=500") #ensuring that the maximum number of links appears per page
				html = urllib.request.urlopen(request)
				soup = BeautifulSoup(html.read(), 'lxml') #to parse the website

				for tag in soup.findAll('a', href=True): #find <a> tags with href in it so you know it is for urls

					#so that if it doesn't contain the full url it can the url itself to it for the download
					href = str(tag['href'])

					if "id=" in href and href.split("id=")[1].split("&")[0] != prev_id:
						id_num = href.split("id=")[1].split("&")[0]
						
						request = urllib.request.Request("http://pubrec3.hillsclerk.com/oncore/ImageBrowser/default.aspx?id=" + id_num, None, headers)
						url1 = urllib.request.urlopen(request)
						cookie = url1.headers.get('Set-Cookie')

						request2 = urllib.request.Request("http://pubrec3.hillsclerk.com/oncore/ImageBrowser/ShowPDF.aspx",  None, headers)
						request2.add_header('cookie', cookie)
						request2.add_header('Connection', 'keep-alive')
						download = urllib.request.urlopen(request2)

						
						print( "\n[*] Downloading: %s" %id_num)
						prev_id = id_num
			 
						f = open(download_path + "hillsborough_" + id_num + ".pdf", "wb")
						f.write(download.read()) # if chunking, change to 'data'
						f.close()
						i+=1
			 
				print( "\n[*] Downloaded %d files" %(i+1))
					 
			except KeyboardInterrupt:
				print( "[*] Exiting...")
				sys.exit(1)
			 
			except urllib.error.URLError as e:
				print(e.reason)
				print( "[*] Could not get information from server!!")
				sys.exit(2)
			 
			except:
				e = sys.exc_info()[0]
				print(e)
				print( "I don't know the problem, sorry!! skipping file...")
				pass
			html.close()
		county_choice.remove("Hillsborough")
	if "Manatee" in county_choice:
		url = "https://records.manateeclerk.com/OfficialRecords/Search/InstrumentType/11/{0}/{1}/1/10000".format(date1.date().isoformat(), date2.date().isoformat())
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
		county_choice.remove("Manatee")
	if "Sarasota" in county_choice:
		msgbox("Sarasota scraper still under development")
		pass
	if "Pinellas" in county_choice:
		msgbox("Pinellas scraper still under development")	
	msgbox("Scraping Completed!!")
	break
