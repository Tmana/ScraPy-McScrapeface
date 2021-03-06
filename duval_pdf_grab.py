
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


def duval_scrape(begin_date = "", end_date = ""):

	if begin_date == "":
	    date1 = input("Please input a start date (mm-dd-yyyy):")
	    begin_date = datetime.datetime.strptime(date1, '%m-%d-%Y')
	    date2 = input("Please input an end date (mm-dd-yyyy):")
	    end_date = datetime.datetime.strptime(date2, '%m-%d-%Y')
	
	delta_date = end_date - begin_date

	download_path = "C:/Users/trobart/Desktop/Deeds/scraped_pdfs/duval/{0}/".format(datetime.datetime.today().date().isoformat())
	if not os.path.exists(os.path.dirname(download_path)):
		os.makedirs(os.path.dirname(download_path))
	os.chdir(download_path)
	prev_id = ''


	for i in range(delta_date.days + 1):

		#grabbing a new url query for each day
		temp_day = begin_date + datetime.timedelta(days=i)
		temp_day_plus = begin_date + datetime.timedelta(days=i+1)

		try:
			url = "http://oncore.duvalclerk.com/search.aspx?bd={0}&ed={1}&bt=OR&d=5%2F1%2F2017&pt=-1&dt=DEED&st=documenttype".format(temp_day.strftime("%m/%d/%y"), temp_day.strftime("%m/%d/%y"))
			#to make it look like a legit user agent for the url request
			headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0"}
		 	
			i = 0
			request = urllib.request.Request(url, None, headers)
			request.add_header("cookie", "OnCoreWeb=DefaultNumberOfRows=500") #ensuring that the maximum number of links appears per page
			html = urllib.request.urlopen(request)
			s = requests.Session()
			soup = BeautifulSoup(html.read(), 'lxml') #to parse the website

			for tag in soup.findAll('a', href=True): #find <a> tags with href in it so you know it is for urls

				#so that if it doesn't contain the full url it can the url itself to it for the download
				href = str(tag['href'])

				if "id=" in href and href.split("id=")[1].split("&")[0] != prev_id:
					id_num = href.split("id=")[1].split("&")[0]
					download = s.get("http://oncore.duvalclerk.com/ImageBrowser/image.aspx?ImageId={}&png=-1".format(id_num))
		
					print( "\n[*] #: %s Downloading: %s   Date: %s" %(i, id_num, temp_day.date().isoformat()))
					prev_id = id_num
					
					f = open(download_path + "duval_" + id_num + ".pdf", "wb")
					f.write(download.content) # raw data of response written to file
					f.close()
					
					# code to extract only the first page and replace the original with one page version
					# infile = PdfReader(download_path + "duval_" + id_num + ".pdf")
					# for i, p in enumerate(infile.pages):
					# 	if i == 0:
					# 			PdfWriter().addpage(p).write(download_path + "duval_" + temp_day.date().isoformat() + "_" + id_num + ".pdf")

					# os.remove(download_path + "duval_" + id_num + ".pdf") #removng original pdf
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


if __name__ == '__main__':
    duval_scrape()
