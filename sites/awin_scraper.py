#
# Company - > Awin
# Link -> https://job-boards.greenhouse.io/awin
#
from A_OO_get_post_soup_update_dec import update_peviitor_api, DEFAULT_HEADERS
from L_00_logo import update_logo
from bs4 import BeautifulSoup
import requests
from _county import get_county
from _validate_city import validate_city


def get_jobs():
    list_jobs = []

    req = requests.get("https://job-boards.greenhouse.io/awin", headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(req.text, "lxml")

    jobs = soup.find_all('a', href=lambda x: x and '/jobs/' in str(x))

    for job in jobs:
        text = job.text.strip()
        
        if 'Romania' not in text:
            continue
        
        link = job.get('href')
        
        # Extract title - remove city/country from text
        parts = text.split(',')
        title = parts[0].strip()
        
        # Clean title (remove city suffix like "Iași")
        for part in parts[1:]:
            if 'Romania' in part:
                break
            if 'Iași' in part or 'Iasi' in part or 'Bucharest' in part:
                title = title.replace(part.strip(), '').strip()
                break
        
        if 'Iasi' in text or 'Iași' in text:
            city = 'Iasi'
        elif 'Bucharest' in text:
            city = 'Bucuresti'
        else:
            city = ''
        
        list_jobs.append({
            "job_title": title,
            "job_link": link,
            "company": "Awin",
            "country": "Romania",
            "city": city,
            "county": get_county(city),
            "remote": 'on-site',
        })
    return list_jobs


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Awin'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Awin',
                  'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/Logo-awin-black.svg/177px-Logo-awin-black.svg.png'
                  ))