#
# Company - > mobilexpense
# Link -> https://mobilexpense.recruitee.com/
#
from A_OO_get_post_soup_update_dec import update_peviitor_api,DEFAULT_HEADERS
from L_00_logo import update_logo
from bs4 import BeautifulSoup
import requests


def get_jobs():
    response = requests.get('https://mobilexpense.recruitee.com/', headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    list_jobs = []

    jobs = soup.find_all('div', class_='sc-465zle-1 eifEKW')

    for job in jobs:
        link = 'https://mobilexpense.recruitee.com/' + job.find('a', class_='sc-465zle-2 bCpqiX')['href']
        title = job.find('a', class_='sc-465zle-2 bCpqiX').text
        try:
            remote = job.find('span', class_='sc-1s8re0d-0 feitSf').text
        except:
            remote = 'on-site'

        city = job.find('span', class_='custom-css-style-job-location-city').text.split(' or ')
        country = job.find('span', class_='custom-css-style-job-location-country').text
        if 'Cluj' in city:
            city = 'Cluj-Napoca'

        if country == 'Romania':

            list_jobs.append({
                "job_title": title,
                "job_link": link,
                "company": "mobilexpense",
                "country": "Romania",
                "city": city,
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