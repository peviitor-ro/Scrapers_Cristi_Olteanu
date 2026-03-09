#
# Company - > qiagen
# Link -> https://www.qiagen.com/us/careers
#
from A_OO_get_post_soup_update_dec import update_peviitor_api, DEFAULT_HEADERS
from L_00_logo import update_logo
import requests
import urllib3
from _county import get_county

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_jobs():

    jobs_list = []

    try:
        # Try the Workday API
        session = requests.Session()
        session.get('https://qiagen.wd3.myworkdayjobs.com/QIAGEN', headers=DEFAULT_HEADERS, timeout=15, verify=False)
        
        url = 'https://qiagen.wd3.myworkdayjobs.com/wday/cxs/qiagen/QIAGEN/jobs'
        
        headers = {
            'Accept': 'application/json',
            'Accept-Language': 'en-US',
            'Content-Type': 'application/json',
            'Origin': 'https://qiagen.wd3.myworkdayjobs.com',
            'Referer': 'https://qiagen.wd3.myworkdayjobs.com/QIAGEN',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }
        
        # Try with empty facets first
        data = {
            "appliedFacets": {},
            "limit": 50,
            "offset": 0,
            "searchText": ""
        }
        
        response = session.post(url=url, json=data, headers=headers, timeout=15, verify=False)
        
        if response.status_code == 200:
            result = response.json()
            jobs = result.get('jobPostings', [])
            
            for job in jobs:
                title = job.get('title', '')
                locations_text = job.get('locationsText', '')
                external_path = job.get('externalPath', '')
                
                # Filter for Romania
                if 'RO' in locations_text or 'Romania' in locations_text:
                    city = locations_text.split(',')[0].strip() if ',' in locations_text else locations_text.strip()
                    
                    if 'Cluj' in city:
                        city = 'Cluj-Napoca'
                    
                    job_link = 'https://qiagen.wd3.myworkdayjobs.com' + external_path
                    
                    # Determine remote type
                    remote_type = 'on-site'
                    
                    jobs_list.append({
                        "job_title": title,
                        "job_link": job_link,
                        "company": "qiagen",
                        "country": "Romania",
                        "city": city,
                        "county": get_county(city),
                        "remote": remote_type
                    })
    except Exception as e:
        print(f"Error fetching QIAGEN jobs: {e}")

    return jobs_list


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """
    return data_list


company_name = 'qiagen'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('qiagen',
                  'https://www.qiagen.com/sfc/images/qiagen-logo.png'
                  ))

