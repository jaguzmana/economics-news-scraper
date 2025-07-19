import requests as r
import lxml.html as html
from random import randint
from time import sleep
from utils.logger_config import logger
from pymongo import MongoClient
from datetime import datetime

class NewsScraper:
    """
    A class used to scrape news from a website using specified settings.

    Attributes
    ----------
    dict_settings : dict
        Dictionary containing the settings for scraping, including XPaths and the URL of the main page.
    json_path : str
        The path to the JSON file where the scraped news will be saved.
    news_set : set
        A set to store unique news URLs.
    extracted_news : list
        A list to store the extracted news information.

    Methods
    -------
    fetch_html(url)
        Fetches the HTML content of a given URL.
    extract_news_urls(parsed_html)
        Extracts news URLs from the parsed HTML content using specified XPaths.
    extract_news_information(parsed_news_html, news_dict)
        Extracts information from the parsed news HTML content and updates the news dictionary.
    is_a_valid_news_url(url_webpage, url_news)
        Checks if the news URL is valid based on the main page URL.
    create_valid_news_url(url_webpage, url_news)
        Creates a valid news URL if it is not already complete.
    wait_random_time(min=1, max=5)
        Pauses execution for a random time between min and max seconds.
    scrape()
        Main method to scrape news URLs and extract information from each news page.
    """

    def __init__(self, dict_settings: dict, mongo_uri: str = None, mongo_db: str = None, mongo_collection: str = None) -> None:
        """
        Initializes the NewsScraper with settings and path for saving JSON.

        Parameters
        ----------
        dict_settings : dict
            Dictionary containing the settings for scraping, including XPaths and the URL of the main page.
        json_path : str
            The path to the JSON file where the scraped news will be saved.
        mongo_uri : str, optional
            The MongoDB connection URI (default is None).
        mongo_db : str, optional
            The MongoDB database name (default is None).
        mongo_collection : str, optional
            The MongoDB collection name (default is None).
        """
        self.dict_settings = dict_settings
        self.news_set = set()
        self.extracted_news = []
        # MongoDB setup
        self.mongo_client = None
        self.mongo_collection = None
        # Use environment variables if not provided
        if mongo_uri and mongo_db and mongo_collection:
            self.mongo_client = MongoClient(mongo_uri)
            self.mongo_collection = self.mongo_client[mongo_db][mongo_collection]

    def fetch_html(self, url: str):
        """
        Fetches the HTML content of a given URL.

        Parameters
        ----------
        url : str
            The URL of the webpage to fetch.

        Returns
        -------
        lxml.html.HtmlElement or None
            The parsed HTML content of the webpage, or None if an error occurs.
        """
        try:
            logger.info(f'Fetching: {url}')
            response = r.get(url)
            response.raise_for_status()
            parsed = html.fromstring(response.text)
            return parsed
        except r.exceptions.RequestException as e:
            logger.error(f"Error fetching URL {url}: {e}")
            return None

    def extract_news_urls(self, parsed_html: html.HtmlElement) -> None:
        """
        Extracts news URLs from the parsed HTML content using specified XPaths.

        Parameters
        ----------
        parsed_html : lxml.html.HtmlElement
            The parsed HTML content of the main news page.

        Returns
        -------
        None
        """
        try:
            for xpath in self.dict_settings['XPATHS_NEWS_URLS_LOCATIONS']:
                news_links = set(parsed_html.xpath(xpath))
                self.news_set.update(news_links)
        except Exception as e:
            logger.error(f"Error extracting news URLs: {e}")

    def extract_news_information(self, parsed_news_html: html.HtmlElement, news_dict: dict) -> dict:
        """
        Extracts information from the parsed news HTML content and updates the news dictionary.

        Parameters
        ----------
        parsed_news_html : lxml.html.HtmlElement
            The parsed HTML content of the news page.
        news_dict : dict
            Dictionary to store the extracted news information.

        Returns
        -------
        dict
            The updated news dictionary with extracted information.
        """
        try:
            news_dict["title"] = parsed_news_html.xpath(self.dict_settings['XPATH_TITLE'])
            news_dict["date"] = parsed_news_html.xpath(self.dict_settings['XPATH_DATE'])
            news_dict["lead"] = parsed_news_html.xpath(self.dict_settings['XPATH_LEAD'])
            news_dict["author"] = parsed_news_html.xpath(self.dict_settings['XPATH_AUTHOR'])
            return news_dict
        except Exception as e:
            logger.error(f"Error extracting news information: {e}")
            return news_dict

    def is_a_valid_news_url(self, url_webpage: str, url_news: str) -> bool:
        """
        Checks if the news URL is valid based on the main page URL.

        Parameters
        ----------
        url_webpage : str
            The URL of the main news page.
        url_news : str
            The URL of the news page to be checked.

        Returns
        -------
        bool
            True if the news URL is valid, False otherwise.
        """
        return url_news.startswith(url_webpage) or url_news.startswith('/economia/')

    def create_valid_news_url(self, url_webpage: str, url_news: str) -> str:
        """
        Creates a valid news URL if it is not already complete.

        Parameters
        ----------
        url_webpage : str
            The URL of the main news page.
        url_news : str
            The URL of the news page to be validated or completed.

        Returns
        -------
        str
            The complete and valid news URL.
        """
        if not url_news.startswith(url_webpage):
            url_webpage = url_webpage.replace('/economia/', '')
            return url_webpage + url_news
        return url_news

    def wait_random_time(self, min=1, max=5) -> None:
        """
        Pauses execution for a random time between min and max seconds.

        Parameters
        ----------
        min : int, optional
            The minimum number of seconds to wait (default is 1).
        max : int, optional
            The maximum number of seconds to wait (default is 5).

        Returns
        -------
        None
        """
        return sleep(randint(min, max))

    def insert_to_mongo(self, news_dict: dict):
        """
        Inserts the extracted news dictionary into MongoDB.

        Parameters
        ----------
        news_dict : dict
            The dictionary containing the news information to be inserted.

        Returns
        -------
        None
        """
        if self.mongo_collection is not None:
            try:
                result = self.mongo_collection.insert_one(news_dict)
                logger.info('Inserted news to MongoDB')
            except Exception as e:
                logger.error(f'Error inserting to MongoDB: {e}')

    def scrape(self) -> None:
        """
        Main method to scrape news URLs and extract information from each news page.

        Returns
        -------
        None
        """
        extracted_date = datetime.now().strftime("%d-%m-%Y")
        # Extract News URLs from main page
        parsed_html = self.fetch_html(self.dict_settings['url'])
        if parsed_html is not None:
            self.extract_news_urls(parsed_html)

            # Extract the information for each news
            for news_url in self.news_set:
                try:
                    if self.is_a_valid_news_url(self.dict_settings['url'], news_url):
                        news_url = self.create_valid_news_url(self.dict_settings['url'], news_url)
                        news_html = self.fetch_html(news_url)
                        if news_html is not None:
                            news_dict = {"url": news_url, "extracted_date": extracted_date}
                            news_dict = self.extract_news_information(news_html, news_dict)
                            self.extracted_news.append(news_dict)
                            # Insert into MongoDB if enabled
                            self.insert_to_mongo(news_dict)
                            logger.info(f"Scraped and inserted news: {news_url}")
                        self.wait_random_time()
                except Exception as e:
                    logger.error(f"Error scraping news {news_url}: {e}")
