from Crawler import *
from Scraper import *
from Elastic import *
from multiprocessing import freeze_support
from pprint import *


def main():
    final_results = []
    print("Starting crawler, crawling all sitemaps of HiltonJobs to find all jobs links")
    c = Crawler()
    links = c.crawl()
    print('\033[91m' + "Found " + str(len(links)) + " jobs..." + '\033[0m')
    print('\33[92m' + "Scraper starting now..."+ '\033[0m') 
    s = Scraper(links)
    print('\33[92m' + "Scraper Finished Successfully..."+ '\033[0m') 
    print('\033[91m' + "Pushing to elastic db..."+ '\033[0m') 
    final_results = s.final_result
    e = Elastic(final_results)
    e.push_to_db()
    print('\33[92m' + "Pushed to Elastic!" + '\033[0m')

if __name__ == "__main__":
    freeze_support()
    main()