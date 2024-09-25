#
# Company - > mobilexpense
# Link -> https://mobilexpense.recruitee.com/
#
from A_OO_get_post_soup_update_dec import update_peviitor_api, DEFAULT_HEADERS
from L_00_logo import update_logo
from bs4 import BeautifulSoup
import requests
from _county import get_county
from _validate_city import validate_city


def get_jobs():
    list_jobs = []

    response = requests.get('https://mobilexpense.recruitee.com/', headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')


    jobs = soup.find_all('div', class_='sc-6exb5d-3 gnPPfQ')

    for job in jobs:
        link = 'https://mobilexpense.recruitee.com' + job.find('a', class_='sc-6exb5d-1 fmfYYf')['href']
        title = job.find('a', class_='sc-6exb5d-1 fmfYYf').text
        remote = job.find('span', class_='sc-6exb5d-5 dNmtYG').text.lower()
        city = validate_city(job.find('span', class_='sc-qfruxy-1 kiOgGf custom-css-style-job-location-city').text.split(' or '))
        country = job.find('span', class_='custom-css-style-job-location-country').text

        if country == 'Romania':

            list_jobs.append({
                "job_title": title,
                "job_link": link,
                "company": "mobilexpense",
                "country": "Romania",
                "city": city,
                "county": get_county(city),
                "remote": remote
            })
    return list_jobs


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'mobilexpense'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('mobilexpense',
                  'https://careers.recruiteecdn.com/image/upload/q_auto,f_auto,w_400,c_limit/production/images/A2Dv/1EA9BGIlGXOu.png'
                  ))