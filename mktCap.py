import requests
from bs4 import BeautifulSoup

def get_mkt_cap(symbol):
    r = requests.get("https://finance.yahoo.com/quote/" + symbol)
    soup = BeautifulSoup(r.content, "html.parser")
    for tr in soup.findAll("table", class_="W(100%) M(0) Bdcl(c)"):
        for td in tr.find_all("td"):
            if td.text == "Market Cap":
                string_cap, value = td.text, td.find_next_sibling("td").text
    return string_cap, value

print(get_mkt_cap("NGL"))