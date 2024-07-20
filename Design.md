# Design Process

## Problem
Develop a program to collect data from news websites, specifically economics news from:
- [La Republica](www.larepublica.com)
- [El Tiempo](www.eltiempo.com)
- [El Espectador](www.elespectador.com)

The information to extract from each news article is the following:
- Title
- Date
- Lead
- Author
- URL

The program must save the extracted news in a JSON file. The name of the JSON file must include the date of the extraction (day, month, and year).
The program must generate a log file with general information about each process.

## Requirements
- The system must extract the title, date, lead, author, and URL of each economics news article from La Republica, El Tiempo, and El Espectador.
- The system must save the extracted data in a JSON file, with the JSON's name including the current date (day, month, and year).
- The system must save a log with the status of each scraped news article.

## Conceptual Design

### Input/Output Diagram
-- Website URLs --> [ **Economics News Scraper** ] -- JSON file (current date) -->

### Subsystem Decomposition
-- Website URLs --> [ **Select one Website URL** ] -- Single URL --> [ **Perform a GET Request** ] -- HTML File --> [ **Extract News URLs** ] -- News URLs --> [ **Select one News URL** ] -- News URL --> [ **Perform a GET Request** ] -- HTML File --> [ **Extract News Information** ] -- News Information --> [ **Save Data in the JSON File** ]

## Detailed Design

### Technology Selection
- Python
  - Requests module
  - LXML module
  - JSON module

### JSON File Structures

**Structure of JSON Settings File**
File Name: `settings.json`

```json
{
  "news websites": [
    {
      "name": "La Republica",
      "url": "www.larepublica.com",
      "XPATH_TITLE": "",
      "XPATH_DATE": "",
      "XPATH_LEAD": "",
      "XPATH_AUTHOR": "",
      "XPATH_NEWS_URL": ""
    },
    {
      "name": "El Espectador",
      "url": "www.elespectador.com",
      "XPATH_TITLE": "",
      "XPATH_DATE": "",
      "XPATH_LEAD": "",
      "XPATH_AUTHOR": "",
      "XPATH_NEWS_URL": ""
    },
    {
      "name": "El Tiempo",
      "url": "www.eltiempo.com",
      "XPATH_TITLE": "",
      "XPATH_DATE": "",
      "XPATH_LEAD": "",
      "XPATH_AUTHOR": "",
      "XPATH_NEWS_URL": ""
    }
  ]
}
```

**Structure of JSON Settings File**
File Name: `settings.json`
```json
[
  {
    "title": "",
    "date": "",
    "lead": "",
    "author": "",
    "url": ""
  }
]
```
