#
# Company - > Teva
# Link -> https://careers.teva/search/?searchby=location&createNewAlert=false&q=&locationsearch=&geolocation=&optionsFacetsDD_facility=&optionsFacetsDD_department=Romania
#
from A_OO_get_post_soup_update_dec import update_peviitor_api,DEFAULT_HEADERS
from L_00_logo import update_logo
import requests
from bs4 import BeautifulSoup
import uuid

def get_jobs():

    response = requests.get('https://careers.teva/search/?searchby=location&createNewAlert=false&q=&locationsearch=&geolocation=&optionsFacetsDD_facility=&optionsFacetsDD_department=Romania',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text,'lxml')

    jobs = soup.find_all('tr',class_='data-row')
    list_jobs = []

    for job in jobs:
        link = 'https://careers.teva'+job.find('a',class_='jobTitle-link')['href']
        title = job.find('a',class_='jobTitle-link').text
        city = job.find('span',class_='jobLocation').text.split(',')[0].strip()

        list_jobs.append({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link": link,
            "company": "Teva",
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


company_name = 'Teva'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Teva',
                  'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Teva_Pharmaceuticals_logo.png/800px-Teva_Pharmaceuticals_logo.png'
                  ))