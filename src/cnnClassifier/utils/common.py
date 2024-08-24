import os
from box import Box
import yaml
from cnnClassifier import logger
import json
import joblib
from ensure import ensure_annotations
from pathlib import Path
from typing import Any
import base64

@ensure_annotations
def read_yaml(path_to_yaml: Path) -> Box:
    """reads yaml file and returns

    Args:
        path_to_yaml (str): path like input

    Raises:
        ValueError: if yaml file is empty
        e: empty yaml file

    Returns:
        Box: Box type
    """
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            if not content:
                raise ValueError(f"yaml file is empty")
            logger.info(f"yaml file: {path_to_yaml} loaded successfully")
            return Box(content)
    except Exception as e:
        raise e

@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """creates list of directories

    Args:
        path_to_yaml (list): list of path of directories
        ignore_log (bool, optional): ignore if multiple dirs is to be created. Default to false.
    """

    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"created directory at: {path}")

@ensure_annotations
def save_json(path: Path, data: dict):
    """save json data

    Args:
        path (Path): path to json file
        data (dict): data to be saved in json file
    """

    with open(path, "w") as f:
        json.dump(data, f, indent=4)

    logger.info(f"{path} saved successfully")

@ensure_annotations
def load_json(path: Path) -> Box:
    """load json files data

    Args:
        path (Path): path to json file

    Returns:
        Box: data as class attributes instead of dict
    """

    with open(path) as f:
        content = json.load(f)
        
    logger.info(f"json file: {path} loaded successfully")
    return Box(content)

@ensure_annotations
def save_bin(data: Any, path: Path):
    """ save binary file
    
    Args:
        data (Any): data to be saved as binary 
        path (Path): path to binary file
    """

    joblib.dump(value=data, filename=path)
    logger.info(f"{path} saved successfully")

@ensure_annotations
def load_bin(path: Path) -> Any:
    """load binary data

    Args:
        path (Path): path to binary file

    Returns:
        Any: object stored in the file
    """
    data = joblib.load(path)
    logger.info(f"{path} loaded successfully")
    return data

@ensure_annotations
def get_size(path: Path) -> str:
    """get size in KB
    
    Args:
        path (Path): path to file

    Returns:
        str: size in KB 
    """

    size_in_kb = round(os.path.getsize(path)/1024)
    return f"{size_in_kb} KB"

@ensure_annotations
def decodeImage(imgstring, fileName):
    imgdata = base64.b64decode(imgstring)
    with open(fileName, 'wb') as f:
        f.write(imgdata)
        f.close()

def encodeImageIntoBase64(croppedImagePath):
    with open(croppedImagePath, "rb") as image_file:
        return base64.b64encode(image_file.read())
