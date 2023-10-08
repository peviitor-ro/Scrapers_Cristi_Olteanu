#
# Company - > kellanova
# Link -> https://jobs.kellanova.com/search/?createNewAlert=false&q=&locationsearch=Romania&optionsFacetsDD_department=&optionsFacetsDD_country=
#

from A_OO_get_post_soup_update_dec import update_peviitor_api,DEFAULT_HEADERS
from L_00_logo import update_logo
import requests
from bs4 import BeautifulSoup
import uuid

def get_jobs():
    list_jobs = []

    response = requests.get(
        'https://jobs.kellanova.com/search/?createNewAlert=false&q=&locationsearch=Romania&optionsFacetsDD_department=&optionsFacetsDD_country=',
        headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    jobs = soup.find_all('tr', class_='data-row')

    for job in jobs:
        link = 'https://jobs.kellanova.com' + job.find('a', class_='jobTitle-link')['href']
        title = job.find('a', class_='jobTitle-link').text
        city = job.find('span', class_='jobLocation').text.split(',')[0].strip()

        list_jobs.append({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link": link,
            "company": "kellanova",
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


company_name = 'kellanova'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('kellanova',
                  'https://rmkcdn.successfactors.com/e1d74a18/93664b85-9f65-4347-b147-9.png'
                  ))
