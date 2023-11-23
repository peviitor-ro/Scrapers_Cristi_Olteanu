#
#  Company - > codecool
# Link -> https://codecool.bamboohr.com/careers/list
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS,update_peviitor_api
from L_00_logo import update_logo
import requests


def get_jobs():
    list_jobs = []
    response = requests.get('https://codecool.bamboohr.com/careers/list',headers=DEFAULT_HEADERS).json()['result']

    for job in response:
        city = job['location']['city']

        if job['locationType'] == '0':
            job_type = 'on-site'
        elif job['locationType'] == '1':
            job_type = 'remote'
        else:
            job_type = 'hibrid'

        title = job['jobOpeningName']
        link = f"https://codecool.bamboohr.com/careers/{job['id']}?source=aWQ9MTA="

        if city == 'Bucharest':
            list_jobs.append({
                "job_title": title,
                "job_link": link,
                "company": "codecool",
                "country": "Romania",
                "city": city,
                "remote": job_type
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


