import MechanicalSoup
import urllib
import urllib.request
import os
import sys
import re
import requests
import pprint
import datetime
from http.cookiejar import CookieJar
from pdfrw import PdfReader, PdfWriter
from easygui import *

try:
	from bs4 import BeautifulSoup
except ImportError:
	print( "[*] Please download and install Beautiful Soup first!")
	sys.exit(0)

begin_date = datetime.datetime.strptime("09-05-2016", '%m-%d-%Y')
end_date = datetime.datetime.strptime("03-20-2017", '%m-%d-%Y')

download_path = "C:/Users/trobart/Desktop/Deeds/scraped_pdfs/hillsborough/"
prev_id = ''



delta_date = end_date - begin_date



for i in range(delta_date.days + 1):

	# grabbing a new url query for each day
	temp_day = begin_date + datetime.timedelta(days=i)
	temp_day_plus = begin_date + datetime.timedelta(days=i+1)
	url = "http://pubrec3.hillsclerk.com/oncore/search.aspx?bd={0}&ed={1}&bt=O&cfn=2017075349&pt=-1&dt=D%2C%20TAXDEED&st=documenttype".format(temp_day.strftime("%m/%d/%y"), temp_day_plus.strftime("%m/%d/%y"))


	try:
		#landing_page = browser.get(URL)

		# to make it look like a legit user agent for the url request
		headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0"}
	 
		i = 0
		request = urllib.request.Request(url, None, headers)
		request.add_header("cookie", "OnCoreWeb=DefaultNumberOfRows=500") # ensuring that the maximum number of links appears per page
		html = urllib.request.urlopen(request)
		soup = BeautifulSoup(html.read(), 'lxml') # to parse the website

		for tag in soup.findAll('a', href=True): # find <a> tags with href in it so you know it is for urls
												# so that if it doesn't contain the full url it can the url itself to it for the download
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
				f.write(download.read()) # raw data of response written to file
				
				# code to extract only the first page
				infile = PdfReader(download_path + "hillsborough_" + id_num + ".pdf")
				for i, p in enumerate(infile.pages):
					if i == 0:
							PdfWriter().addpage(p).write(download_path + "hillsborough" + "_" + id_num + "_" + temp_day.isoformat() + ".pdf")
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
		print(getwithit)
		print( "I don't know the problem, sorry!! skipping file...")
		pass
	html.close()