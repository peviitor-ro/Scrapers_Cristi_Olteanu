#
# Company - > OlxGroup
# Link -> https://jobs.eu.lever.co/olx/?
#
from A_OO_get_post_soup_update_dec import update_peviitor_api,DEFAULT_HEADERS
from L_00_logo import update_logo
import requests
from bs4 import BeautifulSoup


def get_jobs():

    list_jobs = []

    response = requests.get('https://jobs.eu.lever.co/olx', headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    jobs = soup.find_all('div', class_='posting')

    for job in jobs:
        link = job.find('a', class_='posting-title')['href']
        title = job.find('h5').text
        country = job.find('span',  class_='sort-by-location posting-category small-category-label location'
                           ).text
        job_type = job.find('span', class_='display-inline-block small-category-label workplaceTypes'
                            ).text.split()[0]
        location_info = job.find('span', class_='sort-by-location posting-category small-category-label location'
                                 ).text.split()
        cities = []
        if 'Romania' in country:

            for location in location_info:

                if 'bucharest' in location.lower():
                    cities.append('Bucuresti')
                elif 'cluj' in location.lower():
                    cities.append('Cluj-Napoca')
                elif 'timisoara' in location.lower():
                    cities.append('Timisoara')
                elif 'iasi' in location.lower():
                    cities.append('Iasi')

            if not cities:
                cities.append('Bucuresti')

            list_jobs.append({
                "job_title": title,
                "job_link": link,
                "company": "Olx",
                "country": "Romania",
                "city": cities,
                "remote": job_type
            })
    return list_jobs


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """
    return data_list

company_name = 'Olx'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Olx',
                  'https://seeklogo.com/images/O/olx-group-logo-D786F321B8-seeklogo.com.png'
                  ))
