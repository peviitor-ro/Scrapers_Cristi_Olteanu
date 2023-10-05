#
# Company - > Kambi
# Link ->https://boards.eu.greenhouse.io/kambi
#
from A_OO_get_post_soup_update_dec import update_peviitor_api,DEFAULT_HEADERS
from L_00_logo import update_logo
import requests
from bs4 import BeautifulSoup
import uuid

def get_jobs():

    response = requests.get('https://boards.eu.greenhouse.io/kambi',headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text,'lxml')
    jobs = soup.find_all('div',class_='opening')

    list_jobs = []

    for job in jobs:
        link = 'https://boards.eu.greenhouse.io/'+job.find('a')['href']
        title = job.find('a').text
        city = job.find('span').text

        if city == 'Bucharest':
            list_jobs.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link": link,
                "company": "Kambi",
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


company_name = 'Kambi'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Kambi',
                  'https://s101-recruiting.cdn.greenhouse.io/external_greenhouse_job_boards/logos/400/043/510/resized/Kambi_Logo_2023.png?1673968948'
                  ))

