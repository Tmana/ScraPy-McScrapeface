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
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from PyQt4.QtGui import *  
from PyQt4.QtCore import *  
from PyQt4.QtWebKit import *  
from lxml import html 
from http.cookiejar import CookieJar
from PIL import Image
import requests
from io import BytesIO

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
        



def pinellas_scrape(begin_date = "", end_date = ""):


    # initializing variables
    
    captcha_page = "https://public.co.pinellas.fl.us/captcha/captcha.jsp?successPage=/login/captcha_success.jsp"
    download_path = "C:/Users/trobart/Desktop/Deeds/scraped_pdfs/pinellas"
    username = "1WEBUSER"
    password = "FREEACCNT" 
    last_instrument = ""
    i = 0

    if begin_date == "":
        date1 = input("Please input a start date (mm-dd-yyyy):")
        begin_date = datetime.datetime.strptime(date1, '%m-%d-%Y')
        date2 = input("Please input an end date (mm-dd-yyyy):")
        end_date = datetime.datetime.strptime(date2, '%m-%d-%Y')

    delta_date = end_date - begin_date
    os.chdir(download_path)


    ########## Selenium method for navigating to search query page and entering captcha #########

    options = webdriver.ChromeOptions()

    options.add_experimental_option("prefs", {
        "plugins.plugins_list": [{"enabled":False,"name":"Chrome PDF Viewer"}],
        "download.default_directory" : download_path,
        "download.prompt_for_download": False,
        "plugins.always_open_pdf_externally": True,
        "download.open_pdf_in_system_reader": False
        })
    #options.add_argument('--headless')
    
    driver = webdriver.Chrome(executable_path=r'C:/Users/trobart/Downloads/chromedriver.exe' , chrome_options = options)
    driver.get(captcha_page)

    # wait for user to navigate past captcha
    wait = WebDriverWait(driver, 50)
    wait.until(EC.title_is('Pinellas County Records Main Menu'))

    # loop over day range
    for i in range(delta_date.days + 1):

        try:
            # grabbing a new url query for each day
            temp_day = begin_date + datetime.timedelta(days=i)
            print("day: ", temp_day)
            url = "https://public.co.pinellas.fl.us/officialrec/officialrec/DMDAResults2.jsp?RowsPerPage=500&searchtype=NAME&orname=&orbegdate={0}&orenddate={1}&doctype=DEED&currpage=&recordcount=18855&mindate=05%2F10%2F1941&maxdate=03%2F07%2F2017&booknb=&bookpagenb=&nameSearchType=F&desctext=&instrument=&RowsPerPage=500&pageNumber=1".format(temp_day.strftime("%m/%d/%Y"), temp_day.strftime("%m/%d/%Y"))

            #now that we've landed past the captcha, and have a valid session, move to the search query
            driver.get(url)
            
            html = driver.page_source #grabbing html from selenium driver
            soup = BeautifulSoup(html, "lxml") # using beautifulsoup to parse the website html

            # iterate over the pages
            if soup.findAll('td', {"class" : "formbody"})[1].a:
                pages = soup.findAll('td', {"class" : "formbody"})[1]
                for i in range(1,len(pages.a)+2):
                    print("page: ", i)
                    url = "https://public.co.pinellas.fl.us/officialrec/officialrec/DMDAResults2.jsp?RowsPerPage=500&searchtype=NAME&orname=&orbegdate={0}&orenddate={1}&doctype=DEED&currpage=&recordcount=18855&mindate=05%2F10%2F1941&maxdate=03%2F07%2F2017&booknb=&bookpagenb=&nameSearchType=F&desctext=&instrument=&RowsPerPage=500&pageNumber={2}".format(temp_day.strftime("%m/%d/%Y"), temp_day.strftime("%m/%d/%Y"), i)
                    driver.get(url)
                
                    html = driver.page_source #grabbing html from selenium driver
                    soup = BeautifulSoup(html, "lxml") # using beautifulsoup to parse the website html
                    table = soup.find('table', {"id": "tableA"})

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
                    
            else:
                # grabbing a new url query for each day
                temp_day = begin_date + datetime.timedelta(days=i)
                print("day: ", temp_day)
                url = "https://public.co.pinellas.fl.us/officialrec/officialrec/DMDAResults2.jsp?RowsPerPage=500&searchtype=NAME&orname=&orbegdate={0}&orenddate={1}&doctype=DEED&currpage=&recordcount=18855&mindate=05%2F10%2F1941&maxdate=03%2F07%2F2017&booknb=&bookpagenb=&nameSearchType=F&desctext=&instrument=&RowsPerPage=500&pageNumber=1".format(temp_day.strftime("%m/%d/%Y"), temp_day.strftime("%m/%d/%Y"))

                html = driver.page_source #grabbing html from selenium driver
                soup = BeautifulSoup(html, "lxml") # using beautifulsoup to parse the website html
                table = soup.find('table', {"id": "tableA"})

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
            continue
        except IndexError as e:
            print('index error!', e, sys.stderr)
            try:
                break
            finally:
                print("Session expired, please re-enter new captcha")
                pinellas_scrape(temp_day, end_date)
        except:
            print("Unexpected error:", sys.stderr, sys.exc_info())
            pass

if __name__ == '__main__':
    pinellas_scrape()