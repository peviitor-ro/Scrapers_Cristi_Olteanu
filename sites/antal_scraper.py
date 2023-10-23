#
#  Company - > Antal
# Link -> https://www.antal.com/jobs?keywords=&sector=&location=1721&type=&page=
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS,update_peviitor_api
from L_00_logo import update_logo
import uuid
from bs4 import BeautifulSoup
import requests

def get_soup(url):

    session = requests.Session()
    response = session.get(url,headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text,'lxml')
    return soup

def get_nr_pages():

    soup_pages = get_soup('https://www.antal.com/jobs?keywords=&sector=&location=1721&type=&page=')
    nr_pages = int(soup_pages.find('a',class_='next text page-numbers')['href'].split('=')[-1])
    return nr_pages

def get_jobs():

    list_jobs = []

    for page in range(1,get_nr_pages()+1,1):

        soup_jobs = get_soup(f'https://www.antal.com/jobs?keywords=&sector=&location=1721&type=&page={page}')
        jobs = soup_jobs.find_all('li')

        for job in jobs:
            text = job.find('a',class_='job-card__link more-link')
            if text != None:
                link = text['href']
                title = job.find('a').text
                try:
                    city = job.find('ul',class_='job-card__details').text.split(',')[-2].split()[-1]
                except:
                    city = job.find('ul',class_='job-card__details').text.split(',')[-1].split()[-1]
                if city == 'Neamt' or city == 'Neamţ':
                    city = 'Piatra Neamt'
                elif city == 'Harghita':
                    city = 'Miercurea Ciuc'
                elif city == 'Dolj':
                    city = 'Craiova'
                elif city == 'Iulia':
                    city = 'Alba Iulia'
                elif city == 'Jiu':
                    city = 'Targu Jiu'
                elif city == 'Valcea':
                    city = 'Ramnicu Valcea'
                elif city == 'Mures':
                    city = 'Targu Mures'
                elif city == 'Mare':
                    city = 'Satu Mare'
                elif city == 'Romania' or city.lower() == 'negotiable' or city == 'Negotiable':
                    city = 'Bucuresti'
                elif city == 'Ialomita':
                    city = 'Slobozia'

                if 'on site' in title.lower() or 'on-site' in title.lower():
                    type = 'on-site'
                elif 'hybrid' in title.lower() or 'hibrid' in title.lower():
                    type = 'hybrid'
                elif 'remote' in title.lower() or 'Remote' in title.lower() or 'ful-remote' in title.lower():
                    type = 'remote'
                else:
                    type = 'on-site'

                list_jobs.append({
                    "id": str(uuid.uuid4()),
                    "job_title": title,
                    "job_link": link,
                    "company": "Antal",
                    "country": "Romania",
                    "city": city,
                    "remote": type
                })
    return list_jobs

@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Antal'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Antal',
                  'https://www.antal.com/app/public/images/logo.png'
                  ))

