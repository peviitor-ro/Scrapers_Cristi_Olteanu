#
# Company - > konecranes
# Link ->https://careers.konecranes.com/Konecranes/search/?createNewAlert=false&q=&locationsearch=Romania
#
from A_OO_get_post_soup_update_dec import update_peviitor_api,DEFAULT_HEADERS
from L_00_logo import update_logo
import requests
from bs4 import BeautifulSoup
import uuid


def get_jobs():

    list_jobs = []
    response = requests.get('https://careers.konecranes.com/Konecranes/search/?createNewAlert=false&q=&locationsearch=Romania',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text,'lxml')
    jobs = soup.find_all('tr', class_='data-row')

    for job in jobs:
        link = 'https://careers.konecranes.com' + job.find('a', class_='jobTitle-link')['href']
        city = job.find('span', class_='jobLocation').text.split(',')[0].strip()
        title = job.find('a', class_='jobTitle-link').text

        list_jobs.append({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link": link,
            "company": "konecranes",
            "country": "Romania",
            "city": city,
        })
    return list_jobs

@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'konecranes'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('konecranes',
                  'https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/Konecranes-Logo.svg/250px-Konecranes-Logo.svg.png?20140815081543'
                  ))
