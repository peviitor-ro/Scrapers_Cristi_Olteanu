#
# Company - > Visteon
# Link -> https://recruiting.ultipro.com/VIS1004VIST/JobBoard/6ea71e1c-667f-4ddc-9024-5966baaa3256/?q=&o=postedDateDesc&f4=Xy9Fe2f_DF2W-iEWXjoYJA
#
from A_OO_get_post_soup_update_dec import update_peviitor_api
from L_00_logo import update_logo
import uuid
import requests

session = requests.session()


def prepare_post():

    url = 'https://recruiting.ultipro.com/VIS1004VIST/JobBoard/6ea71e1c-667f-4ddc-9024-5966baaa3256/JobBoardView/LoadSearchResults'

    payload = {
        "opportunitySearch": {
            "Top": 50,
            "Skip": 0,
            "QueryString": "",
            "OrderBy": [
                {
                    "Value": "postedDateDesc",
                    "PropertyName": "PostedDate",
                    "Ascending": False
                }
            ],
            "Filters": [
                {
                    "t": "TermsSearchFilterDto",
                    "fieldName": 4,
                    "extra": None,
                    "values": ["7b452f5f-ff67-5d0c-96fa-21165e3a1824"]
                },
                {
                    "t": "TermsSearchFilterDto",
                    "fieldName": 5,
                    "extra": None,
                    "values": []
                },
                {
                    "t": "TermsSearchFilterDto",
                    "fieldName": 6,
                    "extra": None,
                    "values": []
                }
            ]
        },
        "matchCriteria": {
            "PreferredJobs": [],
            "Educations": [],
            "LicenseAndCertifications": [],
            "Skills": [],
            "hasNoLicenses": False,
            "SkippedSkills": []
        }
    }
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ro-RO,ro;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Content-Length': '533',
        'Content-Type': 'application/json; charset=UTF-8',
        'Host': 'recruiting.ultipro.com',
        'Origin': 'https://recruiting.ultipro.com',
        'Referer': 'https://recruiting.ultipro.com/VIS1004VIST/JobBoard/6ea71e1c-667f-4ddc-9024-5966baaa3256/?q=&o=postedDateDesc&f4=Xy9Fe2f_DF2W-iEWXjoYJA',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': "Windows"
    }
    return url, payload, headers


def get_jobs():

    list_jobs = []

    data = prepare_post()

    response = session.post(url=data[0], headers=data[2], json=data[1]).json()['opportunities']

    for job in response:
        title = job['Title']
        link = ('https://recruiting.ultipro.com/VIS1004VIST/JobBoard/6ea71e1c-667f-4ddc-9024-5966baaa3256/OpportunityDetail?opportunityId='
                + job['Id'])
        city = ''
        first_city = job['Locations'][0]['Address']['City']
        secondary_city = job['Locations'][-1]['Address']['City']
        first_country = job['Locations'][0]['Address']['Country']['Name']
        secondary_country = job['Locations'][-1]['Address']['Country']['Name']

        if 'Romania' in first_country:
            city = first_city
        elif 'Romania' in secondary_country:
            city = secondary_city

        list_jobs.append({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link": link,
            "company": "Visteon",
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


company_name = 'Visteon'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Visteon',
                  'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/Visteon_logo_%282016%29.svg/217px-Visteon_logo_%282016%29.svg.png'
                  ))