import requests as r
import lxml.html as html

# TODO: Modify the class to work with the JSON more effectively.
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

    def extract_news_information(self, parsed_news_html, news_dict) -> dict:
        news_dict["title"] = parsed_news_html.xpath(self.dict_settings['XPATH_TITLE'])
        news_dict["date"] = parsed_news_html.xpath(self.dict_settings['XPATH_DATE'])
        news_dict["lead"] = parsed_news_html.xpath(self.dict_settings['XPATH_LEAD'])

        return news_dict

    def scrape(self):
        # Extract News URLs from main page
        parsed_html = self.fetch_html(self.dict_settings['url'])
        self.extract_news_urls(parsed_html)

        # Extract the information for each news
        for news_url in self.news_set:
            news_dict = {
                "title": "",
                "date": "",
                "lead": "",
                "author": "",
                "url": news_url
            }

            self.extracted_news.append(self.extract_news_information(self.fetch_html(news_url), news_dict))