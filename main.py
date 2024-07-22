from models.news_scraper import NewsScraper
from utils.json_management import load_json, save_json
from utils.storage_configs import data_storage_config

def main():
    settings_dict = load_json('settings.json')
    json_path = data_storage_config(settings_dict)

    la_republica_scraper = NewsScraper(settings_dict['news_websites'][0], json_path[0])
    la_republica_scraper.scrape()
    save_json(json_path[0], la_republica_scraper.extracted_news)
    print(la_republica_scraper.extracted_news)

if __name__ == '__main__':
    main()
