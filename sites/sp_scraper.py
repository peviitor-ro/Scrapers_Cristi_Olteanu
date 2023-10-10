#
# Company - > S&P
# Link -> https://careers.spglobal.com/jobs?locations=Bucharest,Bucure%C5%9Fti,Romania&page=1
#
from A_OO_get_post_soup_update_dec import update_peviitor_api
from L_00_logo import update_logo
import requests
import uuid

def get_num_pages():
    response = requests.get('https://careers.spglobal.com/api/jobs?locations=Bucharest%252CBucure%25C5%259Fti%252CRomania&page=1&sortBy=relevance&descending=false&internal=false',
                            headers={
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                            }).json()
    num_jobs = response['totalCount']
    pages = int(num_jobs/10)
    if num_jobs%10>0:
        pages += 1
    else:
        pass
    return pages

def get_jobs():

    list_jobs = []

    for page in range(1,get_num_pages()+1,1):

        response = requests.get(f'https://careers.spglobal.com/api/jobs?locations=Bucharest%252CBucure%25C5%259Fti%252CRomania&page={page}&sortBy=relevance&descending=false&internal=false',
                                headers={
                                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                                }).json()['jobs']

        for job in response:
            full_location = job['data']['full_location']
            city = job['data']['city']
            try:
                job['data']['additional_locations']
                for item in job['data']['additional_locations']:
                    city = item['city']
            except:
                pass

            if 'Romania' in full_location:
                list_jobs.append({
                    "id": str(uuid.uuid4()),
                    "job_title": job['data']['title'],
                    "job_link": job['data']['meta_data']['canonical_url'],
                    "company": "S&P",
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


company_name = 'S&P'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('S&P',
                  'https://companieslogo.com/img/orig/SPGI-23d836fa.png?t=1651808338'
                  ))

