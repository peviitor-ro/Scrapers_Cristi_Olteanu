#
#  Company - > Crif
# Link -> https://careers.crif.com/search/?createNewAlert=false&q=&locationsearch=&optionsFacetsDD_title=&optionsFacetsDD_country=&optionsFacetsDD_location=&optionsFacetsDD_customfield1=&optionsFacetsDD_facility=
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS,update_peviitor_api
from L_00_logo import update_logo
import requests
from bs4 import BeautifulSoup
from _county import get_county


def get_jobs():
    list_jobs = []

    res = requests.get('https://careers.crif.com/search/?q=&q2=&alertId=&locationsearch=&title=&location=Ro&facility=&shifttype=&date=',headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(res.text, 'lxml')
    jobs = soup.find_all('tr', class_='data-row')

    for job in jobs:

        title = job.find('a', class_='jobTitle-link').text
        link = 'https://careers.crif.com' + job.find('a', class_='jobTitle-link')['href']
        city = str(job.find('span', class_='jobLocation').text.split(',')[0].strip()).lower().capitalize()

        list_jobs.append({
                "job_title": title,
                "job_link": link,
                "company": "Crif",
                "country": "Romania",
                "city": city,
                "county": get_county(city),
                "remote": 'on-site'
        })
        return list_jobs


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Crif'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Crif',
                  'https://rmkcdn.successfactors.com/79bb7ddc/63c14298-27ac-405e-a430-a.png'
                  ))