#
# Company - > salesconsulting
# Link -> https://salesconsulting.teamtailor.com/jobs
#
from A_OO_get_post_soup_update_dec import update_peviitor_api,DEFAULT_HEADERS
from L_00_logo import update_logo
from bs4 import BeautifulSoup
import requests
from _county import get_county


def get_jobs():
    list_jobs = []

    response = requests.get('https://salesconsulting.teamtailor.com/jobs', headers=DEFAULT_HEADERS, timeout=15)
    soup = BeautifulSoup(response.text, 'lxml')

    jobs = soup.find_all('li', class_='w-full')

    for job in jobs:
        # Get job link
        link_elem = job.find('a', href=lambda h: h and '/jobs/' in h if h else False)
        if not link_elem:
            continue
            
        link = link_elem.get('href', '')
        
        # Get job text
        text = job.get_text(separator='|')
        
        # Split by | to get parts
        parts = [p.strip() for p in text.split('|') if p.strip()]
        
        # Title is usually the first meaningful text
        title = parts[0] if parts else ''
        
        # Find location
        city = ''
        job_type = 'on-site'
        
        for part in parts:
            # Check for location
            if any(loc in part for loc in ['Bucharest', 'București', 'Cluj', 'Timișoara', 'Timisoara', 'Brașov', 'Brasov', 'Iași', 'Iasi', 'Craiova', 'Constanța', 'Constanta', 'Sibiu', 'Suceava', 'Oradea', 'Ploiești', 'Ploiesti', 'Târgu Mureș', 'Targu Mures', 'Satu Mare']):
                city = part
                break
        
        # Check for remote type
        if 'remote' in text.lower():
            job_type = 'remote'
        elif 'hybrid' in text.lower():
            job_type = 'hybrid'
        
        # Map cities to Romanian names
        if 'Bucharest' in city:
            city = 'București'
        elif 'Timisoara' in city:
            city = 'Timișoara'
        elif 'Brasov' in city:
            city = 'Brașov'
        elif 'Iasi' in city:
            city = 'Iași'
        elif 'Constanta' in city:
            city = 'Constanța'
        elif 'Ploiesti' in city:
            city = 'Ploiești'
        elif 'Targu Mures' in city:
            city = 'Târgu Mureș'
        
        # Handle multiple cities - take the first one
        if ',' in city:
            city = city.split(',')[0].strip()
        
        # Skip non-Romanian cities
        if city and not any(loc in city for loc in ['Romania', 'Moldova', 'Chisinau', 'Ruse', 'Hungary']):
            list_jobs.append({
                "job_title": title,
                "job_link": link,
                "company": "salesconsulting",
                "country": "Romania",
                "city": city,
                "county": get_county(city),
                "remote": job_type
            })

    return list_jobs


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'salesconsulting'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('salesconsulting',
                  'https://www.salesconsulting.ro/images/logo.png'
                  ))

