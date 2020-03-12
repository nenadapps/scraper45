from bs4 import BeautifulSoup
import datetime
from random import randint
from random import shuffle
import requests
from time import sleep

def get_html(url):
    
    html_content = ''
    try:
        page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        html_content = BeautifulSoup(page.content, "html.parser")
    except: 
        pass
    
    return html_content

def get_details(url, category):
    
    stamp = {}
    
    try:
        html = get_html(url)
    except:
        return stamp
    
    try:
        title = html.select('.entry-title')[0].get_text().strip()
        stamp['title'] = title
    except:
        stamp['title'] = None      
    
    try:
        raw_text = html.select('#product-description')[0].get_text().strip()
        raw_text = raw_text.replace(u'\xa0', u' ')
        stamp['raw_text'] = raw_text
    except:
        stamp['raw_text'] = None
        
    try:
        country = html.select('.product_meta .posted_in')[0].get_text().strip()
        country = country.replace('Country:', '').strip()
        stamp['country'] = country
    except:
        stamp['country'] = None        
    
    try:
        price = html.select('.summary-top .price .woocommerce-Price-amount')[0].get_text().strip()
        price = price.replace('£', '').strip()
        stamp['price'] = price
    except:
        stamp['price'] = None  
    
    stamp['category'] = category      

    stamp['currency'] = 'GBP'
    
    # image_urls should be a list
    images = []                    
    try:
        image_items = html.select('.woocommerce-product-gallery__image a')
        for image_item in image_items:
            img = image_item.get('href')
            if img not in images:
                images.append(img)
    except:
        pass
    
    stamp['image_urls'] = images 
        
    # scrape date in format YYYY-MM-DD
    scrape_date = datetime.date.today().strftime('%Y-%m-%d')
    stamp['scrape_date'] = scrape_date
    
    stamp['url'] = url
    
    print(stamp)
    print('+++++++++++++')
    sleep(randint(25, 65))
           
    return stamp

def get_page_items(url):

    items = []
    next_url = ''
    
    try:
        html = get_html(url)
    except:
        return items, next_url
    
    try:
        for item in html.select('.product-details h3 a'):
            item_link = item.get('href')
            if item_link not in items:
                items.append(item_link)
    except:
        pass
    
    try:
        next_url_cont = html.select('a.next')[0]
        next_url = next_url_cont.get('href')
    except:
        pass
   
    shuffle(list(set(items)))
    
    return items, next_url

def get_categories():
    
    url = 'https://www.doreenroyan.com/shop/'
   
    items = {}

    try:
        html = get_html(url)
    except:
        return items

    try:
        for item in html.select('.category ul li a'):
            item_link = 'https://www.doreenroyan.com/shop/' + item.get('href')
            item_text = item.get_text().strip()
            if item_link not in items: 
                items[item_text] = item_link
    except: 
        pass
    
    shuffle(list(set(items)))
    
    return items

categories = get_categories()   
for category in categories:
    page_url = categories[category]
    while(page_url):
        page_items, page_url = get_page_items(page_url)
        for page_item in page_items:
            stamp = get_details(page_item, category) 
