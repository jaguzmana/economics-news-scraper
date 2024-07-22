from datetime import datetime
import os

def data_storage_config(settings: dict):
    current_date = datetime.now().strftime("%d-%m-%Y")

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
