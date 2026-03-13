#
# Company - > konecranes
# Link -> https://konecranes.careers/jobs
#
from A_OO_get_post_soup_update_dec import update_peviitor_api,DEFAULT_HEADERS
from L_00_logo import update_logo
import requests
from bs4 import BeautifulSoup
import re
from _county import get_county


def get_romania_job_urls():
    response = requests.get('https://konecranes.careers/vacanciessitemap.xml', headers=DEFAULT_HEADERS)
    job_urls = re.findall(r'<loc>(.*?job/.*?)</loc>', response.text)
    romania_jobs = [url for url in job_urls if 'romania' in url.lower()]
    return romania_jobs


def get_jobs():

    list_jobs = []
    romania_job_urls = get_romania_job_urls()

    for url in romania_job_urls:
        try:
            response = requests.get(url, headers=DEFAULT_HEADERS, timeout=15)
            soup = BeautifulSoup(response.text, 'lxml')
            
            title = soup.find('title')
            if title:
                title_text = title.text.strip().split('|')[0].strip()
            else:
                continue
            
            # Look for location
            location_text = ''
            location_elem = soup.find(string=re.compile(r'Satu Mare|Timisoara|Târgu Mureș|Bucharest', re.I))
            if location_elem:
                # Find the location element
                location_parent = location_elem.parent
                if location_parent:
                    location_text = location_parent.text.strip()
            
            # If not found, look for location in the page
            if not location_text:
                location_match = re.search(r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*),\s*Romania', response.text)
                if location_match:
                    location_text = location_match.group(1)
                else:
                    location_text = 'Romania'
            
            # Determine city
            city_county_map = {
                'Satu Mare': ('Satu Mare', 'Satu Mare'),
                'Timișoara': ('Timișoara', 'Timiș'),
                'Timisoara': ('Timișoara', 'Timiș'),
                'Târgu Mureș': ('Târgu Mureș', 'Mureș'),
                'Targu Mures': ('Târgu Mureș', 'Mureș'),
                'București': ('București', 'București'),
            }
            
            city = 'Romania'
            county = None
            for key, (city_name, county_name) in city_county_map.items():
                if key in location_text:
                    city = city_name
                    county = county_name
                    break
            
            # Determine remote type
            remote_type = 'on-site'
            if 'Hybrid' in response.text:
                remote_type = 'hybrid'
            elif 'Remote' in response.text:
                remote_type = 'remote'
            
            list_jobs.append({
                "job_title": title_text,
                "job_link": url,
                "company": "konecranes",
                "country": "Romania",
                "city": city,
                "county": county,
                "remote": remote_type
            })
        except Exception as e:
            print(f"Error fetching {url}: {e}")

    return list_jobs


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """
    return data_list


company_name = 'konecranes'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('konecranes',
                  'https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/Konecranes-Logo.svg/250px-Konecranes-Logo.svg.png?20140815081543'
                  ))

