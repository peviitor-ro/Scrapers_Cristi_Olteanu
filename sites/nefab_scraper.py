#
#  Company - > nefab
# Link -> https://www.nefab.com/en/careers/job-opportunities/
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
import requests
from bs4 import BeautifulSoup


def get_soup(url):

    response = requests.get(url, headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup


def get_jobs():

    job_list = []

    jobs = get_soup('https://nefab.workbuster.com'
                    ).find_all('div', class_='position-container filter-item')

    for job in jobs:
        title = job.find('a').text
        link_id = job.find('a')['href'].split('jobs/')[1].split('-')[0]
        link = f'https://www.nefab.com/en/careers/job-opportunities?jobid={link_id}'
        try:
            city = job.find('span', class_='location tag').text
        except:
            if 'Timisoara' in title:
                city = 'Timisoara'
            elif 'Brasov' in title:
                city = 'Brasov'
            else:
                city = None

        if city in ['Timisoara', 'Brasov']:
            job_list.append({
                "job_title": title,
                "job_link": link,
                "company": "nefab",
                "country": "Romania",
                "city": city,
            })
    return job_list

@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """
    return data_list

company_name = 'nefab'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('nefab',
                  'https://www.nefab.com/globalassets/nefab.com--group-site/new-site/startpage/new-purpose-launch/nefab_new_tagline_primary_blue_rgb_small.png'
                  ))

