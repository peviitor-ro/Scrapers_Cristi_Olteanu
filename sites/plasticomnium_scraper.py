#
# Company - > PlasticOmnium
# Link -> https://www.plasticomnium.com/en/careers/
#
from A_OO_get_post_soup_update_dec import update_peviitor_api, DEFAULT_HEADERS
from L_00_logo import update_logo
from bs4 import BeautifulSoup
import requests
from _county import get_county


def get_jobs():

    list_jobs = []
    req = requests.get("https://careers.opmobility.com/search/?createNewAlert=false&optionsFacetsDD_customfield1=&optionsFacetsDD_customfield2=Romania&optionsFacetsDD_customfield3=",
                       headers=DEFAULT_HEADERS, verify=False)
    soup = BeautifulSoup(req.text, "lxml")
    jobs = soup.find_all('tr', class_="data-row")

    for job in jobs:
        link = 'https://careers.plasticomnium.com/' + job.find('a', class_='jobTitle-link')['href']
        title = job.find('a', class_='jobTitle-link').text
        city = job.find('span', class_='jobLocation').text.split(',')[0].strip()

        list_jobs.append({
            "job_title": title,
            "job_link": link,
            "company": "PlasticOmnium",
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


company_name = 'PlasticOmnium'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('PlasticOmnium',
                  'https://logowik.com/content/uploads/images/plastic-omnium7255.logowik.com.webp'
                  ))



