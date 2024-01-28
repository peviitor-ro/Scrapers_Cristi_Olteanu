#
# Company - > Sennder
# Link -> https://www.sennder.com/open-positions
#
from A_OO_get_post_soup_update_dec import update_peviitor_api,DEFAULT_HEADERS
from L_00_logo import update_logo
from bs4 import BeautifulSoup
import requests


def get_jobs():
    list_jobs = []

    response = requests.get("https://www.sennder.com/open-positions/departments/all/locations/bucharest-romania"
                            , headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, "lxml")
    jobs = soup.find_all('li', class_="mb-8")

    for job in jobs:
        title = job.find('div', class_="text-subsection-title mb-2 text-foreground-primary").text
        link = 'https://www.sennder.com/open-positions' + job.find('a')['href']
        city = job.find('span', class_="text-foreground-secondary").text.split(',')[0]

        list_jobs.append({
            "job_title": title,
            "job_link": link,
            "company": "Sennder",
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


company_name = 'Sennder'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Sennder',
                  'https://uploads-ssl.webflow.com/5f0d9d156b2682a4ff0aaa3a/5f100c78742912bf9b8ef246_Logo%20Horizontal_Orange.svg'
                  ))