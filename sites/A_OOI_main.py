#
#
#
#
#
import os
import subprocess

# exclude files
exclude = ['__init__.py',
           'A_OO_get_post_soup_update_dec.py',
           'A_OOI_main.py',
           '000_delete_api_data.py',
           'L_00_logo.py',
           'damen_scraper.py',
           'talentkompass_scraper.py',
           'ascom_scraper'

           ]

path = os.path.dirname(os.path.abspath(__file__))

for site in os.listdir(path):
    if site.endswith('.py') and site not in exclude:
        action = subprocess.run(['python', os.path.join(path, site)], capture_output=True)
        if action.returncode != 0:
            errors = action.stderr.decode('utf-8')
            print("Error in " + site)
            print(errors)
        else:
            print("Success scraping " + site)
