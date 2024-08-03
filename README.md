# Economics News Scraper

## Description
The goal of this project is to create an Economics News Scraper, taking into account the problem described in the [Design.md](Design.md) file, to demonstrate Python coding knowledge. In this project, a class was created to model the general behavior of a NewsScraper, and it was configured for each website using a JSON settings file. Finally, the scraped data from each website was stored in a JSON file as the problem indicated. The technologies used for this project were *Python* and some HTML knowledge to extract the website-specific content using *XPATH*.

## Table of Contents
- [Description](#description)
- [How to run the project?](#how-to-run-the-project)
  - [Prerequisites](#prerequisites)
  - [Steps](#steps)
- [How to modify the XPATH of a website?](#how-to-modify-the-xpath-of-a-website)
  - [Steps](#steps-1)
- [License](#license)
- [Contact Information](#contact-information)

## How to run the project?

### Prerequisites
- **Python:** Ensure Python is installed on your machine and you can create a virtual environment to install the necessary modules.

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/jaguzmana/economics-news-scraper.git
   ```
  
2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   ```

3. Install the necessary modules using the `requirements.txt` file:
   ```bash
   pip install -r requirements.txt 
   ```

4. Run the project whenever you want or schedule it using *cron*:
   ```bash
   python3 main.py
   ```

5. Check out the `app.log` file or the terminal to ensure the scraper worked as expected.

## How to modify the XPATH of a website?

### Steps
1. Locate the `settings.json` file.
2. Append or modify the XPATH depending on the one you need to change:
   - `XPATHS_NEWS_URLS_LOCATIONS` (List of XPATHs)
   - `XPATH_TITLE` (Single XPATH)
   - `XPATH_DATE` (Single XPATH)
   - `XPATH_LEAD` (Single XPATH)
   - `XPATH_AUTHOR` (Single XPATH)
  
## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact Information
For questions or support, please open an issue in the [GitHub repository](https://github.com/jaguzmana/economics-news-scraper/issues) or reach out via [Twitter (now X)](https://x.com/jaguzmana_).