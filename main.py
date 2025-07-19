from models.news_scraper import NewsScraper
from utils.json_management import load_json
from utils.logger_config import logger
from decouple import config

def main():
    try:
        #logger.info("Loading settings and creating storage folder")
        settings_dict = load_json('settings.json')
        logger.info("Configuring Scrapers...")
        scrapers = []

        mongo_uri = f'mongodb://{config("MONGO_INITDB_ROOT_USERNAME")}:{config("MONGO_INITDB_ROOT_PASSWORD")}@localhost:27017/?authSource=admin'
        mongo_db = config("MONGO_DB")
        mongo_collection = config("MONGO_COLLECTION")

        for website in settings_dict['news_websites']:
            scraper = NewsScraper(
                website,
                mongo_uri,
                mongo_db,
                mongo_collection)
            scrapers.append(scraper)

        count = 0
        for scraper in scrapers:
            try:
                logger.info(f"Scraping Website #{count + 1}...")
                scraper.scrape()
                count += 1
            except Exception as e:
                logger.error(f"Error processing {getattr(scraper, 'website', 'unknown')}: {e}")

    except Exception as e:
        logger.critical(f"Unexpected error: {e}")

if __name__ == '__main__':
    logger.info("Starting Scraping Process...")
    main()
    logger.info("Scraping Process Ended")
