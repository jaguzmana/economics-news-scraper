import requests as r
import lxml.html as html
from random import randint
from time import sleep
from utils.logger_config import logger

class NewsScraper:
    def __init__(self, dict_settings: dict, json_path: str):
        self.dict_settings = dict_settings
        self.json_path = json_path
        self.news_set = set()
        self.extracted_news = []

    def fetch_html(self, url):
        try:
            response = r.get(url)
            response.raise_for_status()
            parsed = html.fromstring(response.text)
            return parsed
        except r.exceptions.RequestException as e:
            logger.error(f"Error fetching URL {url}: {e}")
            return None

    def extract_news_urls(self, parsed_html):
        try:
            for xpath in self.dict_settings['XPATHS_NEWS_URLS_LOCATIONS']:
                news_links = set(parsed_html.xpath(xpath))
                self.news_set.update(news_links)
        except Exception as e:
            logger.error(f"Error extracting news URLs: {e}")

    def extract_news_information(self, parsed_news_html, news_dict: dict) -> dict:
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
        return url_news.startswith(url_webpage) or url_news.startswith('/economia/')

    def create_valid_news_url(self, url_webpage: str, url_news: str) -> str:
        if not url_news.startswith(url_webpage):
            url_webpage = url_webpage.replace('/economia/', '')
            return url_webpage + url_news
        return url_news

    def wait_random_time(self, min=1, max=5) -> None:
        return sleep(randint(min, max))

    def scrape(self):
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
