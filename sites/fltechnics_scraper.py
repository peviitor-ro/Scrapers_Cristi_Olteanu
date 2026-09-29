#
# Company - > FlTechincs
# Link -> https://fltechnics.com/careers/
# Jobs -> https://careers.fltechnics.com/
#
from A_OO_get_post_soup_update_dec import update_peviitor_api,DEFAULT_HEADERS
from L_00_logo import update_logo
import requests
from _county import get_county
from _validate_city import validate_city



def get_jobs():

    list_jobs = []

    response = requests.get('https://careers.fltechnics.com/jobs.json', headers=DEFAULT_HEADERS).json()['items']

    for job in response:

        job_posting = job.get('_jobposting', {})

        for location in job_posting.get('jobLocation') or []:

            address = location.get('address', {})

            if address.get('addressCountry') != 'RO':
                continue

            title = job_posting['title']
            link = job['url']
            city = validate_city(address.get('addressLocality'))

            list_jobs.append({
                "job_title": title,
                "job_link": link,
                "company": "FlTechnics",
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


company_name = 'FlTechnics'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('FlTechnics',
                  'https://fltechnics.com/wp-content/uploads/2021/07/flt-logo-org.svg'
                  ))


