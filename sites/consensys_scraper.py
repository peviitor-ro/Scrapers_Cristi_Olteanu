#
# Company - > Consensys
# Link -> https://consensys.io/open-roles
#

from A_OO_get_post_soup_update_dec import update_peviitor_api, DEFAULT_HEADERS
from L_00_logo import update_logo
import requests
from bs4 import BeautifulSoup


def get_jobs():
    jobs_list = []

    req = requests.get("https://consensys.io/open-roles", headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(req.text, "lxml")

    links = soup.find_all('a', href=lambda x: x and '/open-roles/' in x)

    for link in links:
        href = link.get('href')
        text = link.text.strip()
        
        if 'EMEA - Remote' in text or 'GLOBAL - Remote' in text:
            # Extract title - get everything before the first location
            title = text.split(',')[0].strip()
            # Remove location suffixes from title
            title = title.replace('UNITED STATES - Remote', '').replace('CANADA - Remote', '').replace('EMEA - Remote', '').replace('GLOBAL - Remote', '').replace('  ', ' ').strip()
            title = title.rstrip('-').strip()
            
            jobs_list.append({
                "job_title": title,
                "job_link": 'https://consensys.io' + href,
                "company": "Consensys",
                "country": "Romania",
                "city": 'Bucuresti',
                "county": 'Bucuresti',
                "remote": 'remote'
            })
    return jobs_list


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Consensys'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Consensys',
                  'https://consensys.io/_app/immutable/assets/logo.b5f12401.svg'
                  ))