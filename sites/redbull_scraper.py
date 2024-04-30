#
#  Company - > RedBull
# Link -> https://jobs.redbull.com/ro-ro/results?locations=6188&locationNames=Rom%C3%A2nia&functions=&functionNames=&keywords=
#
from A_OO_get_post_soup_update_dec import update_peviitor_api
from L_00_logo import update_logo
import requests
from _county import get_county
from _validate_city import validate_city


def get_jobs():

    response = requests.get('https://jobs.redbull.com/api/search?locations=6188&functions=&keywords=&pageSize=10&locale=ro&country=ro',
                            headers={
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
                            }).json()['jobs']
    list_jobs = []

    for job in response:
        list_jobs.append({
            "job_title": job['title'].split('-')[0],
            "job_link": 'https://jobs.redbull.com/ro-ro/' + job['slug'],
            "company": "RedBull",
            "country": "Romania",
            "city": validate_city(job['locationText'].split(',')[0]),
            "county": get_county(validate_city(job['locationText'].split(',')[0])),
            "remote": 'on-site'
        })

    return list_jobs


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list

company_name = 'RedBull'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('RedBull',
                  'https://resources.redbull.com/logos/redbullcom/v3/redbullcom-logo.svg'
                  ))