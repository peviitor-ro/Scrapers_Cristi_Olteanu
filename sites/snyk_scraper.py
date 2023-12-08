#
# Company - > Snyk
# Link -> https://boards.greenhouse.io/snyk?gh_src=3f9b65652us
#
from A_OO_get_post_soup_update_dec import update_peviitor_api,DEFAULT_HEADERS
from L_00_logo import update_logo
from bs4 import BeautifulSoup
import requests


def get_job_type(url):

    response = requests.get(url, headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')
    text = soup.find('div', {'id': 'content'}).text

    if 'remote' in text:
        job_type = 'remote'
    else:
        job_type = 'on-site'
    return job_type


def get_jobs():

    jobs_list = []
    req = requests.get('https://boards.greenhouse.io/snyk?gh_src=3f9b65652us', headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(req.text, 'lxml')

    jobs = soup.find_all('div', class_='opening')

    for job in jobs:
        title = job.find('a').text
        link = 'https://boards.greenhouse.io/' + job.find('a')['href']
        locations = job.find('span', class_='location').text.split()
        cities = []

        for location in locations:
            if 'Cluj' in location:
                cities.append('Cluj Napoca')
            elif 'Bucharest' in location:
                cities.append('Bucuresti')

        if cities:
            job_type = get_job_type(link)

            jobs_list.append({
                "job_title": title,
                "job_link": link,
                "company": "Snyk",
                "country": "Romania",
                "city": cities,
                "remote": job_type
            })

    return jobs_list

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

