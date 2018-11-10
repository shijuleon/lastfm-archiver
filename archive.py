from bs4 import BeautifulSoup
import requests
import json

headers = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}

total_pages= 246
library_url = "https://www.last.fm/user/shijuleon/library?page={}"

play_info = {"artist": None, "track": None, "timestamp": None}
track_pages = []

def download_page(page, content):
    with open(page+'.html', 'w') as f:
        f.write(content)

def get_page(page):
    page_url = library_url.format(page)
    req = requests.get(page_url, headers=headers)
    page_name = "library_page_{}".format(page)
    content = req.content
    #download_page(page_name, content)
    soup = BeautifulSoup(content, 'html.parser')
    track_tags = soup.find_all("tr")
    #print len(track_tags)
    page_tracks = []
    for i in range(1, len(track_tags)):
        try: # hacky fix for now
            artist = track_tags[i].find_all("td", {"class":"chartlist-name"})[0].find_all("a")[0].text.encode('utf-8')
            track = track_tags[i].find_all("td", {"class":"chartlist-name"})[0].find_all("a")[1].text.encode('utf-8')
            timestamp = track_tags[i].find_all("td", {"class":"chartlist-timestamp"})[0].find_all("span")[0].text.encode('utf-8')
            print "{} - {} - {}".format(artist, track, timestamp)
            play_info['artist'], play_info['track'], play_info['timestamp'] = artist, track, timestamp
            page_tracks.append(play_info.copy())
        except IndexError:
            pass
    track_pages.append({page:page_tracks})

def write_to_json(filename = "final.json"):
    with open(filename, "w") as f:
        json.dump(track_pages, f, ensure_ascii=False)

for i in range(total_pages, total_pages+1):
    get_page(i)

print json.dumps(track_pages, ensure_ascii=False)
#write_to_json()
