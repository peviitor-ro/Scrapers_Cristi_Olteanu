import requests
from bs4 import BeautifulSoup
from headers import default_headers
import uuid


list_jobs = []

response = requests.get('https://boards.greenhouse.io/gympass',headers=default_headers)
soup = BeautifulSoup(response.text,'lxml')

def get_jobs():
    jobs = soup.find_all('div',class_='opening')

    for job in jobs:
        link = 'https://boards.greenhouse.io/' + job.find('a')['href']
        title = job.find('a').text
        city = job.find('span',class_='location').text

        if city == 'Bucharest':
            list_jobs.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link": link,
                "company": "Gympass",
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


company_name = 'Gympass'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Gympass',
                  'https://s2-recruiting.cdn.greenhouse.io/external_greenhouse_job_boards/logos/400/188/200/resized/Gympass_cover.png?1607553944'
                  ))