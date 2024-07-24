import requests as r
import lxml.html as html

class NewsScraper:
    def __init__(self, dict_settings: dict, json_path: str):
        self.dict_settings = dict_settings
        self.json_path = json_path
        self.news_set = set()
        self.extracted_news = []

    def fetch_html(self, url):
        response = r.get(url)

        # Validate the status code
        response.raise_for_status()

        parsed = html.fromstring(response.text)
        return parsed

    def extract_news_urls(self, parsed_html):
        for xpath in self.dict_settings['XPATHS_NEWS_URLS_LOCATIONS']:
            news_links = set(parsed_html.xpath(xpath))
            self.news_set.update(news_links)

    def extract_news_information(self, parsed_news_html, news_dict: dict) -> dict:
        news_dict["title"] = parsed_news_html.xpath(self.dict_settings['XPATH_TITLE'])
        news_dict["date"] = parsed_news_html.xpath(self.dict_settings['XPATH_DATE'])
        news_dict["lead"] = parsed_news_html.xpath(self.dict_settings['XPATH_LEAD'])
        news_dict["author"] = parsed_news_html.xpath(self.dict_settings['XPATH_AUTHOR'])

        return news_dict

    # TODO: Implement this function in the code.
    def is_a_valid_news_url(self, url_webpage: str, url_news: str) -> bool:
        if url_news.find(url_webpage) == 0 or url_news.find('/economia/') == 0:
            return True

        return False

    def create_valid_news_url(self, url_webpage: str, url_news: str) -> str:
        if url_news.find(url_webpage) == -1:
            url_webpage = url_webpage.replace('/economia/', '')
            return url_webpage + url_news

        return url_news

    def scrape(self):
        # Extract News URLs from main page
        parsed_html = self.fetch_html(self.dict_settings['url'])
        self.extract_news_urls(parsed_html)

        # Extract the information for each news
        for news_url in self.news_set:
            
            if self.is_a_valid_news_url(self.dict_settings['url'], news_url):
            
                news_url = self.create_valid_news_url(self.dict_settings['url'], news_url)
                
                news_dict = {
                    "title": "",
                    "date": "",
                    "lead": "",
                    "author": "",
                    "url": news_url
                }
                
                self.extracted_news.append(self.extract_news_information(self.fetch_html(news_url), news_dict))
