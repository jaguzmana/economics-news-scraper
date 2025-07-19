
# Design Process

## Problem
Develop a program to collect data from news websites, specifically economics news from:
- La Republica
- El Tiempo
- El Espectador

The information to extract from each news article is the following:
- Title
- Date
- Lead
- Author
- URL

**Update:** The program now saves the extracted news directly in a MongoDB database instead of a JSON file. Each news document also includes the extraction date. Logging is still performed to a log file.


## Requirements
- The system must extract the title, date, lead, author, and URL of each economics news article from La Republica, El Tiempo, and El Espectador.
- The system must save the extracted data in a MongoDB database. Each document includes an `extracted_date` field with the extraction date (day, month, and year).
- The system must save a log with the status of each scraped news article.


## Conceptual Design

### Input/Output Diagram
Single URL --> [ **Economics News Scraper** ] --> MongoDB (newsdb.articles)

### Subsystem Decomposition
Single URL --> [ **Perform a GET Request** ] --> HTML File --> [ **Extract News URLs** ] --> News URLs --> [ **Select one News URL** ] --> News URL --> [ **Perform a GET Request** ] --> HTML File --> [ **Extract News Information** ] --> News Information --> [ **Save Data in MongoDB** ] --> MongoDB (newsdb.articles)


## Detailed Design

### Technology Selection
- Python
  - Requests module
  - LXML module
  - PyMongo module
  - Logging module

### Settings File Structure
File Name: `settings.json`

```json
{
  "news_websites": [
    {
      "name": "la_republica",
      "url": "www.larepublica.co/economia/",
      "XPATHS_NEWS_URLS_LOCATIONS": [],
      "XPATH_TITLE": "",
      "XPATH_DATE": "",
      "XPATH_LEAD": "",
      "XPATH_AUTHOR": ""
    },
    {
      "name": "el_espectador",
      "url": "www.elespectador.com/economia/",
      "XPATHS_NEWS_URLS_LOCATIONS": [],
      "XPATH_TITLE": "",
      "XPATH_DATE": "",
      "XPATH_LEAD": "",
      "XPATH_AUTHOR": ""
    },
    {
      "name": "el_tiempo",
      "url": "www.eltiempo.com/economia/",
      "XPATHS_NEWS_URLS_LOCATIONS": [],
      "XPATH_TITLE": "",
      "XPATH_DATE": "",
      "XPATH_LEAD": "",
      "XPATH_AUTHOR": ""
    }
  ]
}
```

### MongoDB News Document Structure
Each news article is stored as a document in the `articles` collection in the `newsdb` database. Example:

```json
{
  "title": "",
  "date": "",
  "lead": "",
  "author": "",
  "url": "",
  "extracted_date": "dd-mm-yyyy"
}
```
