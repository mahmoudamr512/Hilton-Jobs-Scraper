from Crawler import *
from Scraper import *
from multiprocessing import freeze_support
from pprint import *


def main():
    print("Starting crawler, crawling all sitemaps of HiltonJobs to find all jobs links")
    c = Crawler()
    links = c.crawl()
    print('\033[91m' + "Found " + str(len(links)) + " jobs..." + '\033[0m')
    print('\33[92m' + "Scraper starting now..."+ '\033[0m') 
    s = Scraper(links)
    print('\33[92m' + "Scraper Finished Successfully..."+ '\033[0m') 
    final_results = s.final_result
    pprint(final_results)


if __name__ == "__main__":
    freeze_support()
    main()