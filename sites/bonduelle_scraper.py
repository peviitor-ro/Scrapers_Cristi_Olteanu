#
# Company - > Bonduelle
# Link -> https://jobs.bonduelle.com/search/?searchby=location&createNewAlert=false&q=&locationsearch=&geolocation=&optionsFacetsDD_country=&optionsFacetsDD_customfield1=&optionsFacetsDD_customfield3=
#
from A_OO_get_post_soup_update_dec import update_peviitor_api,DEFAULT_HEADERS
from L_00_logo import update_logo
from bs4 import BeautifulSoup
import requests
import uuid


def get_soup(url: str):

    req = requests.get(url, headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(req.text, "lxml")
    return soup


def get_num_pages():

    soup_pages = get_soup(url='https://jobs.bonduelle.com/search/?searchby=location&createNewAlert=false&q=&locationsearch=Romania&geolocation=&optionsFacetsDD_country=&optionsFacetsDD_customfield1=&optionsFacetsDD_customfield3=')
    try:
        num_jobs = int(soup_pages.find('span', class_='paginationLabel').text.split()[-1])
    except:
        num_jobs = 0
    return num_jobs


def get_jobs():
    list_jobs = []

    for page in range(0, get_num_pages(), 20):

        soup_jobs = get_soup(url=f'https://jobs.bonduelle.com/search/?searchby=location&createNewAlert=false&q=&locationsearch=Romania&geolocation=&optionsFacetsDD_country=&optionsFacetsDD_customfield1=&optionsFacetsDD_customfield3=&startrow={page}')
        jobs = soup_jobs.find_all('tr', class_='data-row')

        for job in jobs:
            title = job.find('a', class_='jobTitle-link').text
            link = 'https://jobs.bonduelle.com' + job.find('a', class_='jobTitle-link')['href']
            city = job.find('span', class_='jobLocation').text.split(',')[0].strip()

            list_jobs.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link": link,
                "company": "Bonduelle",
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


company_name = 'Bonduelle'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Bonduelle',
                  'https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Logo_Bonduelle.svg/800px-Logo_Bonduelle.svg.png?20140911225559'
                  ))