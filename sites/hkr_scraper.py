#
# Company - > hkr
# Link -> https://jobs.eu.lever.co/hkr/
#
from A_OO_get_post_soup_update_dec import update_peviitor_api,DEFAULT_HEADERS
from L_00_logo import update_logo
import requests
from bs4 import BeautifulSoup



def get_jobs():
    response = requests.get('https://jobs.eu.lever.co/hkr/?', headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    list_jobs = []

    jobs = soup.find_all('div', class_='posting')

    for job in jobs:
        link = job.find('a', class_='posting-title')['href']
        title = job.find('a', class_='posting-title').find('h5').text
        location = job.find('span', class_='sort-by-location posting-category small-category-label location').text
        job_type = job.find('span', class_='display-inline-block small-category-label workplaceTypes').text.split()[0]

        if location in ['Romania', 'Bucharest']:

            list_jobs.append({
                "job_title": title,
                "job_link": link,
                "company": "Hkr",
                "country": "Romania",
                "city": 'Bucuresti',
                "county": 'Bucuresti',
                "remote": job_type
                })

    return list_jobs


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Hkr'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Hkr',
                  'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRbGM14QU7_VhOfFZCXQEE8jQ_Ljw7GxrXzg33ZzT71o75LHAFIDte4asoXRAaRrf6WgNU&usqp=CAU'
                  ))