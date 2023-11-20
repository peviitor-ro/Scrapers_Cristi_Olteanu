#
# Company - > Timken
# Link -> https://careers.timken.com/search/?q=&q2=&alertId=&locationsearch=&title=&location=Ro&department=
#
from A_OO_get_post_soup_update_dec import update_peviitor_api,DEFAULT_HEADERS
from L_00_logo import update_logo
from bs4 import BeautifulSoup
import requests


def get_jobs():
    list_jobs = []

    response = requests.get(
        'https://careers.timken.com/search/?q=&q2=&alertId=&locationsearch=&title=&location=Ro&department=',headers=DEFAULT_HEADERS)

    soup = BeautifulSoup(response.text, 'lxml')
    jobs = soup.find_all('tr', class_='data-row')

    for job in jobs:
        location = job.find('span', class_='jobLocation').text.strip()

        if 'RO' in location:

            list_jobs.append({
                "job_title": job.find('a', class_='jobTitle-link').text,
                "job_link": 'https://careers.timken.com/job.find'+job.find('a',class_='jobTitle-link')['href'],
                "company": "Timken",
                "country": "Romania",
                "city": job.find('span', class_='jobLocation').text.split()[0].strip(',')
        })
    return list_jobs

@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Timken'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Timken',
                  'https://getvectorlogo.com/wp-content/uploads/2019/05/the-timken-company-vector-logo.png'
                  ))