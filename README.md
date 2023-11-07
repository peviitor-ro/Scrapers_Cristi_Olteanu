
# Peviitor.ro Job Listings Web Scrapers

## Overview
This repository houses a collection of more than 100 Python web scrapers. These scrapers are designed to run daily through GitHub Actions as part of a CI/CD pipeline. Their primary purpose is to ensure that the job listings on https://peviitor.ro/ remain current, providing users with accurate and relevant data.

## Technologies used

- **python** as a programming language
- **bs4(BeautifullSoup)**
- **requests**
 
<p align="left"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="80" height="80"/> <img src="https://funthon.files.wordpress.com/2017/05/bs.png?w=772" alt="python" width="120" height="80"/> <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/aa/Requests_Python_Logo.png/467px-Requests_Python_Logo.png" alt="python" width="80" height="80"/></a> <a target="_blank" rel="noreferrer"></a> </p>
  
## The scraped information includes:
- job titles
- links
- locations
- job types

## The accuracy of the scraped data can be verified on the dedicated verification website: https://scrapers.peviitor.ro/.

![image](https://github.com/peviitor-ro/Scrapers_Cristi_Olteanu/assets/142798921/293710e1-0e59-4f6c-b933-ffd7d49fc300)


## Usage

To utilize this project, follow these steps:

1. Download or clone this project to a local folder.

2. Install Python 3.x and the required libraries using the following command:

3. Run the `peviitor_scraper.py` file and follow the instructions in the command-line interface to input your search term and other settings.

4. The search results will be saved in a JSON file, for example: `results.json`.

## Contributions

This project is open for contributions. If you wish to contribute, you can fork the project and submit a pull request with your changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
