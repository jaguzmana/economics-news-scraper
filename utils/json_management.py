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