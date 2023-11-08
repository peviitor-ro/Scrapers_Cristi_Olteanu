#
# Company - > Edenred
# Link -> https://www.edenred.ro/ro/descopera-jobul-potrivit
#
from A_OO_get_post_soup_update_dec import update_peviitor_api,DEFAULT_HEADERS
from L_00_logo import update_logo
import requests
import uuid

list_jobs=[]

def get_pages():

  response = requests.get('https://www.edenred.ro/ro/api/jobs?page=0&_=1696064805636',headers=DEFAULT_HEADERS).json()
  nr_pages = response['pager']['total_pages']

  return nr_pages


def get_jobs():

  list_jobs = []

  for page in range(0,get_pages()):
    res = requests.get(f'https://www.edenred.ro/ro/api/jobs?page={page}&_=1696064805636').json()['rows']
    city = job['field_locatie_job']

    if 'Sfantul' in job['field_locatie_job']:
        city = 'Sfântu Gheorghe'


    for job in res:

      list_jobs.append({
        "id": str(uuid.uuid4()),
        "job_title": job['title'],
        "job_link": 'https://www.edenred.ro'+job['nid'],
        "company": "Edenred",
        "country": "Romania",
        "city": city
      })

  return list_jobs

@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Edenred'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Edenred',
                  'https://www.edenred.ro/themes/custom/edenred/images/logo_25.svg'
                  ))