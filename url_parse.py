import requests
from bs4 import BeautifulSoup

# youtube_url = 'https://www.youtube.com/watch?v=GoFQHjneFFI'

# response = requests.get(youtube_url)
# page = response.text
# soup = BeautifulSoup(page,'html.parser')
# title = soup.select('#eow-title')[0].text.strip()       
# title = title.split('-')
# artist = title[0].strip()
# tune = title[1].strip()

# # Removing [OUT NOW] from a tune name
# index = tune.find('[OUT NOW]') 
# if index > 0:
#     tune = tune[:index]

# print('Artist: ',artist, 'Tune:', tune)
def get_tune_data(url):
    artist = 'Rolo Green'
    tune_name = 'Cool track (Original Mix)'  
    return(artist, tune_name)
