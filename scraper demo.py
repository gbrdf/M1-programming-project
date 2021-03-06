import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

def scraper() :
    genre = []
    game_names = []
    game_prices = []
    console = []
    buy_type = []
    game_url = []
   
    page = requests.get("https://www.go2games.com/catalogsearch/result/index/?category_type=4507&p="+"2"+"&q=VIDEO+GAMES")
    soup = BeautifulSoup(page.content, "html.parser")
        
    for names in soup.find_all('a', alt=True):
        game_names.append(names['alt'])


    product_details = soup.find_all(class_="item product product-item")
    for info in product_details :
        prices = info.find('span', {'class':'price'})
        game_prices.append(prices.text)


    for info in product_details :
        button =info.find('button', title=True)
        if button is not None and button['title'] is not None :
            buy_type.append(button['title'])
        if button is None :
            buy_type.append('NA')
    
    
    for info in product_details :
        urls = info.find('a', href=True)
        game_url.append(urls['href'])   
    
    

#     We will use the list game_url to scrap all the info that we need on the individual game pages. In other words : the game's 
#   genre and console type.    

    l = len(game_url)

    for m in range(0, l) :
        PAGE = requests.get(game_url[m])
        soup = BeautifulSoup(PAGE.content, 'html')
    
        genre_info =soup.find_all('td', attrs={'data-th': "Genre"})
        if genre_info is None :
            genre.append('NA')
        else :
            genre_clean_1 = re.findall('(.*?)</td>',str(genre_info))
            genre_clean_2 = (', '.join(genre_clean_1))
            genre.append(genre_clean_2)
    
        console_info =soup.find_all('td', attrs={'data-th': "Platform"})
        if console_info is None :
            console.append('NA')
        else :
            console_clean_1 = re.findall('(.*?)</td>',str(console_info))
            console_clean_2 = (', '.join(console_clean_1))
            console.append(console_clean_2)
    
    console[:]=['NA' if y=='' else y for y in console]
    console = [re.sub('[ ]{2,}','',itemc) for itemc in console]
    genre[:]=['NA' if x=='' else x for x in genre]
    genre = [re.sub('[ ]{2,}','',item) for item in genre]
    del game_names[::2]          
    
    df = pd.DataFrame(list(zip(game_names, genre, game_prices, console, buy_type)), 
               columns =["Game Names", "Genre", "Game Prices", "Console", "How to buy"]) 
    return  df
    
scraper()    

      


