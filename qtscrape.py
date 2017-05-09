import sys  
from PyQt4.QtGui import *  
from PyQt4.QtCore import *  
from PyQt4.QtWebKit import *  
from lxml import html 
import datetime

#Take this class for granted.Just use result of rendering.
class Render(QWebPage):  
  def __init__(self, url):  
    self.app = QApplication(sys.argv)  
    QWebPage.__init__(self)  
    self.loadFinished.connect(self._loadFinished)  
    self.mainFrame().load(QUrl(url))  
    self.app.exec_()  
  
  def _loadFinished(self, result):  
    self.frame = self.mainFrame()  
    self.app.quit()  


begin_date = datetime.datetime.strptime("01-01-2017", '%m-%d-%Y')
end_date = datetime.datetime.strptime("03-20-2017", '%m-%d-%Y')


url = "https://public.co.pinellas.fl.us/officialrec/officialrec/DMDAResults2.jsp?RowsPerPage=500&searchtype=NAME&orname=&orbegdate={0}&orenddate={1}&doctype=DEED&currpage=&recordcount=18855&mindate=05%2F10%2F1941&maxdate=03%2F07%2F2017&booknb=&bookpagenb=&nameSearchType=F&desctext=&instrument=&RowsPerPage=400&pageNumber=1".format(begin_date.strftime("%m/%d/%y"), end_date.strftime("%m/%d/%y"))

r = Render(url)  
result = r.frame.toHtml()
#This step is important.Converting QString to Ascii for lxml to process
archive_links = html.fromstring(str(result.toAscii()))
print(archive_links)