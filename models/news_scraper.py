import requests as r
import lxml.html as html
from random import randint
from time import sleep
from utils.logger_config import logger

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

    def __init__(self, dict_settings: dict, json_path: str) -> None:
        """
        Initializes the NewsScraper with settings and path for saving JSON.

        Parameters
        ----------
        dict_settings : dict
            Dictionary containing the settings for scraping, including XPaths and the URL of the main page.
        json_path : str
            The path to the JSON file where the scraped news will be saved.
        """
        self.dict_settings = dict_settings
        self.json_path = json_path
        self.news_set = set()
        self.extracted_news = []

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

    def scrape(self) -> None:
        """
        Main method to scrape news URLs and extract information from each news page.

        Returns
        -------
        None
        """
        # Extract News URLs from main page
        parsed_html = self.fetch_html(self.dict_settings['url'])
        if parsed_html is not None:
            self.extract_news_urls(parsed_html)

            # Extract the information for each news
            for news_url in self.news_set:
                count = 0
                try:
                    if self.is_a_valid_news_url(self.dict_settings['url'], news_url):
                        news_url = self.create_valid_news_url(self.dict_settings['url'], news_url)

                        news_dict = {
                            "title": "",
                            "date": "",
                            "lead": "",
                            "author": "",
                            "url": news_url
                        }

                        self.wait_random_time()
                        parsed_news_html = self.fetch_html(news_url)

                        if parsed_news_html is not None:
                            self.extracted_news.append(self.extract_news_information(parsed_news_html, news_dict))
                except Exception as e:
                    logger.error(f"Error processing news URL {news_url}: {e}")
