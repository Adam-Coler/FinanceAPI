import requests
from bs4 import BeautifulSoup
import re
import datetime


def get_html(site):  # goto website and get html
    r = requests.get(site)
    return BeautifulSoup(r.content, "html.parser")

def get_wsj(date): # hard coded site for now but you would set the site plus the date
    threshold = float(-10)
    site01 = 'http://www.wsj.com/mdc/public/page/2_3022-losenyse-loser-' + str(date) + '.html'
    site01_soup = get_html(site01)  # get html code
    tkr_list = []
    # this site uses a table class called mdcTable to store the elements you want
    # the elements are in a span called "a"

    # get elements
    count = 0
    for tr in site01_soup.findAll("table", class_="mdcTable"):  # get all rows in table
        for a in tr.find_all("a"):  # find column in a row
            tkr = re.search(r'\((.*?)\)', a.text).group(1)  # regex to find the group of characters between ()
            loss = float(tr.find_all('td', attrs={'class': 'nnum', 'style': 'font-weight:bold;'})[count].text)
            if loss > threshold:
                return tkr_list
            tkr_list.append([date, tkr, count, loss])
            count += 1
    return tkr_list

# https://finance.yahoo.com/quote/GE/history/
# https://ycharts.com/companies/AAPL/market_cap


def get_hist_mkt_cap(tkr):
    site = 'https://ycharts.com/companies/' + tkr + '/market_cap'
    soup = get_html(site)
    entries = []
    for tr in soup.findAll("table", class_="histDataTable"):
        for td in tr.find_all("td"):
            if "2019" in td.text:
                try:
                    date = str(datetime.datetime.strptime(td.text.replace('.', ''), "%B %d, %Y")).replace('-', '').split(" ")[0]
                except:
                    date = str(datetime.datetime.strptime(td.text.replace('.', ''), "%b %d, %Y")).replace('-', '').split(" ")[0]
                entries.append([date, tkr, td.find_next_sibling("td").text.split('\n')[2].replace(' ', "")])

    return entries

# https://finance.yahoo.com/quote/AAPL/history
def get_hist_adj_close(tkr):
    site = 'https://finance.yahoo.com/quote/' + tkr + '/history'
    soup = get_html(site)
    entries = []
    count = 0
    for tr in soup.findAll("table", class_="W(100%) M(0)"):
        for td in tr.find_all("td"):
            if '2019' in td.text:
                date = str(datetime.datetime.strptime(td.text.replace('.', ''), "%b %d, %Y")).replace('-', '').split(" ")[0]
                col1 = td.find_next_sibling('td')
                col2 = col1.find_next_sibling('td')
                col3 = col2.find_next_sibling('td')
                col4 = col3.find_next_sibling('td')
                col5 = col4.find_next_sibling('td')
                entries.append([date, tkr, float(col5.text)])
                if count >= 44:
                    return entries
                count += 1
    return entries



tkrs_site01 = get_wsj('20190507')
top_tkr = tkrs_site01[:1][0][1]

cap1 = get_hist_mkt_cap(top_tkr)
ents = get_hist_adj_close(top_tkr)

print(tkrs_site01)
print(cap1)
print(ents)


