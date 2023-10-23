#
#  Company - > codecool
# Link -> https://codecool.bamboohr.com/careers/list
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS,update_peviitor_api
from L_00_logo import update_logo
import requests
import uuid

def get_jobs():
    list_jobs = []
    response = requests.get('https://codecool.bamboohr.com/careers/list',headers=DEFAULT_HEADERS).json()['result']

    for job in response:
        city = job['location']['city']
        if job['isRemote'] == 'True':
            type = 'remote'
        else:
            type = 'on-site'
        title = job['jobOpeningName']
        link = f"https://codecool.bamboohr.com/careers/{job['id']}?source=aWQ9MTA="

        if (city is None and type == 'remote') or (city == 'Bucharest'):
            list_jobs.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link": link,
                "company": "codecool",
                "country": "Romania",
                "city": city,
                "remote": type
            })
    return list_jobs

@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'codecool'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('codecool',
                  'https://kcdn.at/company/123331/3589846/codecool_logo_rgb_mono_darkgrey.companysquare.png'
                  ))


