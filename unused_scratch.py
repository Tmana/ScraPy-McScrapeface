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
