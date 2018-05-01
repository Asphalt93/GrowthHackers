from bs4 import BeautifulSoup as bs
import urllib.request as req
import pandas as pd
import datetime
import re

melon_list = pd.DataFrame(columns = ['artist',
                                     'artist_code',
                                     'title',
                                     'title_code',
                                     'rank',
                                     'date',
                                     'hour',
                                     'site'])
dt_now = datetime.datetime.now()
####

url = "http://www.melon.com/chart/index.htm#params%5Bidx%5D=1"
header_ = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"

_ = req.Request(url, headers = {'User-Agent':header_})
HTML = req.urlopen(_).read()
page = bs(HTML, 'html.parser')
print(len(page))

songtable = page.find("table", {"border":"1"})
songlists50 = songtable.findAll('tr', {'class':'lst50'})
songlists100 = songtable.findAll('tr', {'class':'lst100'})

def rank_breaker(_):
    global melon_list
    song_artist = _.find("span", {'class':'checkEllipsis'}).get_text().strip()

    ac = _.find('span', {'class':'checkEllipsis'})
    p = re.compile('[0-9]+')
    song_artist_code = int(p.findall(str(ac))[0])

    song_title = _.find("div", {'class':'ellipsis rank01'}).get_text().strip()
    song_title_code = int(_['data-song-no'])
    song_rank = int(_.find("span", {'class' : "rank "}).get_text())
    song_date = dt_now.strftime('%Y-%m-%d')
    song_hour = dt_now.strftime('%H')
    song_site = "melon"

    
    melon_list = melon_list.append(
        {'artist':song_artist,
         'artist_code':song_artist_code,
         'title' : song_title,
         'title_code' : song_title_code,
         'rank' : song_rank,
         'date' : song_date,
         'hour' : song_hour,
         'site' : song_site}, ignore_index = True)

for half in [songlists50, songlists100]:
    for _ in half:
        rank_breaker(_)

melon_list.to_csv("archive/"+dt_now.strftime("%Y_%m_%d_%H")+".csv", index=False, encoding = 'euc-kr')

    

    
    
    
    
