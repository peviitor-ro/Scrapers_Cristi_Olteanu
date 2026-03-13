#
# Company - > nVent
# Link -> https://nvent.wd5.myworkdayjobs.com/en-US/nVent/
#
from A_OO_get_post_soup_update_dec import update_peviitor_api,DEFAULT_HEADERS
from L_00_logo import update_logo
import requests
import urllib3
from _county import get_county

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

session = requests.Session()


def get_jobs():
    
    list_jobs = []

    try:
        # Get session
        session.get('https://nvent.wd5.myworkdayjobs.com/en-US/nVent/', headers=DEFAULT_HEADERS, timeout=15, verify=False)
        
        url = 'https://nvent.wd5.myworkdayjobs.com/wday/cxs/nvent/nVent/jobs'
        
        headers = {
            'Accept': 'application/json',
            'Accept-Language': 'en-US',
            'Content-Type': 'application/json',
            'Origin': 'https://nvent.wd5.myworkdayjobs.com',
            'Referer': 'https://nvent.wd5.myworkdayjobs.com/en-US/nVent/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }
        
        data = {
            "appliedFacets": {
                "locations": ["8ed57ec2277e01cfca042a6a9c01c50e"]
            },
            "limit": 20,
            "offset": 0,
            "searchText": ""
        }
        
        response = session.post(url=url, headers=headers, json=data, timeout=15, verify=False)
        
        if response.status_code == 200:
            data = response.json()
            jobs = data.get('jobPostings', [])
            
            for job in jobs:
                title = job.get('title', '')
                locations_text = job.get('locationsText', '')
                external_path = job.get('externalPath', '')
                
                # Check if Romania
                if 'RO' in locations_text or 'Romania' in locations_text:
                    city = locations_text.split(',')[0].strip() if ',' in locations_text else locations_text.strip()
                    
                    # Map cities
                    if 'Prejmer' in city:
                        city = 'Prejmer'
                    elif 'Brasov' in city or 'Brașov' in city:
                        city = 'Brașov'
                    elif 'Ploiesti' in city or 'Ploiești' in city:
                        city = 'Ploiești'
                    
                    # Get remote type from job detail
                    job_link = 'https://nvent.wd5.myworkdayjobs.com' + external_path
                    
                    list_jobs.append({
                        "job_title": title,
                        "job_link": job_link,
                        "company": "nVent",
                        "country": "Romania",
                        "city": city,
                        "county": get_county(city),
                        "remote": 'on-site'
                    })
    except Exception as e:
        print(f"Error fetching nVent jobs: {e}")

    return list_jobs


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'nVent'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('nVent',
                  'https://seeklogo.com/images/N/nvent-logo-E3845C5AC6-seeklogo.com.png'
                  ))

