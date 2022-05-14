# This class aims to return a list of URLS that are scrapable. It goes and finish crawling every sitemap available. 
import requests
from collections import deque
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import tqdm
from multiprocessing import cpu_count, Pool



class Crawler:


    # Hilton Jobs have 13 sitemaps embedded in them, we need to crawl each of them and append the jobs to crawled link.
    __scrap_links = deque()
    
    # Sitemaps
    __sitemaps = []
    
    def __init__(self):
        self.url = "https://jobs.hilton.com/us/en/sitemap_index.xml"
        
    # Function to open connection & crawl sitemap. 
    @staticmethod
    def links_generator(site):
        response = requests.get(site, headers={'User-Agent': UserAgent().random})
        soup_page = BeautifulSoup(response.text, 'lxml')
        return [url.text for url in soup_page.find_all('loc')]
        

    # Function to take a site and return all the links to scrap links queue. 
    def crawl(self):
        self.__sitemaps = self.links_generator(self.url)

        print('\33[92m', end="")
        with Pool(processes=cpu_count()*2) as pool, tqdm.tqdm(
            total = len(self.__sitemaps)) as pbar:
                for urls in pool.imap_unordered(self.links_generator, self.__sitemaps): 
                    for url in urls:
                        if '/job/' in url: 
                            self.__scrap_links.append(url)
                   
                    pbar.update()
        print('\033[0m')
        return self.__scrap_links

