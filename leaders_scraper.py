import json
import requests
from bs4 import BeautifulSoup
import re

def get_first_paragraph(wikipedia_url, session):
     # initialization variables
     req = session.get(wikipedia_url)
     soup = BeautifulSoup(req.text, "html.parser")
     paragraphs = soup.find_all('p')
     regexpaterns = ["\[\d+\]","\[\w\]","\([^)]*\)"]
     new_paragraph = ''

     print(wikipedia_url) # keep this for the rest of the notebook
          
          #   [insert your code]
     
     for paragraph in soup.find_all('p'):
          if paragraph.find('b'):
               first_paragraph = paragraph.text
               break
               
     for regex in regexpaterns:
          first_paragraph = re.sub(regex,'',first_paragraph)
     
     return first_paragraph

def get_leaders():
    root_url = "https://country-leaders.herokuapp.com"
    s = requests.Session()

    cookie_url = root_url + "/cookie"
    cookies = s.get(cookie_url).cookies

    countries_url = root_url + "/countries"
    req_countries = s.get (countries_url, cookies=cookies)
    countries = req_countries.json()

    leaders_url = root_url + "/leaders"
    leaders_per_country ={}
    for country in countries:
        payload = {'country':country}
        req_leaders = s.get(leaders_url, params=payload, cookies=cookies)

        if req_leaders.status_code == 403:
            cookies = s.get(cookie_url).cookies
            req_leaders = s.get(leaders_url, params=payload, cookies=cookies)
        leaders_per_country[country] = req_leaders.json()

        for leader in leaders_per_country[country]:
            leader["first_paragraph"] = get_first_paragraph(leader["wikipedia_url"], s)

    return leaders_per_country



def save(leaders_per_country):
    with open('leaders.json','w') as f:
        json.dump(leaders_per_country, f)


leaders_per_country = get_leaders()
save(leaders_per_country)