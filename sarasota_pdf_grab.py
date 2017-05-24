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
 #    For more details, see <http://www.gnu.org/licenses/>.

import urllib
import urllib.request
import os
import sys
import datetime
import time
import mechanicalsoup
import sys  
import glob
from selenium import webdriver

from PyQt4.QtGui import *  
from PyQt4.QtCore import *  
from PyQt4.QtWebKit import *  
from lxml import html 
try:
        from bs4 import BeautifulSoup
except ImportError:
        print( "[*] Please download and install Beautiful Soup first!")
        sys.exit(0)
 

def tiny_file_rename(newname, folder_of_download):
        try:
            filename = max([f for f in glob.glob(os.path.join(folder_of_download, "null*"))], key=lambda xa :   os.path.getctime(os.path.join(folder_of_download,xa)))
            if 'null' in filename:
                try:
                    os.rename(os.path.join(folder_of_download, 'null.pdf'), os.path.join(folder_of_download, newname))
                except FileNotFoundError:
                    print("File Not Found")
                    pass
                except FileExistsError:
                    print("SKIPPED")
                    os.remove(filename)
            else:
                time.sleep(2)
                try:
                    os.rename(os.path.join(folder_of_download, 'null.pdf'), os.path.join(folder_of_download, newname))
                except FileNotFoundError:
                    print("File Not Found")
                    pass
                except FileExistsError:
                    print("SKIPPED 2")
                    os.remove(filename)
        except:
            print('failed rename, skipping')
            time.sleep(2)
            pass
        



def sarasota_scrape():


        # initializing variables

        landing_page = "https://clerkpublicrecords.scgov.net/RealEstate/SearchEntry.aspx"
        download_path = "C:/Users/trobart/Desktop/Deeds/scraped_pdfs/sarasota"
        last_instrument = ""
        i = 0

        date1 = input("Please input a start date (mm-dd-yyyy):")
        begin_date = datetime.datetime.strptime(date1, '%m-%d-%Y')
        date2 = input("Please input an end date (mm-dd-yyyy):")
        end_date = datetime.datetime.strptime(date2, '%m-%d-%Y')

        delta_date = end_date - begin_date
        os.chdir(download_path)


        ########## Selenium method for navigating through search query page ###########

        options = webdriver.ChromeOptions()

        options.add_experimental_option("prefs", {
        "plugins.plugins_list": [{"enabled":False,"name":"Chrome PDF Viewer"}],
        "download.default_directory" : download_path,
        "download.prompt_for_download": False,
        "plugins.always_open_pdf_externally": True,
        "download.open_pdf_in_system_reader": False
        })
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.binary_location = 'C:/Users/trobart/AppData/Local/Google/Chrome SxS/Application/chrome.exe'
        driver = webdriver.Chrome(executable_path=r'C:/Users/trobart/Downloads/chromedriver.exe' , chrome_options = options)
        driver.get(landing_page)

        date_from = driver.find_element_by_xpath("//*[@id='x:2002578730.0:mkr:3']")
        date_from.send_keys(begin_date.strftime("%m/%d/%Y"))
        date_to = driver.find_element_by_xpath("//*[@id='x:625521537.0:mkr:3']")
        date_to.send_keys(end_date.strftime("%m/%d/%Y"))
        deed_button = driver.find_element_by_xpath("//*[@id='ctl00_cphNoMargin_f_dclDocType_67']")
        deed_button.click()
        search = driver.find_element_by_xpath("//*[@id='ctl00_cphNoMargin_SearchButtons2_btnSearch']")
        search.click()


        try:    
            #now that we've landed past the captcha, and have a valid session, move to the search query
            driver.get(url)
            
            html = driver.page_source #grabbing html from selenium driver
            soup = BeautifulSoup(html, "lxml") # using beautifulsoup to parse the website html

            

            # Iterate over the records table on each page
            if table.findAll('tr')[1:]:
                for row in table.findAll('tr')[1:]:
                    instrument = row.findAll('td')[-1].text
                    j = int(row.td.text)

                    for tag in row.findAll('a', href=True): #find <a> tags with href in it so you know it is for urls
                                                             #so that if it doesn't contain the full url itself to it for the download
                            if "NewWindowInit" in tag['href'] and instrument != last_instrument:

                                    
                                    driver.find_element_by_xpath("//*[@id='tableA']/tbody/tr[{0}]/td[2]/a[3]".format(j)).click()
                                    
                                    #close tab 
                                    time.sleep(1)
                                    driver.switch_to_window(driver.window_handles[1])
                                    driver.close()
                                    driver.switch_to_window(driver.window_handles[0]) # switch back to main page

                                    print( "\n[*] Downloading: #{2} - {0} - row {1}".format(instrument, j, i))

                                    tiny_file_rename( "pinellas" + "_" + instrument + ".pdf", download_path) # rename from null to correct name
                                    last_instrument = instrument 
                                    i+=1
            else:
                pass

                    
                    print( "\n[*] Downloaded %d files" %(i+1))
                    
           
        except KeyboardInterrupt:
            print( "[*] Exiting...")
            sys.exit(1)
         
        except urllib.error.URLError as e:
            print( "[*] Could not get information from server!!")
            sys.exit(2)
        except TypeError:
            pass
        except AttributeError:
            # This is to handle any search result has no records for that day (like on weekends or holidays)
            pass

        except FileNotFoundError:
            print("File Not Found!", instrument)
            pass
        except IndexError as e:
            print('index error!', e, sys.stderr)
            pass
        except:
            print("Unexpected error:", sys.stderr, sys.exc_info())
            pass

if __name__ == '__main__':
    sarasota_scrape()