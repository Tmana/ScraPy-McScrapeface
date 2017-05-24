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



 ########### mechanical soup attempt #############
browser = mechanicalsoup.Browser()


landing_page = browser.get(captcha_page)
form = landing_page.soup.form
login = form.find("a", {"href" : "javascript: submitform()"})
response = browser.submit(form, landing_page.url)

captcha_url = urllib.parse.urljoin(response.url, response.soup.findAll("img")[2]['src'])
image = urllib.request.urlretrieve(captcha_url)




#######  urllib and requests attempt at captcha solving ########
s = requests.Session()
r1 = s.get(captcha_page)
image = s.get("https://public.co.pinellas.fl.us/captcha/Captcha").content
img = BytesIO(image)
im = Image.open(img)
im.show()

captcha_code = input("Please enter the captcha: ")
r2 = s.post(captcha_page, data = { "input": captcha_code})
r3 = s.get(url)
