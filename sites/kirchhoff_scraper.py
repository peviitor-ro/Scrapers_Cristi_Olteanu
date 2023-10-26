#
#  Company - > kirchhoff
# Link -> https://www.kirchhoff-automotive.com/ro/cariera/posturi-vacante
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS,update_peviitor_api
from L_00_logo import update_logo
import uuid
import requests
from bs4 import BeautifulSoup


def get_jobs():

    list_jobs = []

    response = requests.get('https://www.kirchhoff-automotive.com/fileadmin/career/assets/ajax/get_ljobs.php?L=9&area=RO&continent=europe&location=-1&locationtext=Nimic%20selectat&search=&nc=1698307068323'
                            , headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')
    jobs = soup.find_all('tr')

    for job in jobs:
        title = job.find('td', class_='hyphenate text').text
        city = job.get_text().split()[-1]
        link = (f'https://www.kirchhoff-automotive.com/ro/cariera/posturi-vacante/detaliu?job=' +
                job.find('td', class_='hyphenate text')['onclick'].split(',')[0].split('(')[-1])

        list_jobs.append({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link": link,
            "company": "Kirchhoff",
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


company_name = 'Kirchhoff'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Kirchhoff',
                  'https://www.kirchhoff-automotive.com/typo3conf/ext/kirchhoff_website/Resources/Public/Images/logo.svg'
                  ))