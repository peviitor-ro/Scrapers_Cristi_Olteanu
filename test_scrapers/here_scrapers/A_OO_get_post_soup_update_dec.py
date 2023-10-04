#
#
#
# This Decorator will avoid duplicate for me!
# Respect DRY
# This decorator have: default headers and soup and update data on peviitor.ro!
#
import requests
#
import os  # I do not have API KEY
#
import json


DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_8_8; like Mac OS X) AppleWebKit/535.14 (KHTML, like Gecko) Chrome/49.0.3028.253 Mobile Safari/603.0',
    'Accept-Language': 'en-US,en;q=0.5',
    'Refer': 'https://google.com',
    'DNT': '1'
}


########### UPDATE API DECORATOR ############
def update_peviitor_api(original_function):
    """
    Decorator for update data on Peviitor.ro API
    """

    def new_function(*args, **kwargs):
        company_name, data_list = args
        #
        API_KEY = os.environ.get('API_KEY')
        CLEAN_URL = 'https://api.peviitor.ro/v4/clean/'

        clean_header = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'apikey': API_KEY
            }

        clean_request = requests.post(CLEAN_URL, headers=clean_header, data={'company': company_name})
        print(f"{company_name} clean -> {clean_request.status_code}")

        post_header = {
            'Content-Type': 'application/json',
            'apikey': API_KEY
            }

        post_request_to_server = requests.post('https://api.peviitor.ro/v4/update/', headers=post_header, data=json.dumps(data_list))
        print(f"{company_name} post -> {post_request_to_server}")

        return original_function(*args, **kwargs)

    return new_function
