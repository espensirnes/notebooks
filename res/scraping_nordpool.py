from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import time
import re
	
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
	f=open('res/table.csv','w')
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
	path = ChromeDriverManager().install()
	driver = webdriver.Chrome(service=webdriver.ChromeService(path))
	driver.get(url)

	#sometimes the page is not loaded properly, so repeating until we have fetched a 
	#postive length string:
	for i in range(1000):
		s = find_string_between(driver.page_source, 
						'<table class="dx-datagrid-table dx-datagrid-table-fixed" .*?>',
						'</table>', 
						1)
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
			cell = format(cell)
			r.append(cell)
		a.append(r)
	return a
	
	
def format(cell):
	"""Returns the text of cell"""

	if cell.content is None:
		return cell.text
	if len(cell.content)==0:
		return ''
	s = ''
	s = ' '.join([str(c) for c in cell.content])

	#if there is undesired contents, replace it here:
	s = s.replace('\xa0','')
	s = s.replace('\n','')
	return s

def find_string_between(string,a,b,n):
	"returns the substring of string between expressions a and b, occurence n" 
	a = re.findall(a, string)
	if len(a)==0:
		return ''
	a = string.index(a[n])
	b = re.findall(b, string[a:])[0]
	b = string[a:].index(b)
	return string[a:a+b]





scrape('https://data.nordpoolgroup.com/auction/day-ahead/prices?deliveryDate=2024-04-02&currency=EUR&aggregation=Daily&deliveryAreas=EE,LT,LV,AT,BE,FR,GER,NL,PL,DK1,DK2,FI,NO1,NO2,NO3,NO4,NO5,SE1,SE2,SE3,SE4,SYS')