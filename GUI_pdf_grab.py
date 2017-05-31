 #    © Tanner Robart 2017

#    This file is part of Scrapy-McScrapeface. It is owned and licensed by Proplogix. Any use of this code must be explicitly negotiated with Proplogix.
#    Any use of this code must be explicitly negotiated with Proplogix.

#import scrapers
import pinellas_pdf_grab
import duval_pdf_grab
import sarasota_pdf_grab
import manatee_pdf_grab
import hillsborough_pdf_grab


import urllib
import urllib.request
import os
import sys
import re
import datetime

from pdfrw import PdfReader, PdfWriter
from easygui import *
from PyQt4.QtGui import *  
from PyQt4.QtCore import *  
from PyQt4.QtWebKit import *  
from lxml import html 





try:
	from bs4 import BeautifulSoup
except ImportError:
	print( "[*] Please download and install Beautiful Soup first!")
	sys.exit(0)

# Start of main run loop and GUI control flow
while 1:
	msgbox("Proplogix PDF Scraper V-0.2")
	msg ="Which Counties' PDFs do you wish to scrape today?"
	title = "PDF Scraper V0.1"
	county_choices = ["Manatee", "Sarasota", "Pinellas", "Hillsborough", "Duval"]
	county_choice = multchoicebox(msg, title, county_choices)
   

	msg = "Do you wish to perform an automatic update or define a manual date range?"
	title = "Automatic or Manual?"
	date_range_choices = ["Automatic", "Manual"]
	date_choice = choicebox(msg, title, date_range_choices)
	print(date_choice)
	if date_choice == "Manual": #show a manual/automatic choice dialog
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
		msgbox("Automatic date update under development")
		pass


	if 'Hillsborough' in county_choice:

		msgbox("Processing Hillsborough...")
		hillsborough_pdf_grab.hillsborough_scrape(begin_date, end_date)
		#clear this option from the county choice list
		county_choice.remove("Hillsborough")

	if 'Duval' in county_choice:
		msgbox("Processing Duval...")
		duval_pdf_grab.duval_scrape(begin_date, end_date)
		#clear this option from the county choice list
		county_choice.remove("Duval")
			
	if "Manatee" in county_choice:
		manatee_pdf_grab.manatee_scrape(begin_date, end_date)
		county_choice.remove("Manatee")

	if "Sarasota" in county_choice:
		msgbox("Processing Sarasota...")
		sarasota_pdf_grab.sarasota_scrape(begin_date, end_date)
		county_choice.remove("Sarasota")

	if "Pinellas" in county_choice:
		msgbox("Processing Pinellas...")
		pinellas_pdf_grab.pinellas_scrape(begin_date, end_date)
		
		#clear this option from the county choice list
		county_choice.remove("Pinellas")	
	msgbox("Scraping Completed!!")
	break
