import requests
from bs4 import BeautifulSoup
import re
import datetime
import pandas as pd


def get_html(site):  # goto website and get html
    r = requests.get(site)
    return BeautifulSoup(r.content, "html.parser")


def get_wsj(date, p_df):  # hard coded site for now but you would set the site plus the date
    threshold = float(-10)
    site01 = 'http://www.wsj.com/mdc/public/page/2_3022-losenyse-loser-' + str(date) + '.html'
    site01_soup = get_html(site01)  # get html code
    count = 0
    for tr in site01_soup.findAll("table", class_="mdcTable"):  # get all rows in table
        for a in tr.find_all("a"):  # find column in a row
            tkr = re.search(r'\((.*?)\)', a.text).group(1)  # regex to find the group of characters between ()
            loss = float(tr.find_all('td', attrs={'class': 'nnum', 'style': 'font-weight:bold;'})[count].text)
            if loss > threshold:
                return p_df
            key = tkr + '_' + date
            df.at[key, 'entry_date'] = date
            df.at[key, 'ticker'] = tkr
            df.at[key, 'percent_loss'] = float(loss)
            count += 1
    return p_df


def get_hist_mkt_cap(entry_date, df):
    for tkr in df['ticker']:
        site = 'https://ycharts.com/companies/' + tkr + '/market_cap'
        soup = get_html(site)
        for tr in soup.findAll("table", class_="histDataTable"):
            for td in tr.find_all("td"):
                if "2019" in td.text:
                    try:
                        date = str(datetime.datetime.strptime(td.text.replace('.', ''), "%B %d, %Y")).replace('-', '').split(" ")[0]
                    except:
                        date = str(datetime.datetime.strptime(td.text.replace('.', ''), "%b %d, %Y")).replace('-', '').split(" ")[0]
                    m_cap = td.find_next_sibling("td").text.split('\n')[2].replace(' ', "")
                    key = tkr + '_' + entry_date
                    df.at[key, 'martket_cap_M'] = float(m_cap[:-1])
                    break
    return df

def get_hist_adj_close(entry_date, df):
    days_to_check = 46  # from day 0 price to day this - 1
    for tkr in df['ticker']:
        key = tkr + '_' + entry_date
        site = 'https://finance.yahoo.com/quote/' + tkr + '/history'
        # print(site)
        soup = get_html(site)
        entries = []
        count = 0
        flag = False
        for tr in soup.findAll("table", class_="W(100%) M(0)"):
            for td in tr.find_all("td"):
                if '2019' in td.text:
                    date = str(datetime.datetime.strptime(td.text.replace('.', ''), "%b %d, %Y")).replace('-', '').split(" ")[0]
                    col1 = td.find_next_sibling('td')
                    if 'Dividend' in col1.text:
                        continue
                    col2 = col1.find_next_sibling('td')
                    col3 = col2.find_next_sibling('td')
                    col4 = col3.find_next_sibling('td')
                    col5 = col4.find_next_sibling('td')
                    df.at[key, "{:02d}".format(count) + '_days_from_entry_date'] = float(col5.text)
                    count += 1
                if count >= days_to_check:
                    break
    return df


if __name__ == '__main__':
    date = '20190508'
    df = pd.DataFrame()
    print('Getting percent loss...')
    df = get_wsj(date, df)

    print('Getting market cap...')
    df = get_hist_mkt_cap(date, df)

    print('Getting Adjusted close...')
    df = get_hist_adj_close(date, df)

    filename = date + '.csv'
    print('Saving file to ' + filename)
    df.to_csv(filename)
    print('finished')

