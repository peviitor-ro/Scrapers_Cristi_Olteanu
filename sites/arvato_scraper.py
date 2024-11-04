#
#  Company - > Arvato
# Link -> https://jobsearch.createyourowncareer.com/Arvato_Systems/search/?q=&q2=&alertId=&locationsearch=&title=&location=RO&department=
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
import requests
from bs4 import BeautifulSoup
from _county import get_county



def get_jobs():

    list_jobs = []
    response = requests.get('https://jobsearch.createyourowncareer.com/Arvato_Systems/go/See-All-Jobs-en/3516301/?q=&q2=&alertId=&locationsearch=&title=&location=RO&department=',headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')
    jobs = soup.find_all('tr', class_='data-row')

    for job in jobs:

        title = job.find('a', class_='jobTitle-link').text
        link = 'https://jobsearch.createyourowncareer.com/' + job.find('a', class_='jobTitle-link')['href']
        city = job.find('span', class_='jobLocation').text.split(',')[0].strip()

        list_jobs.append({
            "job_title": title,
            "job_link": link,
            "company": "Arvato",
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


company_name = 'Arvato'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Arvato',
                  'https://www.bertelsmann.com/media/news-und-media/logos/sg-logo-as_teaser_2_3_lt_768_grid.gif'
                  ))