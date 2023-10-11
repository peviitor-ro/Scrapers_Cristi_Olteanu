#
# Company - > Ses
# Link -> https://careers.ses.com
#
from A_OO_get_post_soup_update_dec import update_peviitor_api, DEFAULT_HEADERS
from L_00_logo import update_logo
import requests
from bs4 import BeautifulSoup
import uuid

def get_jobs():
    list_jobs = []

    response = requests.get('https://careers.ses.com/search/?createNewAlert=false&q=&locationsearch=Romania&optionsFacetsDD_customfield3=&optionsFacetsDD_customfield5=',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    jobs = soup.find_all('tr',class_='data-row')

    for job in jobs:
        link = 'https://careers.ses.com' + job.find('a',class_='jobTitle-link')['href']
        title = job.find('a',class_='jobTitle-link').text
        city = job.find('span',class_='jobLocation').text.split(',')[0].strip()
        location = job.find('span',class_='jobLocation').text.split(',')[1].strip()

        if 'RO' in location:
            list_jobs.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link": link,
                "company": "Ses",
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


company_name = 'Ses'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Ses',
                  'https://upload.wikimedia.org/wikipedia/commons/thumb/9/9d/SES_Logo_claim_BL_M_png.png/1600px-SES_Logo_claim_BL_M_png.png?20151208115653'
                  ))
