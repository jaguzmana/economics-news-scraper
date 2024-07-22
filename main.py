from models.news_scraper import NewsScraper
from utils.json_management import load_json, append_data_json
from utils.storage_configs import data_storage_config

def main():
    json_path = data_storage_config()
    settings_list = load_json('settings.json')

    la_republica_scraper = NewsScraper(settings_list['news_websites'][0], json_path[0])
    la_republica_scraper.scrape()
    append_data_json(json_path[0], la_republica_scraper.extracted_news)
    print(la_republica_scraper.extracted_news)

if __name__ == '__main__':
    main()
