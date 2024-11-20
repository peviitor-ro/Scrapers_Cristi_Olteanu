#
# Company - > Reckitt
# Link ->https://careers.reckitt.com/search/?createNewAlert=false&q=&locationsearch=Romania&optionsFacetsDD_facility=&optionsFacetsDD_country=
#
from A_OO_get_post_soup_update_dec import update_peviitor_api, DEFAULT_HEADERS
from L_00_logo import update_logo
import requests
from bs4 import BeautifulSoup
from _county import get_county
from _validate_city import validate_city


def get_jobs():
    response = requests.get(
        'https://careers.reckitt.com/search/?createNewAlert=false&q=&locationsearch=Ro&optionsFacetsDD_facility=&optionsFacetsDD_country=',
        headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')
    list_jobs = []

    jobs = soup.find_all('tr', class_='data-row')

    for job in jobs:
        link = 'https://careers.reckitt.com/' + job.find('a', class_='jobTitle-link')['href']
        title = job.find('a', class_='jobTitle-link').text
        city = validate_city(job.find('span', class_='jobLocation').text.split(',')[0].strip())

        list_jobs.append({
            "job_title": title,
            "job_link": link,
            "company": "Reckitt",
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


company_name = 'Reckitt'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Reckitt',
                  'http://rmkcdn.successfactors.com/488fb818/9253e4a3-25d5-454f-a856-0.jpg'
                  ))