#
#  Company - > fotc
# Link -> https://fotc.peopleforce.io/careers
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from _validate_city import validate_city
from _county import get_county

CAREERS_URL = 'https://fotc.peopleforce.io/careers'


def get_remote_type(page_text):
    lower_text = page_text.lower()
    offer_start = lower_text.find('we offer')
    if offer_start != -1:
        offer_end = lower_text.find('apply now', offer_start)
        offer_section = (lower_text[offer_start:offer_end]
                         if offer_end != -1 else lower_text[offer_start:])
        return 'remote' if 'remote' in offer_section else 'on-site'

    return 'remote' if re.search(r'\b(?:100%\s*remote|fully\s+remote)\b',
                                 lower_text) else 'on-site'


def get_jobs():

    list_jobs = []
    response = requests.get(CAREERS_URL, headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    for card in soup.select('#results .tw-col-12'):
        link = card.find('a', class_='stretched-link')
        location_icon = card.find('i', class_='fa-map-marker-alt')
        if link is None or location_icon is None:
            continue

        title = link.get_text(strip=True)
        location_text = location_icon.parent.get_text(' ', strip=True)
        if location_text.upper() != 'RO' and 'romania' not in title.lower():
            continue

        job_link = urljoin(CAREERS_URL, link.get('href', ''))
        job_page = requests.get(job_link, headers=DEFAULT_HEADERS)
        page_text = BeautifulSoup(job_page.text, 'lxml').get_text(' ', strip=True)
        city = validate_city('Romania')

        list_jobs.append({
            "job_title": title,
            "job_link": job_link,
            "company": "fotc",
            "country": "Romania",
            "city": city,
            "county": get_county(city),
            "remote": get_remote_type(page_text)
        })
    return list_jobs


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'fotc'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('fotc',
                  'https://fotc.jobsoid.com/PortalJob/GetPortalLogo?size=medium'
                  ))
