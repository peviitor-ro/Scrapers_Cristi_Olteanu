#
# Company - > Snyk
# Link -> https://boards.greenhouse.io/snyk?gh_src=3f9b65652us
#
from A_OO_get_post_soup_update_dec import update_peviitor_api,DEFAULT_HEADERS
from L_00_logo import update_logo
from bs4 import BeautifulSoup
import requests
import uuid


def get_jobs():
    req = requests.get('https://boards.greenhouse.io/snyk?gh_src=3f9b65652us', headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(req.text, 'lxml')
    list = []

    jobs = soup.find_all('div', class_='opening')

    for job in jobs:
        title = job.find('a').text
        link = job.find('a')['href']
        location = job.find('span', class_='location').text.split()[0].strip(',')

        if 'Remote' in job.find('span', class_='location').text:
            remote = 'remote'
        else:
            remote = 'on-site'

        if 'Cluj' in location or 'Bucharest' in location:
            list.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link": 'https://boards.greenhouse.io/' + link,
                "company": "Snyk",
                "country": "Romania",
                "city": location,
                "remote": remote

            })

    return list

@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Snyk'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Snyk',
                  'https://snyk.io/_next/image/?url=https%3A%2F%2Fres.cloudinary.com%2Fsnyk%2Fimage%2Fupload%2Fv1669650003%2Fpress-kit%2Ftitle-card-logo-white-1.png&w=2560&q=75'
                  ))

