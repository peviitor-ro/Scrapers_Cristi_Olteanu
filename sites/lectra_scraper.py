#
# Company - > Lectra
# Link -> https://careers.lectra.com/search/?q=&q2=&alertId=&title=&location=RO&date=
#
from A_OO_get_post_soup_update_dec import update_peviitor_api,DEFAULT_HEADERS
from L_00_logo import update_logo
from bs4 import BeautifulSoup
import requests
from _county import get_county


def get_jobs():
    list_jobs = []

    response = requests.get('https://careers.lectra.com/search/?q=&q2=&alertId=&title=&location=RO&date=',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')
    jobs = soup.find_all('tr', class_='data-row')

    for job in jobs:

        title = job.find('a', class_='jobTitle-link').text
        link = 'https://careers.lectra.com' + job.find('a', class_='jobTitle-link')['href']
        city = job.find('span', class_='jobLocation').text.split(',')[0].strip()

        if 'Cluj' in city:
            city = 'Cluj-Napoca'

        list_jobs.append({
            "job_title": title,
            "job_link": link,
            "company": "Lectra",
            "country": "Romania",
            "city": city,
            "county": get_county(city),
            "remote": 'on-site'
        })
    return list_jobs


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Lectra'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Lectra',
                  'https://rmkcdn.successfactors.com/ef2b0b62/f85e3f8f-b370-4d6a-8d64-b.jpg'
                  ))