from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
	
def scrape(url):
	#get the html from the url
	html=get_page(url)

	#read it with BS
	bs=BeautifulSoup(html)

	#extract all tables and put in array t
	tables=bs.find_all('table')
	t=[]
	for tbl in tables:
		t.extend(html_to_table(tbl))


	#save the result:
	f=open('table.csv','w')
	for row in t:
		f.write(';'.join(row)+'\n')
	f.close()
	a=0

def get_page(url):
	"""returns a specific part of the web site. For some reason 
	BS cannot easily extract the second table, which is the one with data
	which we are interested in"""
	#open the url in browser
	#If SessionNotCreatedException, update chrome. 
	driver = webdriver.Chrome(ChromeDriverManager().install())
	driver.get(url)

	#sometimes the page is not loaded properly, so repeating until we have fetched a 
	#postive length string:
	for i in range(1000):
		s=find_string_between(driver.page_source, '<table id="datatable">','</tfoot></table>')
		if len(s)>0:
			break
		time.sleep(1)
	return s	

def html_to_table(tbl):
	"""Extracts the table from a table found with BS"""
	
	#initiates the list object that will be returned:
	a=[]
	#iterates over all table rows:
	for row in tbl.find_all('tr'):
		#initiates the current row to be added to a:
		r=[]
		
		#identifies all cells in row:
		cells=row.find_all('td')
		#if there were no normal cells, there might be header cells:
		if len(cells)==0:
			cells=row.find_all('th')

		#iterate over cells 
		for cell in cells:
			cell=format(cell)
			r.append(cell)
		a.append(r)
	return a
	
	
def format(cell):
	"""Returns the text of cell"""

	if cell.content is None:
		return cell.text
	if len(cell.content)==0:
		return ''
	s=''
	s=' '.join([str(c) for c in cell.content])

	#if there is unwanted contents, replace it here:
	s=s.replace('\xa0','')
	s=s.replace('\n','')
	return s

def find_string_between(string,a,b):
	"returns the substring of string between expressions a and b" 
	a=string.find(a)
	b=string.find(b)+len(b)
	return string[a:b]





scrape('https://www.nordpoolgroup.com/Market-data1/Dayahead/Area-Prices/NO/Monthly/?view=table')