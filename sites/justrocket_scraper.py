#
#  Company - > justrocket
# Link -> https://join.com/companies/justrocket
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS,update_peviitor_api
from L_00_logo import update_logo
import requests
import re
import json
from _county import get_county


def get_jobs():

    list_jobs = []
    response = requests.get('https://join.com/companies/justrocket', headers=DEFAULT_HEADERS)
    
    pattern = r'"jobs":\{"items":\[(.*?)\],"pagination"'
    match = re.search(pattern, response.text, re.DOTALL)
    
    if match:
        items_str = '[' + match.group(1) + ']'
        
        try:
            jobs = json.loads(items_str)
            
            for job in jobs:
                city = job.get('city', {}).get('cityName', '')
                country = job.get('city', {}).get('countryName', '')
                
                if country == 'Romania':
                    title = job.get('title', '')
                    workplace_type = job.get('workplaceType', '')
                    
                    if workplace_type == 'HYBRID':
                        remote_type = 'hybrid'
                    elif workplace_type == 'REMOTE':
                        remote_type = 'remote'
                    else:
                        remote_type = 'on-site'
                    
                    city_translations = {
                        'Cluj-Napoca': 'Cluj-Napoca',
                    }
                    city = city_translations.get(city, city)
                    
                    link = f"https://join.com/companies/justrocket/{job.get('idParam', '')}"
                    
                    list_jobs.append({
                        "job_title": title,
                        "job_link": link,
                        "company": "JUSTROCKET",
                        "country": "Romania",
                        "city": city,
                        "county": get_county(city),
                        "remote": remote_type
                    })
        except Exception as e:
            print(f"Error parsing jobs: {e}")

    return list_jobs


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'JUSTROCKET'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('JUSTROCKET',
                  'https://cdn.join.com/5f5f31e58d5d6100012b61c6/justrocket-logo-l.jpg'
                  ))

