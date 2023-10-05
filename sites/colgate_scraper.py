#
# Company - > Colgate
# Link -> https://jobs.colgate.com/go/View-All-Jobs/8506400/?q=&q2=&alertId=&locationsearch=&title=&location=RO&department=&facility=
#
from A_OO_get_post_soup_update_dec import update_peviitor_api,DEFAULT_HEADERS
from L_00_logo import update_logo
import requests
from bs4 import BeautifulSoup
import uuid

def get_jobs():
    """
              ... this func() make a simple requests
              and collect data from Colgate API.
           """

    response = requests.get(
        'https://jobs.colgate.com/go/View-All-Jobs/8506400/?q=&q2=&alertId=&locationsearch=&title=&location=RO&department=&facility=',headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')
    list_jobs = []

    jobs = soup.find_all('tr',class_='data-row')

    for job in jobs:
        link = job.find('a',class_='jobTitle-link')['href']
        city = job.find('span',class_='jobLocation').text.split(', ')[0].strip()
        title = job.find('a',class_='jobTitle-link').text

        list_jobs.append({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link": 'https://jobs.colgate.com/'+link,
            "company": "Colgate",
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


company_name = 'Colgate'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Colgate',
                  'https://tukuz.com/wp-content/uploads/2019/11/colgate-palmolive-company-logo-vector.png'
                  ))