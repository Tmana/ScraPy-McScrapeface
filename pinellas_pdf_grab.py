import urllib
import urllib.request
import os
import sys
import datetime
import time
import mechanicalsoup
import sys  
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
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
 



# date1 = input("Please input a start date (mm-dd-yyy):")
# begin_date = datetime.datetime.strptime(date1, '%m-%d-%Y')
# date2 = input("Please input an end date (mm-dd-yyy):")
# end_date = datetime.datetime.strptime(date2, '%m-%d-%Y')



begin_date = datetime.datetime.strptime("01-01-2017", '%m-%d-%Y')
end_date = datetime.datetime.strptime("01-03-2017", '%m-%d-%Y')

captcha_page = "https://public.co.pinellas.fl.us/captcha/captcha.jsp?successPage=/login/captcha_success.jsp"
url = "https://public.co.pinellas.fl.us/officialrec/officialrec/DMDAResults2.jsp?RowsPerPage=500&searchtype=NAME&orname=&orbegdate={0}&orenddate={1}&doctype=DEED&currpage=&recordcount=18855&mindate=05%2F10%2F1941&maxdate=03%2F07%2F2017&booknb=&bookpagenb=&nameSearchType=F&desctext=&instrument=&RowsPerPage=500&pageNumber=1".format(begin_date.strftime("%m/%d/%Y"), end_date.strftime("%m/%d/%Y"))
download_path = "C:/Users/trobart/Desktop/Deeds/scraped_pdfs/pinellas"
username = "1WEBUSER"
password = "FREEACCNT" 
last_instrument = ""
i = 0


########### mechanical soup attempt #############
# browser = mechanicalsoup.Browser()


# landing_page = browser.get(captcha_page)
# form = landing_page.soup.form
# login = form.find("a", {"href" : "javascript: submitform()"})
# response = browser.submit(form, landing_page.url)

# captcha_url = urllib.parse.urljoin(response.url, response.soup.findAll("img")[2]['src'])
# image = urllib.request.urlretrieve(captcha_url)



########  urllib and requests attempt at captcha solving ########
# s = requests.Session()
# r1 = s.get(captcha_page)
# image = s.get("https://public.co.pinellas.fl.us/captcha/Captcha").content
# img = BytesIO(image)
# im = Image.open(img)
# im.show()

# captcha_code = input("Please enter the captcha: ")
# r2 = s.post(captcha_page, data = { "input": captcha_code})
# r3 = s.get(url)


def tiny_file_rename(newname, folder_of_download):
    filename = max([f for f in os.listdir(folder_of_download)], key=lambda xa :   os.path.getctime(os.path.join(folder_of_download,xa)))
    try:
        if '.part' in filename:
            time.sleep(1)
            os.rename(os.path.join(folder_of_download, filename), os.path.join(folder_of_download, newname))
        else:
            os.rename(os.path.join(folder_of_download, filename),os.path.join(folder_of_download,newname))
    except:
        tiny_file_rename(newname, folder_of_download)

try:


        ########## Selenium method for navigating to search query page and entering captcha #########

        options = webdriver.ChromeOptions()

        options.add_experimental_option("prefs", {
            "plugins.plugins_list": [{"enabled":False,"name":"Chrome PDF Viewer"}],
            "download.default_directory" : download_path,
            "download.prompt_for_download": False,
            "plugins.always_open_pdf_externally": True
            })

        driver = webdriver.Chrome(executable_path=r'C:/Users/trobart/Downloads/chromedriver.exe' , chrome_options = options)
        driver.get(captcha_page)

        # wait for user to navigate past captcha
        wait = input("Press Enter after you entered the captcha and navigated to the next page: ")

        driver.get(url)


        os.chdir(download_path)
        html = driver.page_source #grabbing html from selenium driver
        soup = BeautifulSoup(html, "lxml") # using beautifulsoup to parse the website html
        table = soup.find('table', {"id": "tableA"})

        # Iterate over the table on pinellas
        for row in table.findAll('tr')[1:]:
            instrument = row.findAll('td')[-1].text
            j = int(row.td.text)

            for tag in row.findAll('a', href=True): #find <a> tags with href in it so you know it is for urls
                                                     #so that if it doesn't contain the full url itself to it for the download
                    if "NewWindowInit" in tag['href'] and instrument != last_instrument:

                            print(instrument, j)

                            pdf_path = tag['href'].split(",")[-1].strip(")\' ")
                            driver.find_element_by_xpath("//*[@id='tableA']/tbody/tr[{0}]/td[2]/a[3]".format(j)).click()
                            
                            
                            print( "\n[*] Downloading: %s" %(instrument))
                            #close tab 
                            driver.switch_to_window(driver.window_handles[1])
                            driver.close()
                            driver.switch_to_window(driver.window_handles[0]) # switch back to main page

                            tiny_file_rename( "pinellas" + "_" + instrument + ".pdf", download_path) # rename from null to correct name
                            last_instrument = instrument 
                            i+=1
        

        driver.quit()
        print( "\n[*] Downloaded %d files" %(i+1))
        input("[+] Press any key to exit...")
        

except KeyboardInterrupt:
        print( "[*] Exiting...")
        sys.exit(1)
 
except urllib.error.URLError as e:
        print( "[*] Could not get information from server!!")
        sys.exit(2)
 
except:
        print("Unexpected error:", sys.exc_info())
        sys.exit(3)