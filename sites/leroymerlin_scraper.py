#
#  Company - > leroymerlin
# Link -> https://job.leroymerlin.ro/jobs
#
import requests
from bs4 import BeautifulSoup
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
from _county import get_county


def get_jobs():

    list_jobs = []

    response = requests.get('https://job.leroymerlin.ro/jobs', headers=DEFAULT_HEADERS, timeout=15)
    soup = BeautifulSoup(response.text, 'lxml')

    job_links = soup.find_all('a', href=lambda h: h and '/jobs/' in h if h else False)

    for job in job_links:
        link = job.get('href', '')
        text = job.text.strip()
        
        if not text:
            continue
        
        # Split the text to get title and location
        parts = text.split('\n')
        title = parts[0].strip()
        
        # Find location - it's after the last "·"
        location = ''
        for part in reversed(parts):
            part = part.strip()
            if part and '·' in part:
                location = part.split('·')[-1].strip()
                break
            elif part and 'Magazin' not in part and 'Sediu' not in part:
                location = part.strip()
                break
        
        # Map cities
        city = 'Romania'
        
        # Handle headquarters (Sediu) - usually Bucharest
        if 'Sediu' in location or 'Central' in location:
            city = 'București'
        elif 'Cluj' in location:
            city = 'Cluj-Napoca'
        elif 'București' in location or 'Bucuresti' in location:
            city = 'București'
        elif 'Brașov' in location or 'Brasov' in location:
            city = 'Brașov'
        elif 'Iași' in location or 'Iasi' in location:
            city = 'Iași'
        elif 'Craiova' in location:
            city = 'Craiova'
        elif 'Târgu Mureș' in location or 'Targu Mures' in location:
            city = 'Târgu Mureș'
        elif 'Bistrița' in location or 'Bistrita' in location:
            city = 'Bistrița'
        elif 'Timișoara' in location or 'Timisoara' in location:
            city = 'Timișoara'
        
        # Determine remote type (if mentioned)
        job_type = 'on-site'
        if 'hibrid' in text.lower() or 'hybrid' in text.lower():
            job_type = 'hybrid'
        elif 'remote' in text.lower():
            job_type = 'remote'
        
        list_jobs.append({
            "job_title": title,
            "job_link": link,
            "company": "LeroyMerlin",
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


company_name = 'LeroyMerlin'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('LeroyMerlin',
                  'https://logowik.com/content/uploads/images/leroy-merlin8331.jpg'
                  ))

