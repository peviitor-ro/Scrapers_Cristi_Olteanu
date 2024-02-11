#
# Company - > caseware
# Link -> https://jobs.lever.co/caseware?location=Cluj%2C%20Romania
#
from A_OO_get_post_soup_update_dec import update_peviitor_api,DEFAULT_HEADERS
from L_00_logo import update_logo
from bs4 import BeautifulSoup
import requests


def get_jobs():

    req = requests.get('https://jobs.lever.co/caseware?', headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(req.text, 'lxml')
    jobs = soup.find_all('div', class_='posting')

    list_jobs = []

    for job in jobs:

        link = job.find('a', class_='posting-title')['href']
        title = job.find('h5').text
        city = job.find('span', class_='sort-by-location posting-category small-category-label location').text
        job_type = job.find('span', class_='display-inline-block small-category-label workplaceTypes').text
        cities = []

        if "Cluj" in city:
            cities.append("Cluj-Napoca")
        if 'Bucharest' in city:
            cities.append('Bucuresti')

        if cities:
            list_jobs.append({
                "job_title": title,
                "job_link": link,
                "company": "caseware",
                "country": "Romania",
                "city": city,
                "remote": job_type
            })

    return list_jobs


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'caseware'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('caseware',
                  'https://mma.prnewswire.com/media/1905723/CaseWare_International_Inc__Caseware_Expands_Global_Footprint_wi.jpg?w=200'
                  ))
