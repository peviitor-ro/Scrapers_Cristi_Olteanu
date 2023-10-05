#
# Company - > teneco
# Link ->https://jobs.tenneco.com/search/?createNewAlert=false&q=&locationsearch=Romania
#
from A_OO_get_post_soup_update_dec import update_peviitor_api,DEFAULT_HEADERS
from L_00_logo import update_logo
import requests
from bs4 import BeautifulSoup
import uuid


def get_jobs():
    list_jobs = []

    response = requests.get('https://jobs.tenneco.com/search/?createNewAlert=false&q=&locationsearch=Ro',headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    jobs = soup.find_all('tr',class_='data-row')

    for job in jobs:
        link = 'https://jobs.tenneco.com/'+job.find('a',class_='jobTitle-link')['href']
        title = job.find('a',class_='jobTitle-link').text
        city = job.find('span',class_='jobLocation').text.split(', ')[-2].strip()
        country = job.find('span',class_='jobLocation').text.split(', ')[-1].split()[0]

        if country == 'RO':
            list_jobs.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link": link,
                "company": "teneco",
                "country": "Romania",
                "city": city
            })

    return list_jobs

@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'teneco'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('teneco',
                  'https://rmkcdn.successfactors.com/8fba3c45/d59e3e3d-da03-4939-b876-e.jpg'
                  ))
