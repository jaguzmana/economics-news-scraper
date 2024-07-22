from datetime import datetime
import os

# TODO: Modify function to work with the JSON more effectively.
def data_storage_config():
    current_date = datetime.now().strftime("%d-%m-%Y")

    if not os.path.exists(f'data/{current_date}/'):
        os.mkdir(f'data/{current_date}/')

    filenames = []

    filename1 = f'data/{current_date}/news_la_republica.json'
    filename2 = f'data/{current_date}/news_el_espectador.json'
    filename3 = f'data/{current_date}/news_el_tiempo.json'
    filenames.append(filename1)
    filenames.append(filename2)
    filenames.append(filename3)

    with open(filename1, 'w') as f:
        f.write('')

    with open(filename2, 'w') as f:
        f.write('')

    with open(filename3, 'w') as f:
        f.write('')

    return filenames
