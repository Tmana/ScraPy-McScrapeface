 #    © Tanner Robart 2017

#    This file is part of Scrapy-McScrapeface. It is owned and licensed by Proplogix. 
#    Any use of this code must be explicitly negotiated with Proplogix.


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



def sarasota_scrape(begin_date = "", end_date = ""):


        # initializing variables

        landing_page = "https://clerkpublicrecords.scgov.net/RealEstate/SearchEntry.aspx"
        download_path = "C:/Users/trobart/Desktop/Deeds/scraped_pdfs/sarasota"
        last_instrument = ""
        i = 1

        if begin_date == "":
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

        #options.add_argument('--headless')
        #options.add_argument('--disable-gpu')
        options.add_argument("window-size=1024,900")
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
                while 1:
                

                        #now that we've landed past the landing page, and have a valid session, move through the search query and download pdfs
                        driver.get("https://clerkpublicrecords.scgov.net/RealEstate/SearchResults.aspx?pg={}".format(i))
                        print("page: ", i)
                        first_image = driver.find_element_by_xpath("//*[@id='x:1533160306.14:adr:0:tag::chlGCnt:0:exp:False:iep:False:ppd:False']/td[2]")
                        first_image.click()

                        #opens new window, we have to switch to it
                        another_window = list(set(driver.window_handles) - {driver.current_window_handle})[0]
                        driver.switch_to.window(another_window)
                        time.sleep(1)
                        # iterate over all documents in the search date range
                        for j in range(1,26):
                                try:    
                                        iframe = driver.find_element_by_xpath("//iframe")
                                        driver.switch_to_frame(iframe)
                                        time.sleep(2)
                                        page1 = driver.find_element_by_xpath("//*[@id='pageList_0']")
                                        page1.click()
                                        instrument = driver.find_element_by_xpath("//*[@id='lblInstNum']").text
                                        get_image = driver.find_element_by_xpath("//*[@id='btnProcessNow__5']")
                                        get_image.click()

                                        time.sleep(1)
                                        driver.get("https://clerkpublicrecords.scgov.net/Controls/printHelper.aspx?err=skipplugin")
                                        print("downloaded: ", instrument)
                                        iframe = driver.find_element_by_xpath("//iframe")
                                        driver.switch_to_frame(iframe)
                                        close_image = driver.find_element_by_xpath("//*[@id='x:1335771012.4:mkr:Close']")
                                        close_image.click()
                                        next_image = driver.find_element_by_xpath("//*[@id='_imgNext']")
                                        next_image.click()
                                except:
                                        print("error, element not found, skipping page")
                                        break
                        i +=1
               
                    
           
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