from datetime import datetime
import os

def data_storage_config(settings: dict) -> list:
    """
    Configures data storage directories and files based on settings.

    The function creates a directory for the current date and initializes empty JSON files for each news website specified in the settings.

    Parameters
    ----------
    settings : dict
        Dictionary containing the settings, including a list of news websites.

    Returns
    -------
    list
        A list of file paths for the created JSON files.
    """
    current_date = datetime.now().strftime("%d-%m-%Y")

    if not os.path.exists('data/'):
        os.mkdir('data/')

    if not os.path.exists(f'data/{current_date}/'):
        os.mkdir(f'data/{current_date}/')

    filenames = []

    # Getting the names of the files
    for websites in settings['news_websites']:
        filename = f'data/{current_date}/{websites["name"]}.json'
        filenames.append(filename)
        
    # Creating files
    for filename in filenames:
        with open(filename, 'w') as f:
            f.write('')

    return filenames
