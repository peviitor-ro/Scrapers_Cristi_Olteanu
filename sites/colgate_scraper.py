#
# Company - > Colgate
# Link -> https://jobs.colgate.com/go/View-All-Jobs/8506400/?q=&q2=&alertId=&locationsearch=&title=&location=RO&department=&facility=
#
from A_OO_get_post_soup_update_dec import update_peviitor_api,DEFAULT_HEADERS
from L_00_logo import update_logo
import requests
from bs4 import BeautifulSoup
from _county import get_county
from _validate_city import validate_city


def get_soup(url):

    response = requests.get(url, headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup


def get_jobs():

    jobs_list = []
    jobs = get_soup('https://jobs.colgate.com/go/View-All-Jobs/8506400/?q=&q2=&alertId=&locationsearch=&title=&location=RO&department=&facility='
                    ).find_all('tr', class_='data-row')

    for job in jobs:
        city = job.find('span', class_='jobLocation').text.split(', ')[0].strip()

        if get_county(validate_city(city)):

            link = 'https://jobs.colgate.com/' + job.find('a', class_='jobTitle-link')['href']

            title = job.find('a', class_='jobTitle-link').text
            try:
                job_type = get_soup(link).find('span', {'data-careersite-propertyid': 'customfield5'}
                                               ).text.strip()
            except:
                job_type = 'on-site'
            city = validate_city(city)
            jobs_list.append({
                "job_title": title,
                "job_link": link,
                "company": "Colgate",
                "country": "Romania",
                "city": city,
                "county": get_county(city),
                "remote": job_type.lower()
        })
    return jobs_list


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