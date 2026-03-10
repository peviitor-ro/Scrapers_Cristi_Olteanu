#
# Company - > hitachienergy
# Link -> https://www.hitachienergy.com/careers/open-jobs?filterable0-location=Romania%2FBucharest++Ilfov&filterable0-offset=0&filterable0-calculatedOffset=0
#
from A_OO_get_post_soup_update_dec import update_peviitor_api,DEFAULT_HEADERS
from L_00_logo import update_logo
from _county import get_county
import requests


def get_jobs():
    url = "https://www.hitachienergy.com/careers/open-jobs/_jcr_content/root/container/content_1/content/grid_0/joblist.listsearchresults.json"

    response = requests.get(url=url, params={"location": "Romania", "offset": "0"}, headers=DEFAULT_HEADERS).json()
    list_jobs = []

    for job in response.get('items', []):
        location = job.get('location', '')
        
        if 'Romania' in location:
            # Handle multi-location jobs - find the Romania city
            if ';' in location:
                locations = [loc.strip() for loc in location.split(';')]
                romania_loc = None
                for loc in locations:
                    if 'Romania' in loc:
                        romania_loc = loc
                        break
                if romania_loc:
                    city = romania_loc.split(',')[0].strip()
                else:
                    city = 'București'
            else:
                city = location.split(',')[0].strip()
            
            city_translations = {
                'Bucharest': 'București',
            }
            city = city_translations.get(city, city)
            
            if 'Remote' in location:
                remote_type = 'remote'
            elif 'Hybrid' in location:
                remote_type = 'hybrid'
            else:
                remote_type = 'on-site'
            
            list_jobs.append({
                "job_title": job['title'],
                "job_link": job['url'],
                "company": "hitachienergy",
                "country": "Romania",
                "city": city,
                "county": get_county(city) if city else 'Bucuresti',
                "remote": remote_type
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

