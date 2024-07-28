import json

def load_json(path: str) -> dict:
    """
    Loads a JSON file from the specified path.

    Parameters
    ----------
    path : str
        The file path to the JSON file.

    Returns
    -------
    dict
        The loaded JSON data as a dictionary.
    """
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(path: str, data: dict) -> None:
    """
    Saves data to a JSON file at the specified path.

    Parameters
    ----------
    path : str
        The file path to save the JSON file.
    data : dict
        The data to be saved in the JSON file.

    Returns
    -------
    None
    """
    with open(path, 'a', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)