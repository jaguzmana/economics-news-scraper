from models.news_scraper import NewsScraper
from utils.json_management import load_json, save_json
from utils.storage_configs import data_storage_config
from utils.logger_config import logger

def main():
    try:
        logger.info("Loading settings and creating storage folder")
        settings_dict = load_json('settings.json')
        json_path = data_storage_config(settings_dict)

        logger.info("Configuring Scrapers...")
        scrapers = []
        for i, website in enumerate(settings_dict['news_websites']):
            scraper = NewsScraper(website, json_path[i])
            scrapers.append(scraper)

        count = 0
        for scraper in scrapers:
            try:
                logger.info(f"Scraping Website #{count + 1}...")
                scraper.scrape()
                logger.info(f"Saving Scraped Data...")
                save_json(scraper.json_path, scraper.extracted_news)
                count += 1
            except Exception as e:
                logger.error(f"Error processing {scraper.website}: {e}")

    except Exception as e:
        logger.critical(f"Unexpected error: {e}")

if __name__ == '__main__':
    logger.info("Starting Scraping Process...")
    main()
    logger.info("Scraping Process Completed")
