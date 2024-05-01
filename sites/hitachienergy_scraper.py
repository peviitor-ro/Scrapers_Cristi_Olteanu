#
# Company - > hitachienergy
# Link -> https://www.hitachienergy.com/careers/open-jobs?filterable0-location=Romania%2FBucharest++Ilfov&filterable0-offset=0&filterable0-calculatedOffset=0
#
from A_OO_get_post_soup_update_dec import update_peviitor_api,DEFAULT_HEADERS
from L_00_logo import update_logo
import requests


def get_jobs():
    url = "https://www.hitachienergy.com/careers/open-jobs/_jcr_content/root/container/content_1/content/grid_0/joblist.listsearchresults.json"

    querystring = {"location": ["Romania/Bucharest New", "Romania/Bucharest  Ilfov"], "offset": "0",
                   "calculatedOffset": "0"}
    response = requests.get(url=url, params=querystring, headers=DEFAULT_HEADERS).json()['items']
    list_jobs = []

    for job in response:

            list_jobs.append({
                "job_title": job['title'],
                "job_link": job['url'],
                "company": "hitachienergy",
                "country": "Romania",
                "city": 'Bucuresti',
                "county": 'Bucuresti',
                "remote": 'on-site'
            })
    return list_jobs


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """
    return data_list

company_name = 'hitachienergy'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('hitachienergy',
                  'https://www.hitachienergy.com/content/dam/web/logo/hitachi-logo.svg'
                  ))

