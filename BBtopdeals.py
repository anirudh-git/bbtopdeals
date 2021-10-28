from bs4 import BeautifulSoup
from requests_html import HTMLSession
import pandas as pd
import argparse

# my_parser = argparse.ArgumentParser(description=('Return deals'))
# my_parser.add_argument('searchterm', metavar=('searchterm'),help=('Item to be searched. Use + for spaces'))  
# args = my_parser.parse_args()

# searchterm = 'dslr+sd+card+64gb+ritz'

# searchterm = args.searchterm

s = HTMLSession()

dealslist = []

url = 'https://www.bestbuy.com/site/electronics/top-deals/pcmcat1563299784494.c?id=pcmcat1563299784494'


def getdata(url):
    r = s.get(url)
    r.html.render(sleep=5, timeout=100)
    soup = BeautifulSoup(r.html.html, 'html.parser')
    return soup


def getdeals(soup):
    products = soup.find_all('div', {'class': 'wf-offer-content'})
    for item in products:
        try:
            title = item.find('a', {'style': '-webkit-line-clamp:3'}).text.strip()
        except:
            title = 'None'
        try:
            link = item.find('a', {'class': 'wf-offer-link v-line-clamp'})['href']
        except:
            continue
        try:
            salepricetext = item.find('div', {'class': 'priceView-hero-price priceView-customer-price'})
            saleprice = float(salepricetext.find('span', {'aria-hidden': 'true'}).text.replace('$','').replace(',','').strip())
            oldprice = float(item.find('div', {'class': 'pricing-price__regular-price'}).text.replace('Was $','').replace(',','').strip())
        except:
            try:
                oldprice = float(item.find('div', {'class': 'pricing-price__regular-price'}).text.replace('Was $','').replace(',','').strip())
            except: oldprice = saleprice
           
        saleitem = {
            
            'title': title,
            'Link': link,
            'saleprice': saleprice,
            'oldprice': oldprice
            }
        dealslist.append(saleitem)
        
df = pd.DataFrame(dealslist)
print(df.head())
# df['percentoff'] = 100 - ((df.saleprice / df.oldprice) * 100)
# df = df.sort_values(by = ['percentoff'], ascending=False)
# df.to_csv('bbtopdeals.csv',index=False)
print('Completed')    