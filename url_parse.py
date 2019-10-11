import requests
from bs4 import BeautifulSoup

def get_tune_data(url):
    # youtube_url = 'https://www.youtube.com/watch?v=GoFQHjneFFI'
    
    # youtube_url = url
    # response = requests.get(youtube_url)
    # page = response.text
    # soup = BeautifulSoup(page,'html.parser')
    # title = soup.select('#eow-title')[0].text.strip()       
    # title = title.split('-')
    # artist = title[0].strip()
    # tune_name = title[1].strip()

    # # Removing [OUT NOW] from a tune name
    # index = tune_name.find('[OUT NOW]') 
    # if index > 0:
    #     tune_name = tune_name[:index]

    # print('Artist: ',artist, 'Tune:', tune)
    
    artist = 'Rolo Green'
    tune_name = 'Cool track (Original Mix)'  
    return(artist, tune_name)
