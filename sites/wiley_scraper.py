#
# Company - > Wiley
# Link - https://careers.wiley.com/en/jobs?skills=&loc=Romania&loc_coords=
#
from A_OO_get_post_soup_update_dec import update_peviitor_api,DEFAULT_HEADERS
import requests
from L_00_logo import update_logo
from bs4 import BeautifulSoup
import uuid


def get_jobs():

    list_jobs = []
    url = "https://backend.ascendify.com/jobsapi/showPublicJobsList/bwL0bd7JDsDkWmO/1?filter%5Brecent_viewed%5D=&filter%5Bmy_applications%5D=&filter%5Brecent_added%5D=&filter%5Bfav%5D=&filter%5Bsort%5D=resume_collection+DESC%2C+created_date+DESC&filter%5Bsearch%5D%5B1%5D=&filter%5Bsearch%5D%5Bid%5D=&filter%5Blocation%5D%5Bcoord%5D=&filter%5Blocation%5D%5Bnull%5D=1&filter%5Blocation%5D%5Bfreetext%5D=Romania&filter%5Blocation%5D%5Brange%5D=30&filter%5Blocation%5D%5Bmap_coords%5D=&sort=&filter[location][freetext]=Romania&filter[location][map_coords]=45.943161010742,%2024.966760635376&filter[search][1]=&filter[location][range]=30&filter[location][null]=true&community_id=ccid_1b71001253&app=false&language=en"

    response = requests.get(url=url, headers=DEFAULT_HEADERS).json()['page']

    for job in response:
        soup = BeautifulSoup(job, 'lxml')
        link = soup.find('a')['href']
        title = soup.find('a').text
        city = soup.find('div', class_='muted asc-job-public-stats').text.split(' Location:')[-1].split(',')[0].strip()

        list_jobs.append({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link": link,
            "company": "Wiley",
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

company_name = 'Wiley'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Wiley',
                  'https://careers.wiley.com/img/logos/wiley-logo-black.svg'
                  ))
















