import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent 
import json
from multiprocessing import Pool, cpu_count
import tqdm 

"""
    Scraper Class aims to scrap the list of jobs taken from main. The main aim of this class is to 
    verify and validate if the job meets the required fields, then it moves forward and saves it to a temporary list. 
    The list is then returned at the end for the final step, to be tested against elasticsearch db. 
"""
class Scraper: 
    
    
    final_result = []
    
    """
        Scraping all the scripts in the given webpage to return the script required for job posting. 
    """
    @staticmethod
    def scrap_page(site):
        response = requests.get(site, headers= {'User-Agent': UserAgent().random}, timeout=5)
        response.close()
        soup = BeautifulSoup(response.text, 'html.parser')
        scripts = soup.findAll("script", {"type":"application/ld+json"})
        for script in scripts: 
            script = json.loads("".join(script.contents))
            if script["@type"] == "JobPosting":
                return script

    """
        Scraping json+ld (Schema.org) script to extract the required info. 
    """
    @staticmethod
    def scrap_job(site):
        initialData = Scraper.scrap_page(site)
        try:
            return {
                "hiringOrganization":{
                    "name":  initialData["hiringOrganization"]["name"] if "name" in  initialData["hiringOrganization"] else "",
                    "logo":  initialData["hiringOrganization"]["logo"] if "logo" in  initialData["hiringOrganization"] else "",
                    "url":   initialData["hiringOrganization"]["url"] if "url" in  initialData["hiringOrganization"] else ""
                } if "hiringOrganization" in initialData else "",
                "jobLocation": {
                    "address": initialData["jobLocation"]["address"] if "address" in  initialData["jobLocation"] else ""
                } if "jobLocation" in initialData else "",
                "employmentType":initialData["employmentType"] if "employmentType" in initialData else "",
                "description": BeautifulSoup(BeautifulSoup(initialData["description"], features="lxml").text, features="lxml").text if "description" in initialData and initialData["description"] != "None" and initialData["description"]   != None else "",
                "title": initialData["title"] if "title" in initialData else "",
                "datePosted": initialData["datePosted"] if "datePosted" in initialData else ""
            }
        except:
            print('\033[91m' + " Job at site " + site + " has been removed."+ "\033[0;33m")


    def __threaded_scraper(self):
        print("\033[0;33m")
        with Pool(processes=cpu_count()*4) as pool, tqdm.tqdm(
            total = len(self.__links)) as pbar:
                for result in pool.imap_unordered(self.scrap_job, self.__links): 
                    self.final_result.append(result)
                    pbar.update()

    
    """
        Constructor just takes links to work on them.
    """
    def __init__(self, links) -> None:
        self.__links = links
        self.__threaded_scraper()